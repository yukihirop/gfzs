# ref: https://qiita.com/ttsubo/items/c4af71ceba15b5b213f8
import argparse
import curses
import os
import sys
import json

# local

try:
    # need when 「python3 gfzs/config/app.py」
    if __name__ == '__main__':
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(
            os.path.abspath(os.path.dirname(__file__))))
        from utils import debug

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        from gfzs.utils import debug

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('../'))))
    from utils import debug

DEFAULT_CONFIG_PATH = "~/.gfzsrc"
# {
#     "view": {
#         "footer": {
#             "message": "QUERY>",
#             "color": {
#                 "message": {
#                     "text": 2,
#                     "background": 0,
#                     "style": "normal"
#                 },
#                 "hline": {
#                     "text": 7,
#                     "background": 0,
#                     "style": "normal"
#                 }
#             }
#         },
#         "header": {
#             "color": {
#                 "hline": {
#                     "text": 7,
#                     "background": 0,
#                     "style": "normal"
#                 }
#             }
#         },
#         "search_result": {
#             "color": {
#                 "index": {
#                     "text": 6,
#                     "background": 0,
#                     "style": "normal"
#                 },
#                 "title": {
#                     "text": 2,
#                     "background": 0,
#                     "style": "bold"
#                 },
#                 "url": {
#                     "text": 3,
#                     "background": 0,
#                     "style": "link"
#                 },
#                 "abstract": {
#                     "text": 7,
#                     "background": 0,
#                     "style": "normal"
#                 }
#             }
#         },
#         "paging": {
#             "color": {
#                 "common": {
#                     "text": 2,
#                     "background": 0,
#                     "style": "bold"
#                 }
#             }
#         }
#     }
# }

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
                    "style": "normal"
                },
            }
        },
        "header": {
            "color": {
                "hline": {
                    "text": curses.COLOR_WHITE,
                    "background": curses.COLOR_BLACK,
                    "style": "normal"
                },
            }
        },
        "search_result": {
            "color": {
                "index": {
                    "text": curses.COLOR_CYAN,
                    "background": curses.COLOR_BLACK,
                    "style": "normal"
                },
                "title": {
                    "text": curses.COLOR_GREEN,
                    "background": curses.COLOR_BLACK,
                    "style": "bold"
                },
                "url": {
                    "text": curses.COLOR_YELLOW,
                    "background": curses.COLOR_BLACK,
                    "style": "link"
                },
                "abstract": {
                    "text": curses.COLOR_WHITE,
                    "background": curses.COLOR_BLACK,
                    "style": "normal"
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
                }
            }
        },
        "paging": {
            "color": {
                "common": {
                    "text": curses.COLOR_GREEN,
                    "background": curses.COLOR_BLACK,
                    "style": "bold"
                }
            }
        }
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

    def _create_data(self, config_path=DEFAULT_CONFIG_PATH) -> dict:
        """Load the app settings. If the config file does not exist, it will load the default config."""

        data = dict
        if os.path.exists(config_path):
            try:
                json_str = open(config_path).read()
                data = json.loads(json_str)
            except json.decoder.JSONDecodeError as e:
                raise e
        else:
            data = DEFAULT_CONFIG

        return data


if __name__ == '__main__':

    config = AppConfig.get_instance()
    print(config.data)
