from queue import Queue


class JobQueue:

    def __init__(self):

        self.queue = Queue()

    # -----------------------------------------------------

    def put(self, job):

        self.queue.put(job)

    # -----------------------------------------------------

    def get(self):

        return self.queue.get()

    # -----------------------------------------------------

    def empty(self):

        return self.queue.empty()

    # -----------------------------------------------------

    def size(self):

        return self.queue.qsize()

    # -----------------------------------------------------

    def clear(self):

        while not self.queue.empty():

            self.queue.get()