from collections import deque


class UploadQueue:

    def __init__(self, max_concurrent=3):
        self.queue = deque()
        self.max_concurrent = max_concurrent
        self.active_count = 0

    def add(self, file):
        self.queue.append(file)

    def add_many(self, files):
        for file in files:
            self.add(file)

    def get_next(self):
        if self.queue:
            return self.queue.popleft()

        return None

    def can_upload(self):
        return self.active_count < self.max_concurrent

    def start_upload(self):
        if self.can_upload():
            self.active_count += 1
            return True

        return False

    def finish_upload(self):
        if self.active_count > 0:
            self.active_count -= 1

    def size(self):
        return len(self.queue)
