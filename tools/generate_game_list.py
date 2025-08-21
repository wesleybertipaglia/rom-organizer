from cliengine.command import Command
from cli.types import CommandType
import os
import xml.etree.ElementTree as ET

class GenerateGamelistCommand(Command):
    def __init__(self):
        pass

    def name(self) -> str:
        return "Generate Gamelist XML"

    def type(self):
        return CommandType.GAMELIST

    def run(self, *args, **kwargs):
        roms_dir = input("📁 Enter ROMs folder path: ").strip()

        if not os.path.isdir(roms_dir):
            print(f"❌ Error: '{roms_dir}' is not a valid directory.")
            return

        try:
            gamelist = ET.Element("gameList")

            for filename in sorted(os.listdir(roms_dir)):
                full_path = os.path.join(roms_dir, filename)

                if os.path.isfile(full_path):
                    nome_jogo = os.path.splitext(filename)[0]

                    game = ET.SubElement(gamelist, "game")

                    path = ET.SubElement(game, "path")
                    path.text = f"./{filename}"

                    name = ET.SubElement(game, "name")
                    name.text = nome_jogo

                    image = ET.SubElement(game, "image")
                    image.text = f"./media/images/{nome_jogo}.jpg"

            output_path = os.path.join(roms_dir, "gamelist.xml")
            tree = ET.ElementTree(gamelist)
            tree.write(output_path, encoding="utf-8", xml_declaration=True)

            print(f"✅ gamelist.xml generated successfully at: {output_path}")

        except Exception as e:
            print(f"❌ Error generating gamelist: {e}")
