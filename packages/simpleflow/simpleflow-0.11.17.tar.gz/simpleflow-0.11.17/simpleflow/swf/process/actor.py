import abc
import functools
import logging
import multiprocessing
import signal
from builtins import range

from setproctitle import setproctitle

import swf.actors
import swf.exceptions
from simpleflow import utils
from simpleflow.swf.helpers import swf_identity


logger = logging.getLogger(__name__)


__all__ = ['Supervisor', 'Poller']


def reset_signal_handlers(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        return func(*args, **kwargs)

    wrapped.__wrapped__ = func
    return wrapped


def with_state(state):
    def wrapper(method):
        @functools.wraps(method)
        def wrapped(self, *args, **kwargs):
            logger.debug('entering state {}: {}(args={}, kwargs={})'.format(
                state, method.__name__, args, kwargs))
            self.state = state
            return method(self, *args, **kwargs)

        wrapped.__wrapped__ = method
        return wrapped
    return wrapper


def get_payload_name(payload):
    import types

    if isinstance(payload, types.MethodType):
        instance = payload.im_self
        return '{}.{}'.format(instance.__class__.__name__, payload.__name__)
    elif isinstance(payload, types.FunctionType):
        return payload.__name__

    raise TypeError('invalid payload type {}'.format(type(payload)))


class Supervisor(object):
    def __init__(self, payload, arguments=None, nb_children=None):
        # compare explicitly to "None" there because nb_children could be 0
        if nb_children is None:
            self._nb_children = multiprocessing.cpu_count()
        else:
            self._nb_children = nb_children
        self._processes = []
        self._payload = payload
        self._args = arguments if arguments is not None else ()

    def start(self):
        logger.info('starting {}'.format(self._payload))
        setproctitle('simpleflow {}(payload={})'.format(
            self.__class__.__name__,
            get_payload_name(self._payload),
        ))
        assert len(self._processes) == 0
        for _ in range(self._nb_children):
            child = multiprocessing.Process(
                target=self._payload,
                args=self._args,
            )
            child.start()
            self._processes.append(child)
        for proc in self._processes:
            proc.join()

    def stop(self):
        assert len(self._processes) > 0
        self._processes = []

    def restart(self):
        self.stop()
        self.start()

    def bind_signal_handlers(self):
        """Binds signals for graceful shutdown.

        - SIGTERM and SIGINT lead to a graceful shutdown.
        - SIGSEGV, SIGFPE, SIGABRT, SIGBUS and SIGILL displays a traceback
          using the faulthandler library if available.

        """
        def signal_graceful_shutdown(signum, frame):
            """
            Note: Function is nested to have a reference to *self*.

            """
            if not self.is_alive:
                return

            logger.info(
                'signal %d caught. Shutting down %s',
                signum,
                self.name,
            )
            self.is_alive = False
            self.stop(graceful=True)

        # optionnally use faulthandler if available
        try:
            import faulthandler
            faulthandler.enable()
        except ImportError:
            pass

        signal.signal(signal.SIGTERM, signal_graceful_shutdown)
        signal.signal(signal.SIGINT, signal_graceful_shutdown)


class NamedMixin(object):
    def __init__(self, name='', state='initializing'):
        self._name = name
        self._state = state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.set_process_name()

    @property
    def name(self):
        return self._name

    def set_process_name(self, name=None):
        if name is None:
            klass = self.__class__.__name__
            task_list = self.task_list
            name = '{}(task_list={})'.format(klass, task_list)

        setproctitle('simpleflow {}[{}]'.format(name, self.state))


class Poller(NamedMixin, swf.actors.Actor):
    """Multi-processing implementation of a SWF actor.

    """
    def __init__(self,
                 domain,
                 task_list=None,
                 *args, **kwargs):
        self.is_alive = False
        swf.actors.Actor.__init__(self, domain, task_list)
        super(Poller, self).__init__(
            domain,
            task_list,
            *args,
            **kwargs
        )

    @property
    def identity(self):
        """Identity when polling decision task.

        http://docs.aws.amazon.com/amazonswf/latest/apireference/API_PollForDecisionTask.html

        Identity of the decider making the request, which is recorded in the
        DecisionTaskStarted event in the workflow history. This enables
        diagnostic tracing when problems arise. The form of this identity is
        user defined. Minimum length of 0. Maximum length of 256.

        """
        return swf_identity()

    def stop_gracefully(self, join_timeout=60):
        self._worker.join(join_timeout)

    def stop_forcefully(self):
        self._worker.terminate()

    @with_state('running')
    def start(self):
        """
        Start the main decider process. There is no daemonization. The process
        is intended to be run inside a supervisor process.

        """
        logger.info("starting %s on domain %s", self.name, self.domain.name)
        self.set_process_name()
        while self.is_alive:
            try:
                response = self._poll()
            except swf.exceptions.PollTimeout:
                continue
            self.process(response)

    @with_state('stopping')
    def stop(self, graceful=True, join_timeout=60):
        """Stop the actor processes and subprocesses.

        :param graceful: wait for children processes?
        :type  graceful: bool.
        :param join_timeout: maximum time to wait for children.
        :type  join_timeout: int.
        """
        logger.info('stopping %s', self.name)
        self.is_alive = False  # No longer take requests.

        if graceful:
            self.stop_gracefully(join_timeout)
        else:
            self.stop_forcefully()

    def _complete(self, token, response):
        """
        Complete with retry.
        :param token:
        :type token: str
        :param response: response: decision list, JSON result, ...
        :type response: Any
        :return:
        :rtype:
        """
        # FIXME this is a public member
        try:
            complete = utils.retry.with_delay(
                nb_times=self.nb_retries,
                delay=utils.retry.exponential,
                log_with=logger.exception,
                except_on=swf.exceptions.DoesNotExistError,
            )(self.complete)  # Exponential backoff on errors.
            complete(token, response)
        except Exception as err:
            # This is embarrassing because the decider cannot notify SWF of the
            # task completion. As it will not try again, the task will
            # timeout (start_to_complete).
            logger.exception("cannot complete task: %s", str(err))

    @abc.abstractmethod
    def poll(self, task_list, identity):
        raise NotImplementedError

    @abc.abstractmethod
    def complete(self, token, response):
        raise NotImplementedError

    @abc.abstractmethod
    def process(self, request):
        pass

    def _poll(self):
        """
        Polls a task represented by its token and data. It uses long-polling
        with a timeout of one minute.

        See also
        http://docs.aws.amazon.com/amazonswf/latest/apireference/API_PollForDecisionTask.html#API_PollForDecisionTask_RequestSyntax
        http://docs.aws.amazon.com/amazonswf/latest/apireference/API_PollForActivityTask.html#API_PollForActivityTask_RequestSyntax

        :returns:
        :rtype: swf.responses.Response
        """
        task_list = self.task_list
        identity = self.identity

        logger.debug("polling task on %s", task_list)
        try:
            response = self.poll(
                task_list,
                identity=identity,
            )
        except swf.exceptions.PollTimeout:
            logger.debug('{}: PollTimeout'.format(self))
            raise
        except Exception as err:
            logger.error(
                "exception %s when polling on %s",
                str(err),
                task_list,
            )
            raise
        return response
