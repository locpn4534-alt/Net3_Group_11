from .file_item import FileItem, FileStatus


class FileManager:

    def __init__(self):
        self.files = []

    def add_file(self, path):
        file = FileItem(path)
        self.files.append(file)
        return file

    def add_files(self, paths):
        added_files = []

        for path in paths:
            file = self.add_file(path)
            added_files.append(file)

        return added_files

    def remove_file(self, file):
        if file in self.files:
            self.files.remove(file)

    def clear(self):
        self.files.clear()

    def get_waiting_files(self):
        return [
            file for file in self.files
            if file.status == FileStatus.WAITING
        ]

    def get_all_files(self):
        return self.files
