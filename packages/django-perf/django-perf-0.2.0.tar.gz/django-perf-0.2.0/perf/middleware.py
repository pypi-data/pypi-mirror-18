from datetime import datetime
from django.core.exceptions import MiddlewareNotUsed

from recorder import PerfRecorder
from perf import Perf

class PerfMiddleware(object):

    def __init__(self):
        if Perf.is_configured():
            self.recorder = PerfRecorder()
        else:
            raise MiddlewareNotUsed()

    def process_request(self, request):
        request._perf_request_time = datetime.now()

    def process_response(self, request, response):
        response_time = datetime.now() - request._perf_request_time
        payload = {
            "request_url": request.build_absolute_uri(),
            "request_method": request.method,
            "status_code": response.status_code,
            "time_in_millis": int(round(response_time.microseconds / 1000, 0)),
            "normalized_uri": self._build_normalized_uri(request)
        }
        self.recorder.add_request(payload)
        return response

    def _build_normalized_uri(self, request):
        normalized_uri = request.path
        for key, value in request.resolver_match.kwargs.iteritems():
            return normalized_uri.replace(value, ":%s" % key, 1)
        return normalized_uri
