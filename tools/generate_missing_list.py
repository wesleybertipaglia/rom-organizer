from cliengine.command import Command
from cli.types import CommandType

import os
import zlib
import xml.etree.ElementTree as ET
from cli.dat import choose_dat_file

class CheckMissingRomsCommand(Command):
    def __init__(self):
        pass

    def name(self) -> str:
        return "Check Missing ROMs from DAT"

    def type(self):
        return CommandType.GAMELIST

    def run(self, *args, **kwargs):
        dat_file = choose_dat_file()
        if not dat_file:
            return

        roms_folder = input("📁 Enter path to ROMs folder: ").strip()
        missing_file = input("📝 Enter path to save missing list (e.g., faltando.txt): ").strip()

        if not os.path.isfile(dat_file):
            print(f"❌ Error: DAT file not found at: {dat_file}")
            return

        if not os.path.isdir(roms_folder):
            print(f"❌ Error: ROMs folder not found at: {roms_folder}")
            return

        try:
            tree = ET.parse(dat_file)
            root = tree.getroot()

            expected_roms = {}
            for game in root.findall("game"):
                for rom in game.findall("rom"):
                    crc = rom.get("crc")
                    name = rom.get("name")
                    if crc and name:
                        expected_roms[crc.lower()] = name

            have_crcs = set()

            def calc_crc32(filepath):
                with open(filepath, "rb") as f:
                    data = f.read()
                    return f"{zlib.crc32(data) & 0xffffffff:08x}"

            for filename in os.listdir(roms_folder):
                filepath = os.path.join(roms_folder, filename)
                if os.path.isfile(filepath):
                    crc = calc_crc32(filepath)
                    have_crcs.add(crc)

            missing = {crc: name for crc, name in expected_roms.items() if crc not in have_crcs}

            with open(missing_file, "w", encoding="utf-8") as f:
                f.write("Jogos faltando:\n\n")
                for name in missing.values():
                    f.write(f"{name}\n")

            print(f"\n✅ Missing ROMs list saved to: {missing_file}")
            print(f"📦 Total expected: {len(expected_roms)}")
            print(f"📂 Found: {len(have_crcs)}")
            print(f"❗ Missing: {len(missing)}")

        except Exception as e:
            print(f"❌ Error while checking ROMs: {e}")
