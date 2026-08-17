from core.file_manager import FileManager


manager = FileManager()

manager.add_file("test1.txt")
manager.add_file("test2.pdf")
manager.add_file("test3.zip")

for file in manager.get_all_files():
    print(file.name)
    print(file.status)
