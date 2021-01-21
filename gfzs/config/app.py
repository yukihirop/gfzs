# ref: https://qiita.com/ttsubo/items/c4af71ceba15b5b213f8
import argparse
import curses
import os
import sys
import json

# local

try:
    # need when 「python3 gfzs/config/app.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        from utils import debug

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        from gfzs.utils import debug

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    from utils import debug

# ~/.gfzsrc
DEFAULT_CONFIG_PATH = "%s/.gfzsrc" % os.path.expanduser("~")

# 0: curses.COLOR_BLACK
# 1: curses.COLOR_RED
# 2: curses.COLOR_GREEN
# 3: curses.COLOR_YELLOW
# 4: curses.COLOR_BLUE
# 5: curses.COLOR_MAGENTA
# 6: curses.COLOR_CYAN
# 7: curses.COLOR_WHITE
DEFAULT_CONFIG = {
    "view": {
        "footer": {
            "message": "QUERY>",
            "color": {
                "message": {
                    "text": curses.COLOR_GREEN,
                    "background": curses.COLOR_BLACK,
                    "style": "normal",
                },
                "hline": {
                    "text": curses.COLOR_WHITE,
                    "background": curses.COLOR_BLACK,
                    "style": "normal",
                },
            },
        },
        "header": {
            "color": {
                "hline": {
                    "text": curses.COLOR_WHITE,
                    "background": curses.COLOR_BLACK,
                    "style": "normal",
                },
            }
        },
        "search_result": {
            "color": {
                "index": {
                    "text": curses.COLOR_CYAN,
                    "background": curses.COLOR_BLACK,
                    "style": "normal",
                },
                "title": {
                    "text": curses.COLOR_GREEN,
                    "background": curses.COLOR_BLACK,
                    "style": "bold",
                },
                "url": {
                    "text": curses.COLOR_YELLOW,
                    "background": curses.COLOR_BLACK,
                    "style": "link",
                },
                "abstract": {
                    "text": curses.COLOR_WHITE,
                    "background": curses.COLOR_BLACK,
                    "style": "normal",
                },
                "markup_partial": {
                    "text": curses.COLOR_GREEN,
                    "background": curses.COLOR_MAGENTA,
                    "style": "normal",
                },
                "markup_char": {
                    "text": curses.COLOR_RED,
                    "background": curses.COLOR_BLACK,
                    "style": "normal",
                },
            }
        },
        "paging": {
            "color": {
                "common": {
                    "text": curses.COLOR_GREEN,
                    "background": curses.COLOR_BLACK,
                    "style": "bold",
                }
            }
        },
    }
}


class Singleton(object):
    @classmethod
    def get_instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()

        return cls._instance


class AppConfig(Singleton):
    """A class that reads and manages the options passed in the runtime"""

    def __init__(self):
        self.data = self._create_data()

    @property
    def config_path(self):
        return DEFAULT_CONFIG_PATH

    def _create_data(self) -> dict:
        """Load the app settings. If the config file does not exist, it will load the default config."""
        config_path = self.config_path

        data = dict
        if os.path.exists(config_path):
            try:
                json_str = open(config_path).read()
                data = json.loads(json_str)
            except json.decoder.JSONDecodeError as e:
                self._end_curses()
                raise e
        else:
            data = DEFAULT_CONFIG

        return data

    def _end_curses(self):
        """ Terminates the curses application. """
        curses.nocbreak()
        curses.echo()
        curses.endwin()


if __name__ == "__main__":

    config = AppConfig.get_instance()
    print(config.data)
