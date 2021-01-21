import curses
import curses.ascii
import os, sys

# local

try:
    # need when 「python3 gfzs/views/footer.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        from utils import debug
        from utils.multibyte import Multibyte

        from base import Base

        if os.environ.get("DEBUG"):
            import utils.debug as debug
    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        from gfzs.utils import debug
        from gfzs.utils.multibyte import Multibyte
        from gfzs.views.base import Base

        if os.environ.get("DEBUG"):
            import gfzs.utils.debug as debug
# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    from utils import debug
    from utils.multibyte import Multibyte
    from views.base import Base

    if os.environ.get("DEBUG"):
        import utils.debug as debug

KEY_ENTER = 10
KEY_ESC = 27


class Footer(Base):
    def __init__(self, stdscr, model):
        super().__init__(stdscr, model, "footer")
        self.multibyte = Multibyte(stdscr)

    @property
    def query(self):
        return self.model.query

    @property
    def query_len(self):
        return self.multibyte.get_east_asian_width_count(self.query)

    @property
    def message(self):
        return self.app_config.data["view"]["footer"]["message"]

    @property
    def message_len(self):
        return self.multibyte.get_east_asian_width_count(self.message)

    def update_query(self, query):
        self.model.update_query(query)

    def create(self):
        self.update_query("")
        self._make_footer()

    def reset(self):
        self._make_footer()
        self.stdscr.move(
            self.parent_height - 1,
            self.message_len + 1 + self.query_len,
        )
        self.stdscr.refresh()

    def activate(self, is_init=False):
        # Able mouse cursor
        curses.curs_set(1)
        self.stdscr.move(
            self.parent_height - 1,
            self.message_len + 1 + self.query_len,
        )

        if is_init:
            self.stdscr.clrtoeol()

        self.stdscr.refresh()

    def delete_char(self):
        if self.query == None or self.query == "":
            self.stdscr.delch(self.parent_height - 1, self.message_len + 1 + 1)  # ?
            self.stdscr.delch(self.parent_height - 1, self.message_len + 1)  # ^
        else:
            query_len = self.query_len
            if query_len > 0:
                if self.multibyte.is_full_width(self.query[-1]):
                    k = 2
                else:
                    k = 1
                # backspace = ^?
                self.stdscr.delch(
                    self.parent_height - 1, self.message_len + 1 + query_len - k + 2
                )  # ?
                self.stdscr.delch(
                    self.parent_height - 1, self.message_len + 1 + query_len - k + 1
                )  # ^
                self.stdscr.delch(
                    self.parent_height - 1, self.message_len + 1 + query_len - k
                )
                self.update_query(self.query[:-1])

    def write(self, text):
        self.stdscr.addstr(text)
        self.model.push_query(text)

    # stdscr.getch doesn't work when I addstr to subwin
    def _make_footer(self):
        self.stdscr.hline(
            self.parent_height - 2,
            0,
            curses.ACS_HLINE | self.colors["hline"],
            self.parent_width,
        )
        self.stdscr.addstr(
            self.parent_height - 1, 0, self.message, self.colors["message"]
        )


if __name__ == "__main__":

    class TestFooter(Footer):
        def run(self):
            self.create()
            inp = self._loop()
            self._end_curses()
            return inp

        def _end_curses(self):
            """ Terminates the curses application. """
            curses.nocbreak()
            self.stdscr.keypad(0)
            curses.echo()
            curses.endwin()

        def _loop(self):
            self.activate(is_init=True)

            inp = ""
            while True:
                try:
                    user_input = self.multibyte.getch()
                except curses.error:
                    continue
                except KeyboardInterrupt:
                    break

                # Ah hitting enter, return the index of the selected list element.
                if user_input == curses.KEY_ENTER or user_input == KEY_ENTER:
                    return inp
                # https://www.programcreek.com/python/?code=mingrammer%2Fawesome-finder%2Fawesome-finder-master%2Fawesome%2Ftui.py
                elif user_input in (
                    curses.ascii.BS,
                    curses.ascii.DEL,
                    curses.KEY_BACKSPACE,
                ):
                    self.delete_char()
                    inp = inp[:-1]
                elif user_input == curses.KEY_RESIZE:
                    self.reset()
                else:
                    self.write(chr(user_input))
                    inp += chr(user_input)
                    self.update_query(inp)


if __name__ == "__main__":
    import os, sys
    import curses
    import signal

    # local

    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    from model import Model

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # initscr() returns a window object representing the entire screen.
    stdscr = curses.initscr()

    # turn off automatic echoing of keys to the screen
    curses.noecho()
    # Buffering off
    # https://docs.python.org/ja/3/library/curses.html#curses.cbreak
    curses.cbreak()
    # Aable the mouse cursor.
    curses.curs_set(1)

    model = Model([])
    target = TestFooter(stdscr, model)
    error = None
    try:
        inp = target.run()
        print("query:", model.query)
        print("result:", inp)
    except curses.error as e:
        error = str(e)
    finally:
        if error != None:
            print(error)
