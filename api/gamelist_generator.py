import os
import xml.etree.ElementTree as ET

class GamelistGenerator:
    def __init__(self, roms_dir: str, media_subdir: str = "media/images", output_filename: str = "gamelist.xml"):
        self.roms_dir = roms_dir
        self.media_subdir = media_subdir
        self.output_path = os.path.join(roms_dir, output_filename)

    def _validate(self):
        if not os.path.isdir(self.roms_dir):
            raise NotADirectoryError(f"'{self.roms_dir}' is not a valid directory.")

    def generate(self) -> str:
        self._validate()

        gamelist = ET.Element("gameList")

        for filename in sorted(os.listdir(self.roms_dir)):
            full_path = os.path.join(self.roms_dir, filename)

            if os.path.isfile(full_path):
                nome_jogo = os.path.splitext(filename)[0]

                game = ET.SubElement(gamelist, "game")

                ET.SubElement(game, "path").text = f"./{filename}"
                ET.SubElement(game, "name").text = nome_jogo
                ET.SubElement(game, "image").text = f"./{self.media_subdir}/{nome_jogo}.jpg"

        tree = ET.ElementTree(gamelist)
        tree.write(self.output_path, encoding="utf-8", xml_declaration=True)

        return self.output_path
