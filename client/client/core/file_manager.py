import os
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

    def get_all_files(self):
        return self.files

    def get_waiting_files(self):
        return [file for file in self.files if file.status == FileStatus.WAITING]

    def get_uploading_files(self):
        return [file for file in self.files if file.status == FileStatus.UPLOADING]

    def get_completed_files(self):
        return [file for file in self.files if file.status == FileStatus.COMPLETED]

    def get_error_files(self):
        return [file for file in self.files if file.status == FileStatus.ERROR]

    @staticmethod
    def resolve_filename_conflict(server_dir, filename):
        base, ext = os.path.splitext(filename)
        counter = 1
        new_filename = filename
        while os.path.exists(os.path.join(server_dir, new_filename)):
            new_filename = f"{base} ({counter}){ext}"
            counter += 1
        return new_filename
