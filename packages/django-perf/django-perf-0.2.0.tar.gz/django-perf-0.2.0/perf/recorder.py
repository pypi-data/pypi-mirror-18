import logging
import threading

from requests import ConnectionError

from network import PerfNetwork
from request_store import RequestStore


class PerfRecorder(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.network = PerfNetwork()
        self.store = RequestStore()
        self._schedule_poll()

    def add_request(self, request):
        self.store.add(request)

    def send_requests(self):
        self.logger.debug("Polling for pending requests")
        requests = self.store.get_all(True)
        try:
            self.network.send_requests(requests)
        except ConnectionError as e:
            self.logger.error(e)
            self.store.add_all(requests)
        self._schedule_poll()

    def _schedule_poll(self):
        t = threading.Timer(1.0, self.send_requests, ())
        t.daemon = True
        t.start()
