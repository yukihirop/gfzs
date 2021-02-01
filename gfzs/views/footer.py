import curses
import curses.ascii
import os, sys

# local

try:
    # need when 「python3 gfzs/views/footer.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        from utils.multibyte import Multibyte
        from base import Base
        import utils.logger as logger

        if os.environ.get("DEBUG"):
            import utils.debug as debug
    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        from gfzs.utils.multibyte import Multibyte
        from gfzs.views.base import Base
        import gfzs.utils.logger as logger

        if os.environ.get("DEBUG"):
            import gfzs.utils.debug as debug
# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    from utils.multibyte import Multibyte
    from views.base import Base
    import utils.logger as logger

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
        return self.runtime_config.data["view"]["footer"]["message"]

    @property
    def message_len(self):
        return self.multibyte.get_east_asian_width_count(self.message)

    def update_query(self, query):
        logger.debug("[Footer] update query from '%s' to '%s'" % (self.query, query))
        self.model.update_query(query)

    def create(self):
        logger.debug("[Footer] create")
        self.update_query("")
        self._make_footer()

    def reset(self):
        logger.debug("[Footer] reset")
        self._make_footer()
        self.stdscr.move(
            self.parent_height - 1,
            self.message_len + 1 + self.query_len,
        )
        self.stdscr.refresh()

    def activate(self, is_init=False):
        logger.debug("[Footer] active")
        # Able mouse cursor
        curses.curs_set(1)
        self.stdscr.move(
            self.parent_height - 1,
            self.message_len + 1 + self.query_len,
        )

        if is_init:
            logger.debug("[Footer] clean")
            self.stdscr.clrtoeol()

        self.stdscr.refresh()

    def delete_char(self):
        logger.debug("[Footer] delete char")
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

        logger.debug("[Footer] delete char. so that query is '%s'" % self.query)

    def write(self, text):
        logger.debug("[Footer] write text: %s" % text)
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
            logger.debug("[TestFooter] end curses")
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
    import signal

    # local

    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    from model import Model
    from runtime.config import RuntimeConfig

    progname = "gfzs.views.footer"
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
        sys.exit(1)

    # initscr() returns a window object representing the entire screen.
    logger.debug("init curses")
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
        logger.debug("query: '%s'" % model.query)
        logger.debug("result: '%s'" % inp)
        print("query:", model.query)
        print("result:", inp)
    except curses.error as e:
        error = str(e)
    finally:
        if error != None:
            logger.error(error)
            print(error)

        logger.debug("end %s" % progname, new_line=True)
