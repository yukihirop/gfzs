import os, sys
import argparse
from typing import Optional

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

"""RuntimeOpts Class that reads and manages the options passed in the runtime"""

# https://qiita.com/risuoku/items/23789030db29489f8214
self = sys.modules[__name__]

"""fuzzywuzzy's score. please see https://github.com/seatgeek/fuzzywuzzy"""
DEFAULT_SCORE = 30
default_score = DEFAULT_SCORE


def init(args: argparse.Namespace = None) -> None:
    logger.debug("[RuntimeOpts] init")
    self.args = args
    self.score = self._score()


def _score() -> int:
    if self.args is None:
        return default_score
    elif self.args != None and not ("score" in self.args):
        return default_score
    else:
        logger.debug("[RuntimeOpts] score = %d" % self.args.score)
        return self.args.score
