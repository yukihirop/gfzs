# ref: https://github.com/NikolaiT/Scripts/blob/master/scripts/python/curses/text_selector.py

import curses
import unicodedata
import math
import os, sys

# local

try:
    # need when 「python3 gfzs/views/search_result.py」
    if __name__ == "__main__":
        # https://codechacha.com/ja/how-to-import-python-files/
        sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        from utils.markup import Markup
        from utils.multibyte import Multibyte
        from utils.text_wrapper import TextWrapper
        import utils.logger as logger

        from not_found import NotFound
        from paging import Paging
        from base import Base

        if os.environ.get("DEBUG"):
            import utils.debug as debug
    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    else:
        from gfzs.utils.markup import Markup
        from gfzs.utils.multibyte import Multibyte
        from gfzs.utils.text_wrapper import TextWrapper
        import gfzs.utils.logger as logger

        from gfzs.views.not_found import NotFound
        from gfzs.views.paging import Paging
        from gfzs.views.base import Base

        if os.environ.get("DEBUG"):
            import gfzs.utils.debug as debug
# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("../"))))
    from utils.markup import Markup
    from utils.multibyte import Multibyte
    from utils.text_wrapper import TextWrapper
    import utils.logger as logger

    from views.not_found import NotFound
    from views.paging import Paging
    from views.base import Base

    if os.environ.get("DEBUG"):
        import utils.debug as debug


class SearchResultHelper:
    def __init__(self):
        logger.debug("[SearchResultHelper] init")
        self.current_selected = 0
        self.last = 1
        self.topy = 1
        self.top_textbox = None
        self.pad_begin_y = 0
        self.per_page = 1
        self.change_page = False

    def update_attributues(self, current_selected, last, topy, top_textbox):
        logger.debug(
            "[SearchResultHelper] update attributes '(current_selected, last, topy)' from '(%d, %d, %d)' to '(%d, %d, %d)'"
            % (
                self.current_selected,
                self.last,
                self.topy,
                current_selected,
                last,
                topy,
            )
        )
        self.current_selected = current_selected
        self.last = last
        self.topy = topy
        self.top_textbox = top_textbox

    def update_per_page(self, value):
        logger.debug(
            "[SearchResultHelper] update per_page from '%d' to '%d'"
            % (self.per_page, value)
        )
        self.per_page = value

    @property
    def current_page(self) -> int:
        return self.current_selected // self.per_page + 1

    def prev_page(self, total_data_size):
        logger.debug("[SearchResultHelper] prev page")
        per_page = self.per_page
        old_current_selected = self.current_selected
        current_pagetop_index = per_page * math.floor(old_current_selected / per_page)

        self.change_page = True
        if self.current_page == 1:
            total_page = math.ceil(total_data_size / per_page)

            if total_page >= 1:
                self.current_selected = (total_page - 1) * per_page
            else:
                pass
        else:
            self.current_selected = current_pagetop_index - per_page

    def next_page(self, total_data_size):
        logger.debug("[SearchResultHelper] next page")
        per_page = self.per_page
        old_current_selected = self.current_selected
        current_pagetop_index = per_page * math.floor(old_current_selected / per_page)
        total_page = math.ceil(total_data_size / per_page)

        self.change_page = True
        if self.current_page == total_page:
            self.current_selected = 0
        else:
            self.current_selected = current_pagetop_index + per_page

    def down(self, total_data_size):
        logger.debug("[SearchResultHelper] down")
        old_current_page = self.current_page
        old_current_selected = self.current_selected

        if old_current_selected >= total_data_size - 1:
            self.change_page = True
            self.current_selected = 0
        else:
            self.current_selected += 1
            if self.current_page != old_current_page:
                self.change_page = True

    def up(self, total_data_size):
        logger.debug("[SearchResultHelper] up")
        old_current_page = self.current_page
        old_current_selected = self.current_selected

        if old_current_selected == 0:
            self.change_page = True
            self.current_selected = total_data_size - 1  # wrap around.
        else:
            self.current_selected -= 1
            if self.current_page != old_current_page:
                self.change_page = True


