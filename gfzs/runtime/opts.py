import os, sys
import argparse
from typing import Optional

# local

try:
    # need when 「python3 gfzs/runtime/config.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        from utils.logger import Logger

        if os.environ.get("DEBUG"):
            from utils import debug

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        from gfzs.utils.logger import Logger

        if os.environ.get("DEBUG"):
            import gfzs.utils.debug as debug

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    from utils.logger import Logger

    if os.environ.get("DEBUG"):
        import utils.debug as debug

DEFAULT_SCORE = 30

# ref: https://qiita.com/ttsubo/items/c4af71ceba15b5b213f8
class Singleton(object):
    @classmethod
    def get_instance(cls, args: Optional[argparse.Namespace] = None):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(args)
        else:
            if args != None:
                cls._instance.args = args

        return cls._instance


class RuntimeOpts(Singleton):
    """A class that reads and manages the options passed in the runtime"""

    """fuzzywuzzy's score. please see https://github.com/seatgeek/fuzzywuzzy"""
    default_score = DEFAULT_SCORE

    def __init__(self, args):
        self.logger = Logger.get_instance()
        self.logger.debug("[RuntimeOpts] init")
        self.args = args

    @property
    def score(self) -> int:
        if self.args is None:
            return RuntimeOpts.default_score
        else:
            self.logger.debug("[RuntimeOpts] score = %d" % self.args.score)
            return self.args.score
