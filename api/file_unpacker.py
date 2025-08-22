import os
import zipfile
import rarfile
import py7zr
import shutil

class FileUnpacker:
    def __init__(self, folder_path: str, delete_archives: bool = True):
        self.folder_path = os.path.normpath(folder_path)
        self.delete_archives = delete_archives
        self.unpacked = []
        self.errors = []

    def _unpack_zip(self, filepath):
        try:
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(os.path.dirname(filepath))
            return True
        except Exception as e:
            self.errors.append((filepath, str(e)))
            return False

    def _unpack_7z(self, filepath):
        try:
            with py7zr.SevenZipFile(filepath, mode='r') as archive:
                archive.extractall(path=os.path.dirname(filepath))
            return True
        except Exception as e:
            self.errors.append((filepath, str(e)))
            return False

    def _unpack_rar(self, filepath):
        try:
            with rarfile.RarFile(filepath, 'r') as rar_ref:
                rar_ref.extractall(path=os.path.dirname(filepath))
            return True
        except Exception as e:
            self.errors.append((filepath, str(e)))
            return False

    def unpack_all(self) -> dict:
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                filepath = os.path.join(root, file)
                ext = file.lower().split('.')[-1]

                unpacked_successfully = False

                if ext == "zip":
                    unpacked_successfully = self._unpack_zip(filepath)
                elif ext == "7z":
                    unpacked_successfully = self._unpack_7z(filepath)
                elif ext == "rar":
                    unpacked_successfully = self._unpack_rar(filepath)

                if unpacked_successfully:
                    self.unpacked.append(filepath)
                    if self.delete_archives:
                        try:
                            os.remove(filepath)
                        except Exception as e:
                            self.errors.append((filepath, f"Erro ao deletar: {e}"))

        return {
            "unpacked": self.unpacked,
            "errors": self.errors
        }
