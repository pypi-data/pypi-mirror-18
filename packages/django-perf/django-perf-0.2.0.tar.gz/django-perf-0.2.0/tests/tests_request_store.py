import threading
from django.test import TestCase

from perf.request_store import RequestStore


class TestRequestStore(TestCase):

    def setUp(self):
        self.store = RequestStore()

    def test_add(self):
        self.store.add(1)
        self.store.add(2)
        self.store.add(3)
        assert self.store.get_all() == [1, 2, 3]

    def test_add_all(self):
        self.store.add_all([1, 2, 3])
        assert self.store.get_all() == [1, 2, 3]

    def test_get_all_with_blocking(self):
        t = threading.Timer(0.1, self._add_values, ())
        t.daemon = True
        t.start()
        assert self.store.get_all(True) == [1, 2, 3]

    def _add_values(self):
        self.store.add_all([1, 2, 3])
