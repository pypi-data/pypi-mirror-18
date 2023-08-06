from datetime import datetime
from django.conf.urls import url
from django.http import HttpResponse
from django.test import TestCase
from django.urls import ResolverMatch
from middleware import PerfMiddleware
from mock import Mock
from mock import patch


def test_view(_):
    return HttpResponse("Test view")


def test_view_http401(_):
    return HttpResponse('Unauthorized', status=401)


urlpatterns = [
    url(r'^test-view/$', test_view, name='test-view'),
    url(r'^test-view-http401/$', test_view_http401, name='test-view-http401'),
]

class TestPerfMiddlewareRequest(TestCase):

    def setUp(self):
        self.middleware = PerfMiddleware()

    def test_process_request(self):
        request = Mock(path='/')
        request.method = 'GET'
        self.middleware.process_request(request)
        self.assertIsInstance(request._perf_request_time, datetime)

class TestPerfMiddlewareResponse(TestCase):

    def setUp(self):
        self.middleware = PerfMiddleware()

    @patch('perf.middleware.PerfNetwork')
    def test_process_response(self, mock_network):
        response = HttpResponse()
        request = Mock(path='/', META={})
        request._perf_request_time = datetime.now()
        request.resolver_match = Mock(kwargs={})
        processed = self.middleware.process_response(request, response)
        self.assertIsInstance(processed, HttpResponse)
        mock_network.send_requests.assert_called_once()

