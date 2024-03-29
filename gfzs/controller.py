import curses
import curses.ascii
import webbrowser
import os

# local

try:
    # need when 「cat fixtures/rust.json | python -m gfzs」
    # need when 「cat fixtures/rust.json | bin/gfzs」
    from gfzs.model import Model
    from gfzs.utils.multibyte import Multibyte
    from gfzs.views.header import Header
    from gfzs.views.search_result import SearchResult
    from gfzs.views.footer import Footer
    import gfzs.utils.logger as logger
    import gfzs.utils.color as color

    if os.environ.get("DEBUG"):
        import gfzs.utils.debug as debug

# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
    from model import Model
    from utils.multibyte import Multibyte
    from views.header import Header
    from views.search_result import SearchResult
    from views.footer import Footer
    import utils.logger as logger
    import utils.color as color

    if os.environ.get("DEBUG"):
        import utils.debug as debug

KEY_ENTER = 10
KEY_ESC = 27


class Controller:
    def __init__(self, data):
        logger.debug("[Controller] init")
        self._init_curses()
        self.model = Model(data)
        self.header = Header(self.stdscr)
        self.search_result = SearchResult(self.stdscr, self.model)
        self.footer = Footer(self.stdscr, self.model)
        self.multibyte = Multibyte(self.stdscr)

    def _init_curses(self):
        """ Inits the curses application """
        logger.debug("[Controller] init curses")

        # initscr() returns a window object representing the entire screen.
        self.stdscr = curses.initscr()
        color.init()

        # turn off automatic echoing of keys to the screen
        curses.noecho()
        # Enable non-blocking mode. keys are read directly, without hitting enter.
        curses.cbreak()
        # Able mouse cursor
        curses.curs_set(1)
        self.stdscr.keypad(1)
        # Enable colorous output.
        self.stdscr.refresh()

    def _end_curses(self):
        """ Terminates the curses application. """
        logger.debug("[Controller] end curses")

        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    def _search_and_refresh_display(
        self, user_input, is_init_property=False, is_init_query=True
    ):
        # Disable mouse cursor
        curses.curs_set(0)

        self.search_result.reset()

        if is_init_property:
            self.search_result.init_properties_after_create()

        result = self.search_result.update_view_in_loop()

        if is_init_query:
            logger.debug("[Controller] reset query")
            self.search_result.update_query("")

        if result:
            self.search_result.handle_key_in_loop(user_input)

    def _handle_resize(self, user_input):
        logger.debug("[Controller] detect resize")

        self.header.reset()
        self.footer.reset()
        self._search_and_refresh_display(
            user_input, is_init_property=True, is_init_query=False
        )

    def execute_when_enter(self, current_selected):
        result = self.model.result
        if len(result) != 0:
            url = result[current_selected].get("url")
            webbrowser.open(url, new=2)
            logger.debug("[Controller] detect Enter. open url: %s" % url)
        else:
            logger.debug("[Controller] detect Enter. but result is empty.")

    def run(self) -> int:
        input_mode = True
        user_input = ""
        box_select_begin_y = 2
        arrow_keys = {
            curses.KEY_DOWN: "KEY_DOWN",
            curses.KEY_UP: "KEY_UP",
            curses.KEY_LEFT: "KEY_LEFT",
            curses.KEY_RIGHT: "KEY_RIGHT",
        }
        backspace_keys = {
            curses.ascii.BS: "ASCII_BS",
            curses.ascii.DEL: "ASCII_DEL",
            curses.KEY_BACKSPACE: "KEY_BACKSPACE",
        }

        self.header.create()

        self.search_result.create(box_select_begin_y)
        self.search_result.init_properties_after_create()
        self.search_result.update_view_in_loop()

        self.footer.create()
        self.footer.activate(is_init=True)

        while True:
            # stdscr.refresh is called in the process of updating the query of footer and disappears at that time
            self.header.create()

            if input_mode:
                self.footer.activate()
            else:
                self.search_result.update_view_in_loop()

            try:
                user_input = self.multibyte.getch()
            except curses.error:
                continue
            except KeyboardInterrupt:
                self._end_curses()
                break

            if input_mode:
                logger.debug("[Controller] input mode")
                if user_input in arrow_keys:
                    input_mode = False
                    logger.debug(
                        "[Controller] keyboard input: '%s'" % (arrow_keys[user_input])
                    )
                    self._search_and_refresh_display(user_input, is_init_query=False)
                elif user_input == KEY_ESC:
                    logger.debug("[Controller] keyboard input: 'KEY_ESC' (pass)")
                    pass
                elif user_input == KEY_ENTER:
                    input_mode = False
                    logger.debug(
                        "[Controller] keyboard input: 'KEY_ENTER'. query is '%s'"
                        % (self.model.query)
                    )
                    self._search_and_refresh_display(user_input, is_init_query=False)
                # https://www.programcreek.com/python/?code=mingrammer%2Fawesome-finder%2Fawesome-finder-master%2Fawesome%2Ftui.py
                elif user_input in backspace_keys:
                    if self.model.query == "":
                        pass
                    else:
                        self.footer.delete_char()
                        self._search_and_refresh_display(
                            user_input, is_init_property=True, is_init_query=False
                        )
                elif user_input == curses.KEY_RESIZE:
                    logger.debug("[Controller] keyboard input: 'KEY_RESIZE'")
                    self._handle_resize(user_input)
                # I don't know the reason, but - 1 may come in
                elif user_input == -1:
                    pass
                else:
                    text = chr(user_input)
                    will_query = self.model.query + text
                    if self.model.validate_query(will_query):
                        self.footer.write(text)
                        self._search_and_refresh_display(
                            user_input, is_init_property=True, is_init_query=False
                        )
            else:
                logger.debug("[Controller] input mode")
                if user_input in arrow_keys:
                    self.search_result.handle_key_in_loop(user_input)
                elif user_input == KEY_ESC:
                    logger.debug("[Controller] keyboard input: 'KEY_ESC' (pass)")
                    pass
                elif user_input == KEY_ENTER:
                    self.execute_when_enter(self.search_result.current_selected)
                elif user_input in backspace_keys:
                    logger.debug(
                        "[Controller] keyboard input: '%s'" % backspace_keys[user_input]
                    )
                    input_mode = True
                    self.footer.activate()
                    self.footer.delete_char()
                    self._search_and_refresh_display(
                        user_input, is_init_property=True, is_init_query=False
                    )
                elif user_input == curses.KEY_RESIZE:
                    self._handle_resize(user_input)
                # I don't know the reason, but - 1 may come in
                elif user_input == -1:
                    logger.unknown("[Controller] keyboard input: '-1'")
                    pass
                else:
                    input_mode = True
                    text = chr(user_input)
                    self.footer.activate()
                    self.footer.write(text)


if __name__ == "__main__":
    import json
    import os, sys
    import signal

    # https://note.nkmk.me/python-warnings-ignore-warning/
    import warnings

    warnings.simplefilter("ignore", FutureWarning)

    # local

    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    import runtime.config as runtime_config
    import runtime.opts as runtime_opts

    progname = "gfzs.controller"
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
        logger.debug("[prinnt] Config is invalid.")
        print("Config is invalid.")
        for error in runtime_config.errors:
            logger.error(error)
            print("Error: %s" % error)
        logger.debug("exit 1")
        sys.exit(1)

    json_str = open("fixtures/rust.json", "r").read()
    data = json.loads(json_str)

    error = None
    controller = Controller(data)
    try:
        choice = controller.run()
        result = controller.model.result
        if not choice is None:
            enter_result = result[choice].get("title")
            logger.debug(enter_result)
            print(enter_result)
    except curses.error as e:
        error = str(e)
    finally:
        controller._end_curses()
        if error != None:
            logger.error(error)
            print(error)

        logger.debug("end %s" % progname, new_line=True)
