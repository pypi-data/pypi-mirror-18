from datetime import datetime
from network import PerfNetwork

class PerfMiddleware(object):
    PERF_INGEST_URL = "https://data.perf.sh/ingest"

    def process_request(self, request):
        request._perf_request_time = datetime.now()

    def process_response(self, request, response):
        response_time = datetime.now() - request._perf_request_time
        payload = [{
            "request_url": request.build_absolute_uri(),
            "request_method": request.method,
            "status_code": response.status_code,
            "time_in_millis": int(round(response_time.microseconds / 1000, 0)),
            "normalized_uri": self.build_normalized_uri(request)
        }]
        PerfNetwork.send_requests(payload)
        return response

    def build_normalized_uri(self, request):
        normalized_uri = request.path
        for key, value in request.resolver_match.kwargs.iteritems():
            return normalized_uri.replace(value, ":%s" % key, 1)
        return normalized_uri
