# This file is part of eventmq.
#
# eventmq is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# eventmq is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eventmq.  If not, see <http://www.gnu.org/licenses/>.
from testfixtures import LogCapture
import unittest

import mock

from .. import conf
from ..client import messages


class TestClass(object):
    """
    class to use in the path_from_callable test
    """
    def mymethod(self):
        """
        this method is used as the callable in
        :meth:`TestCase.test_path_from_callable`
        """
        return True


class CallableTestClass(object):
    def __call__(self):
        return True


class TestCase(unittest.TestCase):
    @mock.patch('eventmq.client.messages.send_request')
    def test_defer_job(self, sndreq_mock):
        import urlparse

        _msgid = 'mv029aisjf-09asdfualksd-aklds290fjoiw'

        sndreq_mock.return_value = _msgid
        socket = mock.Mock()

        msgid = messages.defer_job(socket, urlparse.urlsplit,
                                   args=[1, 2],
                                   kwargs={'a': 1, 'b': 2},
                                   class_args=[9, 8],
                                   class_kwargs={'z': 9, 'y': 8},
                                   reply_requested=True,
                                   guarantee=False,
                                   retry_count=3,
                                   queue='test_queue')
        # defer_job should return _msgid untouched
        self.assertEqual(msgid, _msgid)

        msg = ['run', {
            'callable': 'urlsplit',
            'path': 'urlparse',
            'args': [1, 2],
            'kwargs': {'a': 1, 'b': 2},
            'class_args': [9, 8],
            'class_kwargs': {'z': 9, 'y': 8},
        }]

        sndreq_mock.assert_called_with(socket, msg,
                                       reply_requested=True,
                                       guarantee=False,
                                       retry_count=3,
                                       queue='test_queue')

        with LogCapture() as log_checker:
            # don't blow up on a non-callable
            messages.defer_job(socket, 'non-callable')

            # don't blow up on some random nameless func
            def nameless_func():
                return True
            nameless_func.func_name = ''
            messages.defer_job(socket, nameless_func)

            # don't blow-up for pathless functions
            nameless_func.func_name = 'nameless_func'
            nameless_func.__module__ = None
            messages.defer_job(socket, nameless_func)

            # log an error if a callable instance object is passed
            callable_obj = CallableTestClass()
            messages.defer_job(socket, callable_obj)

            log_checker.check(
                ('eventmq.client.messages',
                 'ERROR',
                 'Encountered non-callable func: non-callable'),
                ('eventmq.client.messages',
                 'ERROR',
                 'Encountered callable with no name in '
                 'eventmq.tests.test_client_messages'),
                ('eventmq.client.messages',
                 'ERROR',
                 'Encountered callable with no __module__ path nameless_func'),
                ('eventmq.utils.functions',
                 'ERROR',
                 'Encountered unknown callable ({}) type instanceobject'.
                 format(callable_obj)),
                ('eventmq.client.messages',
                 'ERROR',
                 'Encountered callable with no name in '
                 'eventmq.tests.test_client_messages'),
            )

    def test_path_from_callable(self):
        import mimetools
        funcpath = messages.path_from_callable(mimetools.choose_boundary)

        t = TestClass()
        methpath = messages.path_from_callable(t.mymethod)

        self.assertEqual(funcpath, ('mimetools', 'choose_boundary'))
        self.assertEqual(
            methpath,
            ('eventmq.tests.test_client_messages:TestClass', 'mymethod'))

    @mock.patch('eventmq.client.messages.send_schedule_request')
    def test_schedule(self, send_schedule_req_mock):
        import mimetools
        _msgid = 'ovznopi4-)*(@#$Nn0av84-a0cn84n03'
        send_schedule_req_mock.return_value = _msgid

        socket = mock.Mock()

        msgid = messages.schedule(socket, mimetools.decode,
                                  interval_secs=500,
                                  args=(1, 2),
                                  kwargs={'a': 1, 'b': 2},
                                  class_args=(9, 8),
                                  class_kwargs={'z': 9, 'y': 8},
                                  headers=('guarantee', 'poop'),
                                  queue='blurp')

        # send_schedule should return an untouched message id
        self.assertEqual(msgid, _msgid)

        msg = ['run', {
            'callable': 'decode',
            'path': 'mimetools',
            'args': (1, 2),
            'kwargs': {'a': 1, 'b': 2},
            'class_args': (9, 8),
            'class_kwargs': {'z': 9, 'y': 8},
        }]

        send_schedule_req_mock.assert_called_with(
            socket,
            interval_secs=500,
            cron='',  # default arg
            message=msg,
            headers=('guarantee', 'poop'),
            queue='blurp',
            unschedule=False)  # default arg

        with LogCapture() as log_checker:
            # don't blow up on a non-callable
            messages.schedule(socket, 'non-callable',
                              class_args=(123,),
                              interval_secs=10)

            # don't blow up on some random nameless func
            def nameless_func():
                return True
            nameless_func.func_name = ''
            messages.schedule(socket, nameless_func,
                              class_args=(48,),
                              interval_secs=19)

            # don't blow-up for pathless functions
            nameless_func.func_name = 'nameless_func'
            nameless_func.__module__ = None
            messages.schedule(socket, nameless_func,
                              class_args=(123,),
                              interval_secs=8920)

            # log an error if a callable instance object is passed
            callable_obj = CallableTestClass()
            messages.schedule(socket, callable_obj,
                              class_args=(123,),
                              interval_secs=23)

            # error if class_args does't have an inital id. (if this test needs
            # to be removed, also remove the class_args from the above calls)
            messages.schedule(socket, mimetools.decode)

            # error if neither cron or interval_secs is specified
            messages.schedule(socket, mimetools.decode, class_args=(123,))

            log_checker.check(
                ('eventmq.client.messages',
                 'ERROR',
                 'Encountered non-callable func: non-callable'),
                ('eventmq.client.messages',
                 'ERROR',
                 'Encountered callable with no name in '
                 'eventmq.tests.test_client_messages'),
                ('eventmq.client.messages',
                 'ERROR',
                 'Encountered callable with no __module__ path nameless_func'),
                ('eventmq.utils.functions',
                 'ERROR',
                 'Encountered unknown callable ({}) type instanceobject'.
                 format(callable_obj)),
                ('eventmq.client.messages',
                 'ERROR',
                 'Encountered callable with no name in '
                 'eventmq.tests.test_client_messages'),
                ('eventmq.client.messages',
                 'ERROR',
                 'First `class_args` argument must be caller_id for '
                 'scheduling interval jobs'),
                ('eventmq.client.messages',
                 'ERROR',
                 'You must sepcify either `interval_secs` or `cron`, but not '
                 'both (or neither)'),
            )

    @mock.patch('eventmq.client.messages.send_emqp_message')
    def test_send_request(self, snd_empq_msg_mock):
        _msgid = '0svny2rj8d0-aofinsud4839'
        snd_empq_msg_mock.return_value = _msgid

        socket = mock.Mock()

        msg = {'alksjfd': [1, 2],
               'laksdjf': 4,
               'alkfjds': 'alksdjf'}

        msgid = messages.send_request(socket, msg,
                                      reply_requested=True,
                                      guarantee=False,
                                      retry_count=2,
                                      queue='mozo')
        self.assertEqual(msgid, _msgid)
        snd_empq_msg_mock.assert_called_with(
            socket, 'REQUEST',
            ('mozo',
             'reply-requested,retry-count:2',
             messages.serialize(msg)))

    @mock.patch('eventmq.client.messages.send_emqp_message')
    def test_send_schedule_request(self, snd_empq_msg_mock):
        _msgid = 'va08n45-lanf548afn984-m7489vs'
        snd_empq_msg_mock.return_value = _msgid

        socket = mock.Mock()

        msg = {'20if': [1, 2],
               'mu8vc': 5,
               'zhx7': {'a': 1}}

        msgid = messages.send_schedule_request(socket, msg,
                                               interval_secs=38)
        self.assertEqual(msgid, _msgid)

        snd_empq_msg_mock.assert_called_with(
            socket, 'SCHEDULE',
            (conf.DEFAULT_QUEUE_NAME,
             '',
             '38',
             messages.serialize(msg),
             '')
        )

        msgid = messages.send_schedule_request(socket, msg,
                                               interval_secs=92,
                                               unschedule=True)
        self.assertEqual(msgid, _msgid)

        snd_empq_msg_mock.assert_called_with(
            socket, 'UNSCHEDULE',
            (conf.DEFAULT_QUEUE_NAME,
             '',
             '92',
             messages.serialize(msg),
             '')
        )
