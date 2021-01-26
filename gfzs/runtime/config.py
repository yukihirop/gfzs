# ref: https://qiita.com/ttsubo/items/c4af71ceba15b5b213f8
import argparse
import curses
import os
import sys
import json
from flatten_dict import flatten

# local

try:
    # need when 「python3 gfzs/runtime/config.py」
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


class RuntimeConfig(Singleton):
    """A class that reads and manages the options passed in the runtime"""

    SUPPORT_FLATTEN_KEYS = list(flatten(DEFAULT_CONFIG, reducer="dot"))
    SUPPORT_COLOR_NUMBERS = list(range(8))
    SUPPORT_STYLES = ["normal", "link", "bold"]

    def __init__(self):
        self.data = self._create_data()
        self.errors = []

    @property
    def config_path(self):
        return DEFAULT_CONFIG_PATH

    def valid(self) -> bool:
        flatten_data = flatten(
            self.data, reducer="dot", keep_empty_types=(dict, str, int, list)
        )
        for flatten_key in flatten_data:
            target_val = flatten_data[flatten_key]
            # Check key
            if not flatten_key in RuntimeConfig.SUPPORT_FLATTEN_KEYS:
                self.errors.append(
                    Exception(
                        "Contains unsupported key.   (key_path, value) = (%s, %s)."
                        % (flatten_key, target_val)
                    )
                )
            # Check value
            else:
                if flatten_key.endswith("text") or flatten_key.endswith("background"):
                    if not target_val in RuntimeConfig.SUPPORT_COLOR_NUMBERS:
                        self.errors.append(
                            Exception(
                                "Contains unsupported value. (key_path, value) = (%s, %s)."
                                % (flatten_key, target_val)
                            )
                        )
                elif flatten_key.endswith("style"):
                    if not target_val in RuntimeConfig.SUPPORT_STYLES:
                        self.errors.append(
                            Exception(
                                "Contains unsupported value. (key_path, value) = (%s, %s)."
                                % (flatten_key, target_val)
                            )
                        )

        if self.errors != []:
            return False
        else:
            return True

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

    config = RuntimeConfig.get_instance()
    print(config.data)
