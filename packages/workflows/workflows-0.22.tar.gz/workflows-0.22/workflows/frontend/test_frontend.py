from __future__ import absolute_import, division
from workflows.services.common_service import CommonService
import workflows.frontend
import mock

@mock.patch('workflows.frontend.multiprocessing')
@mock.patch('workflows.frontend.workflows.status.StatusAdvertise')
@mock.patch('workflows.frontend.workflows.transport')
def test_frontend_connects_to_transport_layer(mock_transport, mock_status, mock_mp):
  '''Frontend should call connect method on transport layer module and subscribe to a unique command queue.'''
  workflows.frontend.Frontend()
  mock_transport.lookup.assert_called_once_with(None)
  mock_transport.lookup.return_value.assert_called_once_with()
  mock_transport.lookup.return_value.return_value.connect.assert_called_once_with()

  workflows.frontend.Frontend(transport="some_transport")
  mock_transport.lookup.assert_called_with("some_transport")

  mock_trn = mock.Mock()
  workflows.frontend.Frontend(mock_trn)
  mock_trn.assert_called_once_with()
  mock_trn.return_value.connect.assert_called_once_with()

@mock.patch('workflows.frontend.workflows.status.StatusAdvertise')
@mock.patch('workflows.frontend.workflows.transport')
def test_frontend_subscribes_to_command_channel(mock_transport, mock_status):
  '''Frontend should call connect method on transport layer module and subscribe to a unique command queue.'''
  transport = mock_transport.lookup.return_value.return_value
  fe = workflows.frontend.Frontend()
  mock_transport.lookup.assert_called_once_with(None)
  transport.connect.assert_called_once()
  transport.subscribe.assert_not_called()

  fe = workflows.frontend.Frontend(transport_command_prefix='sentinel.')
  transport.subscribe.assert_called_once()
  assert transport.subscribe.call_args == (('sentinel.' + fe.get_host_id(), mock.ANY), {})
  callbackfn = transport.subscribe.call_args[0][1]

  assert fe.shutdown == False
  callbackfn({}, { 'command': 'shutdown' })
  assert fe.shutdown == True

@mock.patch('workflows.frontend.multiprocessing')
@mock.patch('workflows.frontend.workflows.status.StatusAdvertise')
@mock.patch('workflows.frontend.workflows.transport')
def test_start_service_in_frontend(mock_transport, mock_status, mock_mp):
  '''Check that the service is being run and connected to the frontend properly via the correct pipes,
     and the status advertiser is being started in the background.'''
  mock_service = mock.Mock()
  mock_mp.Pipe.side_effect = [
      (mock.sentinel.pipe1, mock.sentinel.pipe2),
      (mock.sentinel.pipe3, mock.sentinel.pipe4),
      None ]

  # initialize frontend
  fe = workflows.frontend.Frontend()

  # check status information is being broadcast
  mock_status.assert_called_once()
  mock_status.return_value.start.assert_called_once()

  # start service
  fe.switch_service(mock_service)

  # check service was started properly
  mock_service.assert_called_once_with(commands=mock.sentinel.pipe2, frontend=mock.sentinel.pipe3)
  mock_mp.Process.assert_called_once_with(target=mock_service.return_value.start, args=())
  mock_mp.Process.return_value.start.assert_called_once()

@mock.patch('workflows.frontend.workflows.status.StatusAdvertise')
@mock.patch('workflows.frontend.workflows.transport')
def test_get_frontend_status(mock_transport, mock_status):
  '''Check that the get_status-method works and contains the correct host-id.'''
  fe = workflows.frontend.Frontend()
  status = fe.get_status()
  assert status['host'] == fe.get_host_id()

