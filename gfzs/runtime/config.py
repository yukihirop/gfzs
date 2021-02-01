# ref: https://qiita.com/ttsubo/items/c4af71ceba15b5b213f8
import argparse
import curses
import os
import sys
import json
from flatten_dict import flatten
from typing import Union

# local

try:
    # need when 「python3 gfzs/runtime/config.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        import utils.logger as logger

        if os.environ.get("DEBUG"):
            from utils import debug

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        import gfzs.utils.logger as logger

        if os.environ.get("DEBUG"):
            import gfzs.utils.debug as debug

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    import utils.logger as logger

    if os.environ.get("DEBUG"):
        import utils.debug as debug

"""RuntimeConfig Class that reads and manages the options passed in the runtime"""

# https://qiita.com/risuoku/items/23789030db29489f8214
self = sys.modules[__name__]

# ~/.gfzsrc
DEFAULT_CONFIG_PATH = "%s/.gfzsrc" % os.path.expanduser("~")
# ~/gfzs.log
DEFAULT_LOG_PATH = "%s/gfzs.log" % os.path.expanduser("~")

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
    },
}

SUPPORT_FLATTEN_KEYS = list(flatten(DEFAULT_CONFIG, reducer="dot"))
SUPPORT_COLOR_NUMBERS = list(range(8))
SUPPORT_STYLES = ["normal", "link", "bold"]

default_log_path = DEFAULT_LOG_PATH
default_config_path = DEFAULT_CONFIG_PATH


def init() -> None:
    logger.debug("[RuntimeConfig] init")
    self.config_path = DEFAULT_CONFIG_PATH
    self.data = self._create_data()
    self.errors = []


def valid() -> bool:
    logger.debug("[RuntimeConfig] validate")
    flatten_data = flatten(
        self.data, reducer="dot", keep_empty_types=(dict, str, int, list)
    )
    for flatten_key in flatten_data:
        target_val = flatten_data[flatten_key]
        # Check key
        if not flatten_key in SUPPORT_FLATTEN_KEYS:
            self.errors.append(
                Exception(
                    "Contains unsupported key.   (key_path, value) = (%s, %s)."
                    % (flatten_key, target_val)
                )
            )
        # Check value
        else:
            if flatten_key.endswith("text") or flatten_key.endswith("background"):
                if not target_val in SUPPORT_COLOR_NUMBERS:
                    self.errors.append(
                        Exception(
                            "Contains unsupported value. (key_path, value) = (%s, %s)."
                            % (flatten_key, target_val)
                        )
                    )
            elif flatten_key.endswith("style"):
                if not target_val in SUPPORT_STYLES:
                    self.errors.append(
                        Exception(
                            "Contains unsupported value. (key_path, value) = (%s, %s)."
                            % (flatten_key, target_val)
                        )
                    )

    if self.errors != []:
        logger.error("[RuntimeConfig] is invalid")
        return False
    else:
        logger.debug("[RuntimeConfig] is valid")
        return True


def _create_data() -> dict:
    """Load the app settings. If the config file does not exist, it will load the default config."""
    config_path = self.config_path
    data = dict

    if os.path.exists(config_path):
        try:
            json_str = open(config_path).read()
            data = json.loads(json_str)
            logger.debug("[RuntimeConfig] file is loaded")
        except json.decoder.JSONDecodeError as e:
            logger.debug(e)
            self._end_curses()
            raise e
    else:
        logger.debug("[RuntimeConfig] file do not exist. so load default config data")
        data = DEFAULT_CONFIG

    return data


def _end_curses():
    """ Terminates the curses application. """
    logger.debug("end curses")
    curses.nocbreak()
    curses.echo()
    curses.endwin()


if __name__ == "__main__":
    progname = "gfzs.runtime.config"
    properties = {"progname": progname, "severity": 0, "log_path": "./tmp/gfzs.log"}
    logger.init_properties(**properties)
    logger.debug("start %s" % progname)

    self.init()
    logger.debug("end %s" % progname, new_line=True)
    print(self.data)
