import os
import zipfile

class FileCompressor:
    def __init__(self, path: str, delete_originals: bool = True, ignore_exts: list[str] = None): # type: ignore
        self.path = os.path.normpath(path)
        self.delete_originals = delete_originals
        self.ignore_exts = ignore_exts or [".zip", ".rar", ".7z", ".txt", ".xml", ".log", ".bak", ".html", ".json"]
        self.compressed_files = []

    def compress(self) -> dict:
        if os.path.isfile(self.path):
            zip_path = self._compress_single_file(self.path)
            return {
                "type": "file",
                "compressed": [zip_path],
                "success": True
            }

        elif os.path.isdir(self.path):
            compressed = self._compress_all_in_directory(self.path)
            return {
                "type": "directory",
                "compressed": compressed,
                "success": True
            }

        else:
            raise FileNotFoundError(f"'{self.path}' is not a valid file or directory.")

    def _compress_single_file(self, file_path: str) -> str:
        dir_name = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        zip_name = os.path.splitext(file_name)[0] + ".zip"
        zip_path = os.path.join(dir_name, zip_name)

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path, arcname=file_name)

        if self.delete_originals:
            os.remove(file_path)

        self.compressed_files.append(zip_path)
        return zip_path

    def _compress_all_in_directory(self, folder_path: str) -> list:
        items = os.listdir(folder_path)
        if not items:
            raise FileNotFoundError("No items found in the directory.")

        for item in items:
            item_path = os.path.join(folder_path, item)
        
            item_lower = item.lower()

            if item_lower == "missing.md":
                continue

            if any(item_lower.endswith(ext) for ext in self.ignore_exts):
                continue

            zip_name = os.path.splitext(item)[0] + ".zip"
            zip_path = os.path.join(folder_path, zip_name)

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if os.path.isfile(item_path):
                    zipf.write(item_path, arcname=item)
                elif os.path.isdir(item_path):
                    for sub_item in os.listdir(item_path):
                        sub_item_path = os.path.join(item_path, sub_item)
                        arcname = os.path.join(item, sub_item)
                        if os.path.isfile(sub_item_path):
                            zipf.write(sub_item_path, arcname=arcname)

            if self.delete_originals:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    try:
                        os.rmdir(item_path)
                    except OSError:
                        pass

            self.compressed_files.append(zip_path)

        return self.compressed_files
