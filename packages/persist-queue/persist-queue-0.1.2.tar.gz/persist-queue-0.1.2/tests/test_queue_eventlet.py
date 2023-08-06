# coding=utf-8

import eventlet
eventlet.monkey_patch() # noqa

import shutil
import tempfile
import unittest
from threading import Thread

from persistqueue import Queue, Empty


class PersistEventletTest(unittest.TestCase):
    def setUp(self):
        self.path = tempfile.mkdtemp(suffix='persistqueue_event')

    def tearDown(self):
        shutil.rmtree(self.path, ignore_errors=True)

    def test_multi_threaded(self):
        """Create consumer and producer threads, check parallelism"""

        q = Queue(self.path)

        def producer():
            for i in range(1000):
                q.put('var%d' % i)

        def consumer():
            for i in range(1000):
                q.get()
                q.task_done()

        c = Thread(target=consumer)
        c.start()
        p = Thread(target=producer)
        p.start()
        c.join()
        p.join()
        with self.assertRaises(Empty):
            q.get_nowait()
