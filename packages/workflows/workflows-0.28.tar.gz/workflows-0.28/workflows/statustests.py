from __future__ import absolute_import, division
import workflows.status
import mock
import pytest

@mock.patch('workflows.status.Queue')
@mock.patch('workflows.status.threading')
@mock.patch('workflows.status.time')
def test_status_advertiser_regularly_passes_status(mock_time, mock_threading, mock_queue):
  '''Check that the status advertiser calls a status function and passes the results on properly.'''
  sm = mock.Mock() # status mock
  tm = mock.Mock() # transport mock
  empty_exception = ZeroDivisionError # use 0-div-error as Queue-is-empty-exception
  mock_queue.Empty = empty_exception
  qm = mock_queue.Queue.return_value
  s = workflows.status.StatusAdvertise(interval=120, status_callback=sm, transport=tm)
  t = mock_threading.Thread.call_args[1]['target'] # target function
  mock_time.time.return_value = 100
  qm.get.side_effect = RuntimeError(mock.sentinel.pause)
  sm.return_value = mock.sentinel.status1

  # Run with a failing status function
  sm.side_effect = RuntimeError(mock.sentinel.status_error)
  with pytest.raises(RuntimeError) as excinfo:
    t()
  assert excinfo.value.message == mock.sentinel.pause

  qm.get.assert_called_once_with(True, 120)
  sm.assert_called_once()

  # Run with a working status function
  sm.side_effect = None
  with pytest.raises(RuntimeError) as excinfo:
    t()
  assert excinfo.value.message == mock.sentinel.pause

  assert qm.get.call_count == 2
  tm.broadcast_status.assert_called_once_with(mock.sentinel.status1)

  # Check that Queue-is-empty-exceptions lead to another status run
  qm.get.side_effect = [ empty_exception, RuntimeError(mock.sentinel.pause) ]
  with pytest.raises(RuntimeError) as excinfo:
    t()
  assert excinfo.value.message == mock.sentinel.pause
  assert tm.broadcast_status.call_count == 3
  assert qm.get.call_count == 4
  tm.broadcast_status.assert_called_with(mock.sentinel.status1)

  # Run after being stopped
  s.stop_and_wait()
  t() # this must no longer throw an exception

  assert sm.call_count == 5
  assert qm.get.call_count == 4
  assert tm.broadcast_status.call_count == 4
  tm.broadcast_status.assert_called_with(mock.sentinel.status1)

@mock.patch('workflows.status.Queue')
@mock.patch('workflows.status.threading')
@mock.patch('workflows.status.time')
def test_status_advertiser_can_run_without_status_function(mock_time, mock_threading, mock_queue):
  '''Check that the status advertiser can run without a status function.'''
  tm = mock.Mock() # transport mock
  qm = mock_queue.Queue.return_value
  s = workflows.status.StatusAdvertise(interval=120, transport=tm)
  t = mock_threading.Thread.call_args[1]['target'] # target function
  mock_time.time.return_value = 100
  qm.get.side_effect = RuntimeError(mock.sentinel.pause)

  # Run once
  with pytest.raises(RuntimeError) as excinfo:
    t()
  assert excinfo.value.message == mock.sentinel.pause

  qm.get.assert_called_once_with(True, 120)
  tm.broadcast_status.assert_called_once_with()

  # Run after being stopped
  s.stop_and_wait()
  t() # this must no longer throw an exception

  assert qm.get.call_count == 1
  assert tm.broadcast_status.call_count == 2

@mock.patch('workflows.status.Queue')
@mock.patch('workflows.status.threading')
@mock.patch('workflows.status.time')
def test_status_advertiser_external_triggering(mock_time, mock_threading, mock_queue):
  '''Check that the status advertiser can be triggered by external sources.'''
  sm = mock.Mock() # status mock
  tm = mock.Mock() # transport mock
  qm = mock_queue.Queue.return_value
  mock_threading.Queue.return_value = qm
  s = workflows.status.StatusAdvertise(interval=120, status_callback=sm, transport=tm)
  t = mock_threading.Thread.call_args[1]['target'] # target function

  s.trigger()
  qm.put.assert_called_once()

@mock.patch('workflows.status.Queue')
@mock.patch('workflows.status.threading')
def test_status_advertiser_sends_last_update_when_stopping(mock_threading, mock_queue):
  '''Check that the status advertiser sends a final update when shutting down.'''
  tm = mock.Mock() # transport mock
  qm = mock_queue.Queue.return_value
  mock_threading.Queue.return_value = qm
  s = workflows.status.StatusAdvertise(transport=tm)
  t = mock_threading.Thread.call_args[1]['target'] # target function
  qm.get.side_effect = RuntimeError(mock.sentinel.queue_read)
  qm.empty.return_value = False

  s.stop()

  t()
  tm.broadcast_status.assert_called_once()
