from cliengine.command import Command
from api.command_type import CommandType
from api.dat_loader import choose_dat_file

from api.game_renamer import RomRenamer
from api.game_missing import MissingRomsChecker
from api.game_list import GamelistGenerator
from api.file_compressor import FileCompressor
from api.dir_flattener import DirectoryFlattener
from api.file_unpacker import FileUnpacker
from api.file_filter_remover import FilteredRemover

import os
import shutil

class AutoRunCommand(Command):
    def name(self) -> str:
        return "🛠 Auto Run: Fully Organize ROMs"

    def type(self):
        return CommandType.PIPELINE

    def run(self, *args, **kwargs):
        print("⚠️  This process will reorganize your ROMs through multiple steps.")
        print("📂 Original files will not be modified directly.")
        input("Press Enter to continue...")

        dat_file = choose_dat_file()
        if not dat_file:
            return

        roms_folder = input("📁 Path to your ROMs folder: ").strip()

        print("❓ Which types of ROMs do you want to remove?")
        print("   [Proto, Beta, Demo, Aftermarket, Rev]")
        filter_input = input("Separate by comma (or leave blank to skip): ").strip()
        filters = [f.strip() for f in filter_input.split(",") if f.strip()] if filter_input else []

        base_dir = os.path.dirname(os.path.abspath(roms_folder))
        corrected_folder = os.path.join(base_dir, f"{os.path.basename(roms_folder)}_corrected")

        if os.path.exists(corrected_folder):
            print(f"⚠️  Folder '{corrected_folder}' already exists. Using it.")
        else:
            shutil.copytree(roms_folder, corrected_folder)
            print(f"✅ Folder copied to '{corrected_folder}'")

        print("📦 Unpacking files...")
        unpacker = FileUnpacker(corrected_folder)
        unpack_result = unpacker.unpack_all()
        print(f"✔ Files unpacked: {len(unpack_result['unpacked'])}")
        if unpack_result["errors"]:
            print(f"⚠️  {len(unpack_result['errors'])} errors while unpacking.")

        print("📁 Flattening directory structure...")
        flattener = DirectoryFlattener(corrected_folder)
        flatten_result = flattener.flatten()
        print(f"✔ Files moved: {flatten_result['files_moved']}")

        if filters:
            print(f"🧹 Removing files with filters: {', '.join(filters)}")
            remover = FilteredRemover(corrected_folder, filters)
            remove_result = remover.remove()
            print(f"✔ Files removed: {len(remove_result['removed'])}")
            if remove_result["errors"]:
                print(f"⚠️  {len(remove_result['errors'])} errors while removing files.")

        print("🔄 Renaming files...")
        renamer = RomRenamer(dat_file, corrected_folder, corrected_folder)
        rename_result = renamer.run()
        print(f"✔ Files renamed: {rename_result['copied']}, not matched: {rename_result['unmatched']}")

        print("📋 Checking for missing ROMs...")
        checker = MissingRomsChecker(dat_file, corrected_folder)
        missing_result = checker.run()
        print(f"✔ Found: {missing_result['found']}, Missing: {missing_result['missing']}")
        print(f"📄 Missing list saved at: {missing_result['output_file']}")

        print("📦 Compressing files...")
        compressor = FileCompressor(corrected_folder, delete_originals=True)
        compress_result = compressor.compress()
        print(f"✔ Files compressed: {len(compress_result['compressed'])}")

        print("🗂 Generating gamelist.xml...")
        gamelist = GamelistGenerator(corrected_folder)
        gamelist_path = gamelist.generate()
        print(f"✔ Gamelist saved at: {gamelist_path}")

        print("\n✅ Process completed successfully!")
        print(f"📂 Final folder: {corrected_folder}")
        print(f"🗃 Total games organized: {rename_result['copied']}")
        print(f"📄 Missing list: {missing_result['output_file']}")
