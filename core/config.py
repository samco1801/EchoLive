import json


class Config:

    def __init__(self):

        with open("config/config.json", "r", encoding="utf-8") as file:
            self.data = json.load(file)

    def get(self, key):

        return self.data.get(key)

    def get_section(self, section):

        return self.data.get(section, {})