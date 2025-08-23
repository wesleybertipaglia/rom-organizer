import os
import zlib
import zipfile
import xml.etree.ElementTree as ET

class MissingRomsChecker:
    def __init__(self, dat_file: str, roms_folder: str, output_file: str = None): # type: ignore
        self.dat_file = dat_file
        self.roms_folder = roms_folder

        default_name = "missing.md"
        if output_file:
            self.output_file = output_file.replace("_", "", 1).replace(".txt", ".md")
        else:
            self.output_file = os.path.join(roms_folder, default_name)

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

    def _classify_by_region(self, games):
        regions = {
            "World": [],
            "USA": [],
            "Europe": [],
            "Japan": [],
            "Taiwan": [],
            "Hong Kong": [],
            "Korea": [],
            "Asia": [],
            "China": [],
            "Others": []
        }

        for game in games:
            name_lower = game.lower()

            if "usa" in name_lower:
                regions["USA"].append(game)
            elif "europe" in name_lower or "eur" in name_lower:
                regions["Europe"].append(game)
            elif "japan" in name_lower or "jpn" in name_lower:
                regions["Japan"].append(game)
            elif "world" in name_lower:
                regions["World"].append(game)
            elif "asia" in name_lower:
                regions["Asia"].append(game)
            elif "taiwan" in name_lower:
                regions["Taiwan"].append(game)
            elif "hong kong" in name_lower:
                regions["Hong Kong"].append(game)
            elif "korea" in name_lower:
                regions["Korea"].append(game)
            elif "china" in name_lower:
                regions["China"].append(game)
            else:
                regions["Others"].append(game)

        return regions

    def _write_output(self):
        subset_tags = ["proto", "beta", "demo", "aftermarket", "rev", "v", "program"]

        main_set = []
        sub_sets = []

        for name in self.missing_roms.values():
            if any(tag in name.lower() for tag in subset_tags):
                sub_sets.append(name)
            else:
                main_set.append(name)

        main_by_region = self._classify_by_region(main_set)
        subs_by_region = self._classify_by_region(sub_sets)

        region_order = [
            "World", "USA", "Europe", "Japan", "Brazil", "Asia", "Taiwan", "Hong Kong",
            "Korea", "China", "Australia", "Russia", "Others"
        ]

        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write("# Missing Games\n\n")

            f.write("## Main Sets\n")
            for region in region_order:
                games = main_by_region.get(region, [])
                if games:
                    f.write(f"### {region}\n")
                    for game in sorted(games):
                        f.write(f"- {game}\n")
                    f.write("\n")

            f.write("## Sub Sets\n")
            for region in region_order:
                games = subs_by_region.get(region, [])
                if games:
                    f.write(f"### {region}\n")
                    for game in sorted(games):
                        f.write(f"- {game}\n")
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
