from cliengine.command import Command
from cli.types import CommandType

import os
import zlib
import xml.etree.ElementTree as ET

class RenameRomsByDatCommand(Command):
    def __init__(self):
        pass

    def name(self) -> str:
        return "Rename ROMs using DAT file"

    def type(self):
        return CommandType.RENAMER

    def run(self, *args, **kwargs):
        dat_file = input("📄 Enter path to DAT file: ").strip()
        roms_folder = input("📁 Enter path to ROMs folder: ").strip()

        if not os.path.isfile(dat_file):
            print(f"❌ Error: DAT file not found: {dat_file}")
            return
        if not os.path.isdir(roms_folder):
            print(f"❌ Error: ROMs folder not found: {roms_folder}")
            return

        try:
            tree = ET.parse(dat_file)
            root = tree.getroot()

            crc_dict = {}
            for game in root.findall("game"):
                for rom in game.findall("rom"):
                    crc = rom.get("crc")
                    name = rom.get("name")
                    if crc and name:
                        crc_dict[crc.lower()] = name

            def calc_crc32(filepath):
                with open(filepath, "rb") as f:
                    data = f.read()
                    return f"{zlib.crc32(data) & 0xffffffff:08x}"

            renamed = 0
            skipped = 0
            unmatched = 0

            for filename in os.listdir(roms_folder):
                filepath = os.path.join(roms_folder, filename)
                if os.path.isfile(filepath):
                    crc = calc_crc32(filepath)
                    if crc in crc_dict:
                        new_name = crc_dict[crc]
                        new_path = os.path.join(roms_folder, new_name)
                        if filename != new_name:
                            os.rename(filepath, new_path)
                            print(f"✔ {filename} -> {new_name}")
                            renamed += 1
                        else:
                            print(f"= {filename} is already correctly named.")
                            skipped += 1
                    else:
                        print(f"✘ No match for {filename}")
                        unmatched += 1

            print("\n✅ Rename Summary:")
            print(f" • Renamed: {renamed}")
            print(f" • Already correct: {skipped}")
            print(f" • No match: {unmatched}")

        except Exception as e:
            print(f"❌ Error: {e}")
