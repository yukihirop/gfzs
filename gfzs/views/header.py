import curses
import os, sys

GOOGLE = "Google"
FUZZY = "Fuzzy"
SEARCH = "Search"

try:
    # need when 「python3 gfzs/views/header.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        import info
        from utils import debug

        from base import Base

        if os.environ.get("DEBUG"):
            import utils.debug as debug
    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        from gfzs import info
        from gfzs.utils import debug
        from gfzs.views.base import Base

        if os.environ.get("DEBUG"):
            import gfzs.utils.debug as debug

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    import info
    from utils import debug
    from views.base import Base

    if os.environ.get("DEBUG"):
        import utils.debug as debug


class Header(Base):
    def __init__(self, stdscr):
        super().__init__(stdscr, None, "header")
        self.version = "(%s)" % info.__version__
        self.copyright = info.__copyright__

    def create(self):
        self._init_layout()
        self._make_header()
        self.window.refresh()

    def reset(self):
        self.window.erase()
        self._init_layout()
        self._make_header()
        self.window.refresh()

    def _init_layout(self):
        self.parent_height, self.parent_width = self.stdscr.getmaxyx()
        self.window = curses.newwin(2, self.parent_width, 0, 0)

    # https://stackoverflow.com/a/53016371/9434894
    def _make_header(self):
        start_index = 0
        # Write Google
        google = list(GOOGLE)
        first_o = True
        for i in range(len(google)):
            c = google[i]
            if c == "o":
                if first_o:
                    first_o = False
                    self.window.addstr(0, i, c, self.color.google("o"))
                else:
                    self.window.addstr(0, i, c, self.color.google("o2"))
            else:
                self.window.addstr(0, i, c, self.color.google(c))

        # Write Fuzzy
        start_index += len(GOOGLE) + 1
        self.window.addstr(0, start_index, FUZZY, self.color.fuzzy())

        # Write Search
        start_index += len(FUZZY) + 1
        self.window.addstr(0, start_index, SEARCH, self.color.search())

        # Write verion
        start_index += len(SEARCH) + 1
        self.window.addstr(0, start_index, self.version, self.color.version())

        # Write Copyright
        self.window.addstr(
            0,
            self.parent_width - len(self.copyright),
            self.copyright,
            self.color.copy_right(),
        )
        self.window.hline(
            1, 0, curses.ACS_HLINE | self.colors["hline"], self.parent_width
        )


if __name__ == "__main__":

    class TestHeader(Header):
        def run(self):
            self._loop()

        def _end_curses(self):
            """ Terminates the curses application. """
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
    import curses
    import signal
    import os, sys

    # local

    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    import utils, model
    from model import Model

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # initscr() returns a window object representing the entire screen.
    stdscr = curses.initscr()

    # turn off automatic echoing of keys to the screen
    curses.noecho()
    # Buffering off
    # https://docs.python.org/ja/3/library/curses.html#curses.cbreak
    curses.cbreak()
    # Disable the mouse cursor.
    curses.curs_set(0)

    target = TestHeader(stdscr)
    error = None
    try:
        target.run()
    except curses.error as e:
        error = str(e)
    finally:
        target._end_curses()
        if error != None:
            print(error)
