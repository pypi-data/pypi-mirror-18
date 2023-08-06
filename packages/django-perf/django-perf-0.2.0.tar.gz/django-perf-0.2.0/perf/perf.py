from django.conf import settings


class Perf(object):

    @staticmethod
    def get_api_key():
        perf_settings = getattr(settings, "PERF_CONFIG", None)
        if perf_settings != None:
            return perf_settings.get("api_key", None)
        return None

    @staticmethod
    def is_configured():
        return Perf.get_api_key() != None
