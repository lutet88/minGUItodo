import yaml
import os
import styling
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt


class Config(dict):
    def __init__(self):
        super(Config, self).__init__()
        f = open(os.path.join(os.path.dirname(__file__), "config.yml"), "r+")
        self.configuration = yaml.load(f, Loader=yaml.SafeLoader)
        f.close()
        print("[INFO] config.yml loaded")

        fs = open(os.path.join(os.path.dirname(__file__), "style.yml"), "r+")
        self.styling = yaml.load(fs, Loader=yaml.SafeLoader)
        self.styledata = []
        self.palette = QPalette()
        fs.close()
        try:
            for style in self.styling:
                self.styledata.append((eval("QPalette." + style), eval(self.styling[style])))
            print("[INFO] styling:", self.styledata)
            self.palette = styling.Palette(self.styledata)
            print("[INFO] style.yml loaded")
        except Exception:
            print("[ERR] style not loaded")
        print(self.configuration)

    def __getitem__(self, key):
        return self.configuration[key]

    def __repr__(self):
        return repr(self.configuration)

    def __delitem__(self, key):
        del self.configuration[key]

    def __setitem__(self, key, item):
        print("debug: configuration change called.")
        print(key, self.configuration[key], "->", item)
        self.configuration[key] = item

    def get_palette(self):
        return self.palette
