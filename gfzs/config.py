# ref: https://qiita.com/ttsubo/items/c4af71ceba15b5b213f8

class Singleton(object):
    @classmethod
    def get_instance(cls, args = None):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(args)
        else:
            if args != None:
              cls._instance.args = args
        return cls._instance

class Config(Singleton):
    def __init__(self, args):
        self.args = args

    @property
    def score(self):
      return self.args.score
