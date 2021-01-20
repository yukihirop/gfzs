# ref: https://qiita.com/ttsubo/items/c4af71ceba15b5b213f8

import argparse

DEFAULT_SCORE = 30

default_args = argparse.Namespace(score=DEFAULT_SCORE)


class Singleton(object):
    @classmethod
    def get_instance(cls, args=default_args):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(args)
        else:
            if args != None:
                cls._instance.args = args

        return cls._instance


class RuntimeConfig(Singleton):
    """A class that reads and manages the options passed in the runtime"""

    """fuzzywuzzy's score. please see https://github.com/seatgeek/fuzzywuzzy"""
    default_score = DEFAULT_SCORE

    def __init__(self, args):
        self.args = args

    @property
    def score(self):
        return self.args.score or RuntimeConfig.default_score
