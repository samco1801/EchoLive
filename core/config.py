import json

CONFIG_PATH = "config/config.json"


class Config:

    def __init__(self):

        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            self.data = json.load(file)

    def get(self, key):

        return self.data.get(key)

    def get_section(self, section):

        return self.data.get(section, {})

    def set(self, key, value):

        self.data[key] = value

    def set_section(self, section, values: dict):
        """Actualiza (merge) los valores de una sección, ej: 'tts' o 'filters'."""

        current = self.data.get(section, {})
        current.update(values)
        self.data[section] = current

    def save(self):
        """Escribe el estado actual de vuelta en config/config.json."""

        with open(CONFIG_PATH, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)