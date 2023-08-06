from perf import Perf
import requests

class PerfNetwork(object):
    PERF_INGEST_URL = "https://data.perf.sh/ingest"

    @staticmethod
    def send_requests(payload):
        api_key = Perf.get_api_key()
        if api_key != None:
            headers = {
                "X-Perf-Public-API-Key": api_key,
                "Content-Type": "application/json",
                "User-Agent": "PerfAgent-Django/0.1.2"
            }
            requests.post(PerfNetwork.PERF_INGEST_URL, json=payload, headers=headers)
