from cliengine.command import Command
from cli.types import CommandType

import os
import zlib
import shutil
import xml.etree.ElementTree as ET
from cli.dat import choose_dat_file

class CorrectRomsNamesByDatCommand(Command):
    def __init__(self):
        pass

    def name(self) -> str:
        return "Correct ROMs Names using DAT file (Copy to _corrected folder)"

    def type(self):
        return CommandType.RENAMER

    def run(self, *args, **kwargs):
        dat_file = choose_dat_file()
        if not dat_file:
            return

        roms_folder = input("📁 Enter path to ROMs folder: ").strip()

        if not os.path.isfile(dat_file):
            print(f"❌ Error: DAT file not found: {dat_file}")
            return
        if not os.path.isdir(roms_folder):
            print(f"❌ Error: ROMs folder not found: {roms_folder}")
            return

        base_dir = os.path.dirname(os.path.abspath(roms_folder))
        base_name = os.path.basename(os.path.normpath(roms_folder))
        output_folder = os.path.join(base_dir, f"{base_name}_corrected")

        os.makedirs(output_folder, exist_ok=True)

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

            copied = 0
            skipped = 0
            unmatched = 0

            for filename in os.listdir(roms_folder):
                filepath = os.path.join(roms_folder, filename)
                if os.path.isfile(filepath):
                    crc = calc_crc32(filepath)
                    if crc in crc_dict:
                        new_name = crc_dict[crc]
                        dest_path = os.path.join(output_folder, new_name)
                        shutil.copy2(filepath, dest_path)
                        print(f"✔ {filename} -> {new_name}")
                        copied += 1
                    else:
                        print(f"✘ No match for {filename}")
                        unmatched += 1
                else:
                    skipped += 1

            print("\n✅ Copy Summary:")
            print(f" • Copied and renamed: {copied}")
            print(f" • Skipped non-files: {skipped}")
            print(f" • No match: {unmatched}")
            print(f"📂 Output folder: {output_folder}")

        except Exception as e:
            print(f"❌ Error: {e}")