@mock.patch('workflows.frontend.workflows.status.StatusAdvertise')
def test_connect_queue_communication_to_transport_layer(mock_status):
  '''Check that communication messages coming in from the service layer via the Queue are
     passed correctly to the transport layer and vice versa in the other direction.'''
  transport = mock.Mock()
  commqueue = mock.Mock()

  fe = workflows.frontend.Frontend(transport=transport)
  setattr(fe, '_pipe_commands', commqueue)

  transport.assert_called_once()
  transport = transport.return_value
  transport.connect.assert_called_once()

  fe.parse_band_transport( {
      'call': 'send',
      'payload': (
        ( mock.sentinel.channel, mock.sentinel.message ),
        {}
      )
    } )
  transport.send.assert_called_once_with(mock.sentinel.channel,
                                         mock.sentinel.message)

  fe.parse_band_transport( {
      'call': 'subscribe',
      'payload': (
        ( mock.sentinel.subid, mock.sentinel.channel, mock.sentinel.something ),
        { 'kwarg': mock.sentinel.kwarg }
      )
    } )
  transport.subscribe.assert_called_once_with(
    mock.sentinel.channel,
    mock.ANY,
    mock.sentinel.something, kwarg=mock.sentinel.kwarg
    )
  callback_function = transport.subscribe.call_args[0][1]

  callback_function(mock.sentinel.header, mock.sentinel.message)
  commqueue.send.assert_called_once_with( {
      'band': 'transport_message',
      'payload': {
          'subscription_id': mock.sentinel.subid,
          'header': mock.sentinel.header,
          'message': mock.sentinel.message,
        }
    } )

class CrashServiceOnInit(CommonService):
  '''A service that crashes python 2.7 with a segmentation fault.'''
  def initializing(self):
    '''Crash.'''
    self._register_idle(1, self.kill_service)
#    import ctypes
#    ctypes.string_at(1)
#   Python 2
#   from types import CodeType as code
#   exec type((lambda:0).func_code)(0,1,0,0,'Q',(),(),(),'','',0,'')
#   Python 3
#   exec(type((lambda:0).__code__)(0,1,0,0,0,b'',(),(),(),'','',1,b''))

  def kill_service(self):
    '''Raise exception in case the segmentation fault code above does not work.
       This should set the error state, kill the service and cause the frontend
       to leave its main loop.'''
    assert False, "Segfault test failing"

@mock.patch('workflows.frontend.workflows.status.StatusAdvertise')
def test_frontend_can_handle_service_segfaults(mock_status):
  '''Check that the get_status-method works and contains the correct host-id.'''
  return
  transport = mock.Mock()

  fe = workflows.frontend.Frontend(transport=transport, service=CrashServiceOnInit)

  transport = transport.return_value
  transport.connect.assert_called_once()

  fe.run()

  return

  status = fe.get_status()
  assert status['host'] == fe.get_host_id()

  '''Check that communication messages coming in from the service layer via the Queue are
     passed correctly to the transport layer and vice versa in the other direction.'''
  fe.parse_band_transport( {
      'call': 'send',
      'payload': (
        ( mock.sentinel.channel, mock.sentinel.message ),
        {}
      )
    } )
  transport.send.assert_called_once_with(mock.sentinel.channel,
                                         mock.sentinel.message)

  fe.parse_band_transport( {
      'call': 'subscribe',
      'payload': (
        ( mock.sentinel.subid, mock.sentinel.channel, mock.sentinel.something ),
        { 'kwarg': mock.sentinel.kwarg }
      )
    } )
  transport.subscribe.assert_called_once_with(
    mock.sentinel.channel,
    mock.ANY,
    mock.sentinel.something, kwarg=mock.sentinel.kwarg
    )
  callback_function = transport.subscribe.call_args[0][1]

  callback_function(mock.sentinel.header, mock.sentinel.message)
  commqueue.send.assert_called_once_with( {
      'band': 'transport_message',
      'payload': {
          'subscription_id': mock.sentinel.subid,
          'header': mock.sentinel.header,
          'message': mock.sentinel.message,
        }
    } )