class SearchResult(Base):
    """Display options build from a list of strings in a (unix) terminal.
    The user can browser though the textboxes and select one with enter.
    """

    def __init__(self, stdscr, model):
        """Create a SearchResult object.
        'data' is list of string. Each string is used to build
        a textbox.
        """
        logger.debug("[SearchResult] init")
        super().__init__(stdscr, model, "search_result")
        self.paging = Paging(stdscr, self)
        self.textboxes = []
        self.helper = SearchResultHelper()
        self.not_found = NotFound(stdscr)
        self.markup = Markup()
        self.multibyte = Multibyte()

        # Element parameters. Channge them here.
        self.TEXTBOX_HEIGHT = 8
        self.PAD_WIDTH = 400
        self.PAD_HEIGHT = 1000

    @property
    def current_selected(self) -> int:
        return self.helper.current_selected

    @property
    def per_page(self) -> int:
        return self.helper.per_page

    @property
    def data_size(self) -> int:
        return self.model.data_size

    @property
    def current_page(self) -> int:
        return self.helper.current_page

    def update_per_page(self, value):
        self.helper.update_per_page(value)

    def init_properties_after_create(self):
        logger.debug("[SearchResult] init properties")
        current_selected = 0
        textboxes_len = len(self.textboxes)

        if textboxes_len > 0:
            top_textbox = self.textboxes[0]
            topy, _ = self._refresh_view(top_textbox)
            if textboxes_len > 1:
                last = 1
            else:
                last = 0

            self.helper.update_attributues(current_selected, last, topy, top_textbox)

    def create(self, pad_begin_y=0):
        logger.debug("[SearchResult] create")
        self.helper.pad_begin_y = pad_begin_y
        self._init_layout()
        self._create_pad()
        self.textboxes = self._make_textboxes()
        if len(self.textboxes) > 0:
            self._refresh_view(self.textboxes[0])
            self.paging.create()

    def destroy(self):
        logger.debug("[SearchResult] destroy")
        self._delete_pad()

    def update_query(self, query):
        logger.debug(
            "[SearchResult] update query from '%s' to '%s'" % (self.model.query, query)
        )
        self.model.update_query(query)

    def reset(self):
        logger.debug("[SearchResult] reset")
        self._reset_pad()
        self._init_layout()
        self.textboxes = self._make_textboxes()
        if len(self.textboxes) > 0:
            self.not_found.destroy()
            self._refresh_view(self.textboxes[0])
            self.paging.create()
        else:
            self.paging.destroy()
            self.destroy()
            self.not_found.create()

    def _init_layout(self):
        self.parent_height, self.parent_width = self.stdscr.getmaxyx()
        # 「2」 is the height of the header or footer
        # 「4」 = header + footer height
        self.window = curses.newwin(self.parent_height - 4, self.parent_width, 2, 0)
        self.update_per_page(self.parent_height // self.TEXTBOX_HEIGHT - 1)
        # https://stackoverflow.com/a/17369532/9434894
        self.window.keypad(1)

    def _delete_pad(self):
        self.pad.clear()
        self.window.refresh()

    def _reset_pad(self):
        self._delete_pad()
        self._init_layout()
        self._create_pad()

    def _create_pad(self):
        """ Creates a big self.pad to place the textboxes in. """
        self.pad = curses.newpad(self.PAD_HEIGHT, self.PAD_WIDTH)
        self.pad.box()
        self.window.refresh()

    def _make_textboxes(self):
        """Build the textboxes in the pad center and put them in the
        horizontal middle of the pad."""
        textboxes = []
        i = 1
        data = self.model.find()

        if len(data) == 0:
            return textboxes

        for s in data:
            textbox = self.pad.derwin(
                self.TEXTBOX_HEIGHT,
                self.parent_width - 4,
                i + self.helper.pad_begin_y,
                2,
            )

            textboxes.append(textbox)
            i += self.TEXTBOX_HEIGHT

        # When all are displayed as multi-byte character strings
        gap = 7  # 4 = 1 (Frame border) + 3(padding) + 3(margin)
        abstract_line_len = self.parent_width - 2 * gap
        text_wrapper = TextWrapper(width=abstract_line_len)
        can_write_fn = lambda y: (4 + y) <= (self.TEXTBOX_HEIGHT - 1)

        for k in range(len(textboxes)):
            textboxes[k].box()

            title = data[k].get("title")
            url = data[k].get("url")
            abstract = data[k].get("abstract")

            textboxes[k].addstr(
                2, 2, "%s%-3s" % ("", str(k + 1) + "."), self.colors["index"]
            )
            textboxes[k].addstr(2, 6, title, self.colors["title"])
            textboxes[k].addstr(3, 6, url, self.colors["url"])

            lines = text_wrapper.wrap(abstract)
            for l in range(len(lines)):
                if can_write_fn(l):
                    textboxes[k].addstr(4 + l, 6, lines[l], self.colors["abstract"])

            # Markup Search Query for title
            markup_data = self.markup.parse(title, self.model.query)
            for search_text in markup_data:
                for item in markup_data[search_text]:
                    offset_x = item["half_width"]["start_index"]
                    color = item["color"]
                    match_text = item["match"]
                    textboxes[k].addstr(
                        2, 6 + offset_x, match_text, color | curses.A_BOLD
                    )

            # Markup Search Query for abstract
            for l in range(len(lines)):
                markup_data = self.markup.parse(lines[l], self.model.query)
                for search_text in markup_data:
                    for item in markup_data[search_text]:
                        offset_x = item["half_width"]["start_index"]
                        color = item["color"]
                        match_text = item["match"]

                        match_text_byte_len = self.multibyte.get_east_asian_width_count(
                            match_text
                        )
                        if offset_x + 6 + match_text_byte_len <= self.parent_width - 1:
                            if can_write_fn(l):
                                textboxes[k].addstr(
                                    4 + l,
                                    6 + offset_x,
                                    match_text,
                                    color | curses.A_BOLD,
                                )
                        # Wrap display
                        else:
                            match_text_before = match_text[
                                : (self.parent_width - offset_x)
                            ]
                            byte_len = self.multibyte.get_east_asian_width_count(
                                match_text_before
                            )
                            gap = 6  # 4 = 1 (Frame border) + 3(padding) + 2(margin)
                            if can_write_fn(l + 1):
                                textboxes[k].addstr(
                                    4 + l,
                                    self.parent_width - byte_len - gap,
                                    match_text_before,
                                    color,
                                )

                                match_text_after = match_text[
                                    (self.parent_width - offset_x) :
                                ]
                                textboxes[k].addstr(5 + l, 6, match_text_after, color)

        return textboxes

    def _refresh_view(self, window):
        """ Refresh textboxes """
        cy, cx = window.getbegyx()

        per_page = self.per_page
        display_limit_pos_y = self.TEXTBOX_HEIGHT * per_page
        display_limit_pos_x = self.parent_width - 1

        # Since the display of the last pad is cut off, display_limit_pos_y + self.helper.pad_begin_y
        display_limit_pos_y += self.helper.pad_begin_y

        self.pad.refresh(
            cy,
            cx,
            1 + self.helper.pad_begin_y,
            2,
            display_limit_pos_y,
            display_limit_pos_x,
        )
        return (cy, cx)

    def update_view_in_loop(self) -> bool:
        logger.debug("[SearchResult] update view in loop")
        textboxes = self.textboxes
        textboxes_len = len(textboxes)

        if textboxes_len == 0:
            return False

        current_selected = self.current_selected
        last = self.helper.last
        topy = self.helper.topy
        top_textbox = self.helper.top_textbox

        # Highligth the selected one, the last selected textbox should
        # become normal again.
        if last == current_selected == 0:
            textboxes[current_selected].border(self.color.highlight)
        else:
            textboxes[current_selected].border(self.color.highlight)
            textboxes[last].border()

        # Paging

        # While the textbox can be displayed on the page with the current top_textbox,
        # don't after the view. When this becomes impossible,
        # center the view to last displayable textbox on the previous view.
        cy, cx = textboxes[current_selected].getbegyx()
        per_page = self.per_page

        # The current window is to far down. Switch the top textbox.
        # When you reach the bottom, redisplay the current box at the top
        if (topy + self.parent_height - self.TEXTBOX_HEIGHT) <= cy:
            top_textbox = textboxes[current_selected]

        # The current window is to far up. There is a better way though...
        # Update the top until you reach the top of the screen.
        if topy >= cy + self.TEXTBOX_HEIGHT:
            top_textbox = textboxes[current_selected]

        if last == 0:
            if current_selected > per_page + 1:
                top_textbox = textboxes[current_selected - per_page + 1]

        if self.helper.change_page:
            top_textbox = textboxes[current_selected]

        if last != current_selected:
            last = current_selected

        refresh_topy, _ = self._refresh_view(top_textbox)

        if self.helper.change_page:
            self.paging.reset()

        self.textboxes = textboxes

        self.update_per_page(per_page)
        self.helper.update_attributues(
            current_selected, last, refresh_topy, top_textbox
        )

        return True

    def handle_key_in_loop(self, user_input):
        self.helper.change_page = False
        textboxes = self.textboxes
        textboxes_len = len(textboxes)

        if textboxes_len == 0:
            return

        per_page = self.per_page
        backspace_keys = {
            curses.ascii.BS: "ASCII_BS",
            curses.ascii.DEL: "ASCII_DEL",
            curses.KEY_BACKSPACE: "KEY_BACKSPACE",
        }

        if textboxes_len > 1 and user_input == curses.KEY_DOWN:
            logger.debug("[SearchResult] handle key in loop with 'KEY_DOWN'")
            self.helper.down(textboxes_len)
        elif textboxes_len > 1 and user_input == curses.KEY_UP:
            logger.debug("[SearchResult] handle key in loop with 'KEY_UP'")
            self.helper.up(textboxes_len)
        elif textboxes_len >= per_page + 1 and user_input == curses.KEY_RIGHT:
            logger.debug("[SearchResult] handle key in loop with 'KEY_RIGHT'")
            self.helper.next_page(textboxes_len)
        elif textboxes_len >= per_page + 1 and user_input == curses.KEY_LEFT:
            logger.debug("[SearchResult] handle key in loop with 'KEY_LEFT'")
            self.helper.prev_page(textboxes_len)
        elif user_input == curses.KEY_RESIZE:
            logger.debug("[SearchResult] handle key in loop with 'KEY_RESIZE'")
            self.reset()
        elif user_input in backspace_keys:
            logger.debug(
                "[SearchResult] handle key in loop with '%s'"
                % backspace_keys[user_input]
            )
            self.reset()


if __name__ == "__main__":

    class TestSearchResult(SearchResult):
        def run(self, pad_begin_y=0):
            """ Just run this when you want to spawn the selection process. """
            self.create(pad_begin_y)
            picked = self._loop()
            self._end_curses()
            return picked

        def _end_curses(self):
            """ Terminates the curses application. """
            logger.debug("[TestSearchResult] end curses")
            curses.nocbreak()
            self.window.keypad(0)
            curses.echo()
            curses.endwin()

        def _loop(self):
            current_selected = 0
            textboxes_len = len(self.textboxes)

            if textboxes_len > 1:
                last = 1
            else:
                last = 0

            # See at the root textbox.
            if textboxes_len > 0:
                top_textbox = self.textboxes[0]
                topy, _ = self._refresh_view(top_textbox)
                self.helper.update_attributues(
                    current_selected, last, topy, top_textbox
                )

            while True:
                self.update_view_in_loop()

                try:
                    user_input = self.window.getch()
                except curses.error:
                    continue
                except KeyboardInterrupt:
                    break

                if user_input == curses.KEY_ENTER or user_input == 10:
                    return int(self.current_selected)

                self.handle_key_in_loop(user_input)


if __name__ == "__main__":
    import signal
    import json

    # local

    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    from model import Model
    import runtime.config as runtime_config
    import runtime.opts as runtime_opts
    import utils.color as color

    progname = "gfzs.views.search_result"
    properties = {"progname": progname, "severity": 0, "log_path": "./tmp/gfzs.log"}
    logger.init_properties(**properties)
    logger.debug("start %s" % progname)

    def handle_sigint(signum, frame):
        logger.debug("detect SIGINT (Ctrl-c)")
        logger.debug("exit 0")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_sigint)

    runtime_config.init()
    runtime_opts.init()
    if not runtime_config.valid():
        logger.debug("[print] 'Config is invalid.'")
        print("Config is invalid.")
        for error in runtime_config.errors:
            logger.error(error)
            print("Error: %s" % error)
        logger.debug("exit 1")
        sys.exit(1)

    json_str = open("fixtures/rust.json", "r").read()
    data = json.loads(json_str)

    # initscr() returns a window object representing the entire screen.
    logger.debug("init curses")
    stdscr = curses.initscr()
    color.init()

    # turn off automatic echoing of keys to the screen
    curses.noecho()
    # Enable non-blocking mode. keys are read directly, without hitting enter.
    curses.cbreak()
    # Disable the mouse cursor.
    curses.curs_set(0)

    stdscr.refresh()

    model = Model(data)
    model.update_query("Amazon")
    _ = model.find()

    target = TestSearchResult(stdscr, model)
    error = None
    try:
        choice = target.run(pad_begin_y=1)
        if choice != None:
            enter_result = model.result[choice].get("title")
            logger.debug("Enter Result: '%s'" % enter_result)
            print(enter_result)
    except curses.error as e:
        error = e
    except Exception as e:
        error = e
    finally:
        target._end_curses()
        if error != None:
            logger.error(error)
            print("Error: %s" % error)

        logger.debug("end %s" % progname, new_line=True)
