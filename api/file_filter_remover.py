import os
from typing import List

class FilteredRemover:
    def __init__(self, folder: str, filters: List[str]):
        self.folder = os.path.normpath(folder)
        self.filters = [f.lower() for f in filters]

    def remove(self) -> dict:
        removed_files = []
        errors = []

        for root, _, files in os.walk(self.folder):
            for file in files:
                filename_lower = file.lower()
                if any(filt in filename_lower for filt in self.filters):
                    full_path = os.path.join(root, file)
                    try:
                        os.remove(full_path)
                        removed_files.append(full_path)
                    except Exception as e:
                        errors.append((full_path, str(e)))

        return {"removed": removed_files, "errors": errors}
