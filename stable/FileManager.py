import os
from Log import Log

class FileManager:
    def __init__(self):
        Log.print("Initializing FileManager..")
        self.folder_path = "data"

    def set_folder_path(self, path):
        self.folder_path = path
    
    def create_file(self, file_name, content="", flag="w"):
        file_path = os.path.join(self.folder_path, file_name)
        with open(file_path, flag) as f:
            f.write(content)
    
    def edit_file(self, file_name, new_content, flag="w"):
        file_path = os.path.join(self.folder_path, file_name)
        with open(file_path, flag) as f:
            f.write(new_content)
    
    def read_file(self, file_name, flag="r"):
        file_path = os.path.join(self.folder_path, file_name)
        with open(file_path, flag) as f:
            content = f.read()
        return content
    
    def save_file(self, file_name, content, flagIfExists="a", flagIfNotExists="w"):
        file_path = os.path.join(self.folder_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, flagIfExists) as f:
                f.write(content)
        else:
            with open(file_path, flagIfNotExists) as f:
                f.write(content)

    def read_file_lines(self, file_name, flag="r"):
        file_path = os.path.join(self.folder_path, file_name)
        with open(file_path, flag) as f:
            lines = f.readlines()
        return lines

    def read_file_delimited(self, file_name, delimiter=","):
        lines = self.read_file_lines(file_name)
        parts_list = []
        for line in lines:
            parts = line.strip().split(delimiter)
            parts_list.append(parts)
        return parts_list