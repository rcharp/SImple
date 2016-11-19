__author__ = 'Ricky'

import threading
import events

class eventThread(threading.Thread):
    def __init__(self, queue, list):
        threading.Thread.__init__(self)
        self.queue = queue
        self.list = list

    def run(self):
        while True:
            event = self.queue.get()
            events.process(event, self.list)
            self.queue.task_done()
