import configparser

import xml.etree.ElementTree as ET
class Config:
    def __init__(self):
        self.find_config()
        self.read_config()

    def read_config(self):
        tree = ET.parse(self.configPath)
        root = tree.getroot()

        self.sys_prompt_info = root[2].text
        self.sys_prompt_rp = root[1].text
        self.character = root[0].text
        self.wiki_init = self.get_wiki_init()

    def find_config(self):
        self.configPath = "rp.xml"
        self.wikiInitPath = "pre_data.txt"

    def get_wiki_init(self):
        with open(self.wikiInitPath, "rb") as f:
            return f.read()

    def generate_config(self):
        try:
            self.configPath = 'config.xml'
            file = open(self.configPath, 'wr')
            file.write(self.config_template)
            file.close()
        except PermissionError as e:
            raise RuntimeError
        

if __name__ == "__main__":
    conf = Config()