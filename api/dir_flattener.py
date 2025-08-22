import os
import shutil

class DirectoryFlattener:
    def __init__(self, root_dir: str):
        self.root_dir = os.path.normpath(root_dir)
        self.files_moved = 0
        self.move_log = []

    def _validate(self):
        if not os.path.exists(self.root_dir):
            raise FileNotFoundError("Path does not exist.")
        if os.path.isfile(self.root_dir):
            raise NotADirectoryError("Path is a file. Please provide a directory.")

    def flatten(self) -> dict:
        self._validate()
        index = 1

        for current_dir, _, files in os.walk(self.root_dir):
            if current_dir == self.root_dir:
                continue

            for file in files:
                src = os.path.join(current_dir, file)
                dst = os.path.join(self.root_dir, file)

                if os.path.exists(dst):
                    name, ext = os.path.splitext(file)
                    i = 1
                    while os.path.exists(dst):
                        new_name = f"{name}_{i}{ext}"
                        dst = os.path.join(self.root_dir, new_name)
                        i += 1

                shutil.move(src, dst)
                self.files_moved += 1
                self.move_log.append((index, file, dst))
                index += 1

        return {
            "files_moved": self.files_moved,
            "move_log": self.move_log
        }
