from cliengine.command import Command
from cli.types import CommandType
from api.file_compressor import FileCompressor

class FileCompressCommand(Command):
    def name(self):
        return "Compress Files"

    def type(self):
        return CommandType.FILE

    def run(self, *args, **kwargs):
        path = input("File or directory: ").strip()

        try:
            compressor = FileCompressor(path)
            result = compressor.compress()

            if not result["compressed"]:
                print("⚠️ No files were compressed.")
                return

            for idx, zip_path in enumerate(result["compressed"], start=1):
                print(f"{idx} 📦 Compressed: {zip_path}")

            print(f"\n✅ Total compressed: {len(result['compressed'])}")

        except Exception as e:
            print(f"❌ Error: {e}")
