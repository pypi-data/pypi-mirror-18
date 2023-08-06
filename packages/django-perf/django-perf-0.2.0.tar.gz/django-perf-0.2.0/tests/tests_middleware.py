from datetime import datetime
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponse
from django.test import TestCase
from mock import Mock
from mock import patch

from perf.middleware import PerfMiddleware


class TestPerfMiddleware(TestCase):

    def test_raises_middleware_not_used(self):
        with self.assertRaises(MiddlewareNotUsed):
            self.middleware = PerfMiddleware()

    @patch('perf.middleware.Perf')
    def test_can_initialize_middleware(self, mock_perf):
        mock_perf.is_configured.return_value = True
        self.middleware = PerfMiddleware()
        self.assertIsInstance(self.middleware, PerfMiddleware)


class TestPerfMiddlewareRequest(TestCase):

    def setUp(self):
        with patch('perf.middleware.Perf') as mock_perf:
            mock_perf.is_configured.return_value = True
            self.middleware = PerfMiddleware()

    def test_process_request(self):
        request = Mock(path='/')
        request.method = 'GET'
        self.middleware.process_request(request)
        self.assertIsInstance(request._perf_request_time, datetime)


class TestPerfMiddlewareResponse(TestCase):

    def setUp(self):
        with patch('perf.middleware.Perf') as mock_perf:
            mock_perf.is_configured.return_value = True
            self.middleware = PerfMiddleware()

    @patch('perf.middleware.PerfRecorder')
    def test_process_response(self, mock_recorder):
        self.middleware.recorder = mock_recorder
        response = HttpResponse()
        request = Mock(path='/', META={})
        request._perf_request_time = datetime.now()
        request.resolver_match = Mock(kwargs={})
        processed = self.middleware.process_response(request, response)
        self.assertIsInstance(processed, HttpResponse)
        mock_recorder.add_request.assert_called_once()

