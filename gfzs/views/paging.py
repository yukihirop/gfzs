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
        from utils import debug
        from utils.color import Color
        from config.app import AppConfig

    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        from gfzs.utils import debug
        from gfzs.utils.color import Color
        from gfzs.config.app import AppConfig

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    from utils import debug
    from utils.color import Color
    from config.app import AppConfig


class Paging:
    def __init__(self, stdscr, view):
        self.stdscr = stdscr
        self.view = view
        self.app_config = AppConfig.get_instance()
        self.color = Color.get_instance()
        self.color_data = self.app_config.data["view"]["paging"]["color"]
        self.colors = self._create_colors(self.app_config, self.color_data)

    def create(self):
        self._init_layout()
        self._make_paging()
        self.window.refresh()

    def reset(self):
        self.destroy()
        self._init_layout()
        self._make_paging()
        self.window.refresh()

    def destroy(self):
        self.window.erase()

    def _create_colors(self, app_config, color_data) -> dict:
        result = {}
        for view_name in color_data:
            result[view_name] = self.color.use(color_data[view_name])

        return result

    def _init_layout(self):
        self.parent_height, self.parent_width = self.stdscr.getmaxyx()
        self.window = curses.newwin(2, self.parent_width, self.parent_height - 4, 0)

    def _end_curses(self, end=True):
        """ Terminates the curses application. """
        curses.nocbreak()
        self.window.keypad(0)
        if end:
            curses.echo()
            curses.endwin()

    # https://stackoverflow.com/a/53016371/9434894
    def _make_paging(self):
        begin_x = self.parent_width // 2 - 1
        current_selected = self.view.current_selected
        per_page = self.view.per_page
        data_size = self.view.data_size
        paging = "{0}/{1}".format(
            (current_selected // per_page + 1), math.ceil(data_size / per_page)
        )
        self.window.addstr(0, begin_x, paging, self.colors["common"] | curses.A_BOLD)

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
    import os, sys
    import curses
    import signal
    import json

    # local

    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    from model import Model
    from search_result import SearchResult

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    json_str = open("fixtures/rust.json", "r").read()
    data = json.loads(json_str)

    # initscr() returns a window object representing the entire screen.
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

    Paging(stdscr, view)._loop()
