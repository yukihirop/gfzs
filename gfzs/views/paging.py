import curses
import math
import os, sys

GOOGLE = "Google"
FUZZY = "Fuzzy"
SEARCH = "Search"

try:
    # need when 「python3 gfzs/views/header.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        from base import Base
        import utils.logger as logger

        if os.environ.get("DEBUG"):
            import utils.debug as debug

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        from gfzs.views.base import Base
        import gfzs.utils.logger as logger

        if os.environ.get("DEBUG"):
            import gfzs.utils.debug as debug

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    from views.base import Base
    import utils.logger as logger

    if os.environ.get("DEBUG"):
        import utils.debug as debug


class Paging(Base):
    def __init__(self, stdscr, view):
        logger.debug("[Paging] init")
        super().__init__(stdscr, None, "paging")
        self.view = view

    def create(self):
        logger.debug("[Paging] create")
        self._init_layout()
        self._make_paging()
        self.window.refresh()

    def reset(self):
        logger.debug("[Paging] reset")
        self.destroy()
        self._init_layout()
        self._make_paging()
        self.window.refresh()

    def destroy(self):
        logger.debug("[Paging] destroy")
        self.window.erase()

    def _init_layout(self):
        self.parent_height, self.parent_width = self.stdscr.getmaxyx()
        self.window = curses.newwin(2, self.parent_width, self.parent_height - 4, 0)

    # https://stackoverflow.com/a/53016371/9434894
    def _make_paging(self):
        begin_x = self.parent_width // 2 - 1
        per_page = self.view.per_page
        data_size = self.view.data_size
        paging = "{0}/{1}".format(
            self.view.current_page, math.ceil(data_size / per_page)
        )
        self.window.addstr(0, begin_x, paging, self.colors["common"] | curses.A_BOLD)


if __name__ == "__main__":

    class TestPaging(Paging):
        def run(self):
            self._loop()

        def _end_curses(self):
            """ Terminates the curses application. """
            logger.debug("[TestPaging] end curses")
            curses.nocbreak()
            self.window.keypad(0)
            curses.echo()
            curses.endwin()

        def _loop(self):
            self.create()

            while True:
                try:
                    user_input = self.window.getch()
                except curses.error:
                    continue
                except KeyboardInterrupt:
                    break

                if user_input == curses.KEY_RESIZE:
                    self.reset()


if __name__ == "__main__":
    import signal
    import json

    # local

    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    from model import Model
    from search_result import SearchResult
    from runtime.config import RuntimeConfig

    progname = "gfzs.views.paging"
    properties = {"progname": progname, "severity": 0, "log_path": "./tmp/gfzs.log"}
    logger.init_properties(**properties)
    logger.debug("start %s" % progname)

    def handle_sigint(signum, frame):
        logger.debug("detect SIGINT (Ctrl-c)")
        logger.debug("exit 0")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_sigint)

    runtime_config = RuntimeConfig.get_instance()
    if not runtime_config.valid():
        logger.debug("[print] 'Config is invalid.'")
        print("Config is invalid.")
        for error in runtime_config.errors:
            logger.error(error)
            print("Error: %s" % error)

        logger.debug("exit 1")
        logger.debug("end %s" % progname, new_line=True)
        sys.exit(1)

    json_str = open("fixtures/rust.json", "r").read()
    data = json.loads(json_str)

    # initscr() returns a window object representing the entire screen.
    logger.debug("init curses")
    stdscr = curses.initscr()

    # turn off automatic echoing of keys to the screen
    curses.noecho()
    # Buffering off
    # https://docs.python.org/ja/3/library/curses.html#curses.cbreak
    curses.cbreak()
    # Aable the mouse cursor.
    curses.curs_set(0)

    model = Model(data)
    model.update_query("")
    _ = model.find()

    view = SearchResult(stdscr, model)
    view.helper.current_selected = 1
    view.helper.per_page = 5

    target = TestPaging(stdscr, view)
    error = None
    try:
        target.run()
    except curses.error as e:
        error = str(e)
    finally:
        target._end_curses()
        if error != None:
            logger.error(error)
            print(error)

        logger.debug("end %s" % progname, new_line=True)
