import logging
import requests

from perf import Perf


class PerfNetwork(object):
    PERF_INGEST_URL = "https://data.perf.sh/ingest"

    def __init__(self):
        self.api_key = Perf.get_api_key()
        self.logger = logging.getLogger(__name__)

    def send_requests(self, payload):
        if self.api_key != None:
            self.logger.info("Sending %d requests to Perf" % len(payload))
            requests.post(PerfNetwork.PERF_INGEST_URL, json=payload, headers=self.headers())

    def headers(self):
        return {
            "X-Perf-Public-API-Key": self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "PerfAgent-Django/0.2.0"
        }
