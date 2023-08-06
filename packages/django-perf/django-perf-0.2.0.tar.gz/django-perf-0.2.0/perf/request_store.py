import threading


class RequestStore(object):
    def __init__(self):
        self.cond = threading.Condition()
        self.requests = []

    def add_all(self, requests):
        with self.cond:
            self.requests.extend(requests)
            self.cond.notify() # Wake 1 thread waiting on cond (if any)

    def add(self, request):
        with self.cond:
            self.requests.append(request)
            self.cond.notify() # Wake 1 thread waiting on cond (if any)

    def get_all(self, blocking=False):
        with self.cond:
            # If blocking is true, always return at least 1 item
            while blocking and len(self.requests) == 0:
                self.cond.wait()
            requests, self.requests = self.requests, []
        return requests
