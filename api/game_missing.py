import os
import zlib
import zipfile
import xml.etree.ElementTree as ET

class MissingRomsChecker:
    def __init__(self, dat_file: str, roms_folder: str, output_file: str = None): # type: ignore
        self.dat_file = dat_file
        self.roms_folder = roms_folder
        self.output_file = output_file or os.path.join(roms_folder, "_missing.txt")
        self.expected_roms = {}
        self.found_crcs = set()
        self.missing_roms = {}

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
                    self.expected_roms[crc.lower()] = name

    def _calc_crc32(self, filepath):
        with open(filepath, "rb") as f:
            data = f.read()
            return f"{zlib.crc32(data) & 0xffffffff:08x}"

    def _scan_roms(self):
        for filename in os.listdir(self.roms_folder):
            filepath = os.path.join(self.roms_folder, filename)

            if not os.path.isfile(filepath):
                continue

            try:
                if filename.lower().endswith(".zip"):
                    with zipfile.ZipFile(filepath, 'r') as zipf:
                        for zipinfo in zipf.infolist():
                            with zipf.open(zipinfo) as file:
                                data = file.read()
                                crc = f"{zlib.crc32(data) & 0xffffffff:08x}"
                                self.found_crcs.add(crc)
                else:
                    crc = self._calc_crc32(filepath)
                    self.found_crcs.add(crc)
            except Exception:
                pass


    def _find_missing(self):
        self.missing_roms = {
            crc: name for crc, name in self.expected_roms.items() if crc not in self.found_crcs
        }

    def _write_output(self):
        subset_tags = ["proto", "beta", "demo", "aftermarket", "rev", "v", "progam"]

        main_set = []
        sub_sets = []

        for name in self.missing_roms.values():
            if any(tag in name.lower() for tag in subset_tags):
                sub_sets.append(name)
            else:
                main_set.append(name)

        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write("Games missing:\n")

            if main_set:
                f.write("\n-- main set --\n")
                for game in main_set:
                    f.write(f"{game}\n")
                f.write("\n")

            if sub_sets:
                f.write("\n-- sub sets --\n")
                for game in sub_sets:
                    f.write(f"{game}\n")
                f.write("\n")

    def run(self) -> dict:
        self._validate_paths()
        self._parse_dat_file()
        self._scan_roms()
        self._find_missing()
        self._write_output()

        return {
            "output_file": self.output_file,
            "total_expected": len(self.expected_roms),
            "found": len(self.found_crcs),
            "missing": len(self.missing_roms),
            "missing_roms": list(self.missing_roms.values())
        }
