import os
import shutil
import zlib
import xml.etree.ElementTree as ET

class RomRenamer:
    def __init__(self, dat_file: str, roms_folder: str, output_folder: str = None): # type: ignore
        self.dat_file = dat_file
        self.roms_folder = os.path.normpath(roms_folder)
        self.output_folder = os.path.normpath(output_folder) if output_folder else self._default_output_folder()
        self.in_place = self.roms_folder == self.output_folder
        self.crc_dict = {}

    def _default_output_folder(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(self.roms_folder))
        base_name = os.path.basename(os.path.normpath(self.roms_folder))
        return os.path.join(base_dir, f"{base_name}_corrected")

    def _validate_paths(self):
        if not os.path.isfile(self.dat_file):
            raise FileNotFoundError(f"DAT file not found: {self.dat_file}")
        if not os.path.isdir(self.roms_folder):
            raise NotADirectoryError(f"ROMs folder not found: {self.roms_folder}")

    def _parse_dat_file(self):
        tree = ET.parse(self.dat_file)
        root = tree.getroot()
        for game in root.findall("game"):
            for rom in game.findall("rom"):
                crc = rom.get("crc")
                name = rom.get("name")
                if crc and name:
                    self.crc_dict[crc.lower()] = name

    def _calc_crc32(self, filepath: str) -> str:
        with open(filepath, "rb") as f:
            data = f.read()
            return f"{zlib.crc32(data) & 0xffffffff:08x}"

    def run(self) -> dict:
        self._validate_paths()
        self._parse_dat_file()
        if not self.in_place:
            os.makedirs(self.output_folder, exist_ok=True)

        copied = 0
        skipped = 0
        unmatched = 0
        renamed_files = []

        for filename in os.listdir(self.roms_folder):
            filepath = os.path.join(self.roms_folder, filename)
            if not os.path.isfile(filepath):
                skipped += 1
                continue

            crc = self._calc_crc32(filepath)
            if crc in self.crc_dict:
                new_name = self.crc_dict[crc]
                dest_path = os.path.join(self.output_folder, new_name)

                if filepath == dest_path:
                    renamed_files.append((filename, new_name))
                    continue

                if self.in_place:
                    os.rename(filepath, dest_path)
                else:
                    shutil.copy2(filepath, dest_path)

                renamed_files.append((filename, new_name))
                copied += 1
            else:
                unmatched += 1

        return {
            "copied": copied,
            "skipped": skipped,
            "unmatched": unmatched,
            "output_folder": self.output_folder,
            "renamed_files": renamed_files,
        }
