import time
import threading
from django.test import TestCase
from mock import patch

from perf.middleware import PerfRecorder


class TestPerfRecorder(TestCase):

    @patch('perf.recorder.PerfNetwork')
    @patch('perf.recorder.PerfRecorder._schedule_poll')
    @patch('perf.recorder.RequestStore')
    def test_recorder_sends_payload(self, mock_store, mock_poll, mock_network):
        self.recorder = PerfRecorder()
        self.recorder.store = mock_store
        self.recorder.network = mock_network
        mock_poll.assert_called_once()
        payload = {"test": "test"}
        self.recorder.add_request(payload)
        mock_store.add.assert_called_once_with(payload)
        mock_store.get_all.return_value = [payload]
        # Manually call send reqeuests to imitate thread
        self.recorder.send_requests()
        mock_network.send_requests.assert_called_once_with([payload])
