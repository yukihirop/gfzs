# ref: https://github.com/NikolaiT/Scripts/blob/master/scripts/python/curses/text_selector.py

import curses
import unicodedata
import textwrap
import math
import os,sys

# local

try:
  # need when 「python3 gfzs/views/search_result.py」
  if __name__ == '__main__':
    # https://codechacha.com/ja/how-to-import-python-files/
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    from utils.color import Color
    from utils.markup import Markup
    from config.app import AppConfig

    from not_found import NotFound
    from paging import Paging
  # need when 「cat fixtures/rust.json | python -m gfzs」
  # need when 「cat fixtures/rust.json | bin/gfzs」
  else:
    from gfzs.utils.color import Color
    from gfzs.utils.markup import Markup
    from gfzs.config.app import AppConfig

    from gfzs.views.not_found import NotFound
    from gfzs.views.paging import Paging
# need when 「python3 gfzs/controller.py」
except ModuleNotFoundError:
  sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('../'))))
  from utils.color import Color
  from utils.markup import Markup
  from config.app import AppConfig

  from views.not_found import NotFound
  from views.paging import Paging

class SearchResultHelper:
  def __init__(self):
    self.current_selected = 0
    self.last = 1
    self.topy = 1
    self.top_textbox = None
    self.pad_begin_y = 0
    self.per_page = 1
    self.change_page = False

  def update_attributues(self, current_selected, last, topy, top_textbox):
    self.current_selected = current_selected
    self.last = last
    self.topy = topy
    self.top_textbox = top_textbox

  def update_per_page(self, value):
    self.per_page = value

class SearchResult:
  """Display options build from a list of strings in a (unix) terminal.
     The user can browser though the textboxes and select one with enter.
  """

  def __init__(self, stdscr, model):
    """Create a SearchResult object.
       'data' is list of string. Each string is used to build
       a textbox.
    """
    self.stdscr = stdscr
    self.model = model
    self.paging = Paging(stdscr, self)
    self.stop_loop = False
    self.textboxes = []
    self.helper = SearchResultHelper()
    self.not_found = NotFound(stdscr)
    self.markup = Markup()
    self.app_config = AppConfig.get_instance()
    self.color_data = self.app_config.data["view"]["search_result"]["color"]
    self.color = Color.get_instance()
    self.colors = self._create_colors(self.app_config, self.color_data)

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

  def update_per_page(self, value):
    self.helper.update_per_page(value)

  def init_properties_after_create(self):
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

  def create(self, pad_begin_y = 0):
    self.helper.pad_begin_y = pad_begin_y
    self._init_layout()
    self._create_pad()
    self.textboxes = self._make_textboxes()
    if len(self.textboxes) > 0:
      self._refresh_view(self.textboxes[0])
      self.paging.create()

  def destroy(self):
    self._delete_pad()
  
  def update_query(self, query):
    self.model.update_query(query)

  def reset(self):
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
  
  def _create_colors(self, app_config, color_data) -> dict:
    result = {}
    for view_name in color_data:
      result[view_name] = self.color.use(color_data[view_name])

    return result

  def _pick(self, pad_begin_y = 0):
    """ Just run this when you want to spawn the selection process. """
    self.create(pad_begin_y)
    picked = self._loop()
    self._end_curses()

    return picked

  def _init_layout(self):
    self.height, self.width = self.stdscr.getmaxyx()
    # 「2」 is the height of the header or footer
    # 「4」 = header + footer height
    self.window = curses.newwin(self.height - 4, self.width, 2, 0)
    self.update_per_page(self.height//self.TEXTBOX_HEIGHT - 1)
    # https://stackoverflow.com/a/17369532/9434894
    self.window.keypad(1)

  def _finish_curses(self):
    self._end_curses(False)

  def _end_curses(self, end = True):
    """ Terminates the curses application. """
    curses.nocbreak()
    self.window.keypad(0)
    if end:
      curses.echo()
      curses.endwin()

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
    """ Build the textboxes in the pad center and put them in the
        horizontal middle of the pad. """
    textboxes = []
    i = 1
    data = self.model.find()

    if len(data) == 0:
      return textboxes

    for s in data:
        textbox = self.pad.derwin(
            self.TEXTBOX_HEIGHT,
            self.width - 4,
            i + self.helper.pad_begin_y,
            2
        )

        textboxes.append(textbox)
        i += self.TEXTBOX_HEIGHT

    # When all are displayed as multi-byte character strings
    abstract_line_len = self.width//2
    for k in range(len(textboxes)):
        textboxes[k].box()

        title = data[k].get('title')
        url = data[k].get('url')
        abstract = data[k].get('abstract')

        textboxes[k].addstr(2, 2, '%s%-3s' %
                          ('', str(k + 1) + '.'), self.colors["index"])
        textboxes[k].addstr(2, 6, title, self.colors["title"])
        textboxes[k].addstr(3, 6, url, self.colors["url"])
        lines = textwrap.wrap(abstract, abstract_line_len)
        for l in range(len(lines)):
          textboxes[k].addstr(4 + l, 6, lines[l], self.colors["abstract"])

        # Markup Search Query for title
        markup_data = self.markup.parse(title, self.model.query)
        for search_text in markup_data:
          for item in markup_data[search_text]:
            offset_x = item["half_width"]["start_index"]
            color = item["color"]
            match_text = item["match"]
            textboxes[k].addstr(
                2, 6 + offset_x, match_text, color | curses.A_BOLD)
        
        # Markup Search Query for abstract
        for l in range(len(lines)):
          markup_data = self.markup.parse(lines[l], self.model.query)
          for search_text in markup_data:
            for item in markup_data[search_text]:
              offset_x = item["half_width"]["start_index"]
              color = item["color"]
              match_text = item["match"]
              textboxes[k].addstr(4 + l, 6 + offset_x, match_text, color | curses.A_BOLD)

    return textboxes

  def _refresh_view(self, window):
    """ Refresh textboxes """
    cy, cx = window.getbegyx()

    per_page = self.per_page
    display_limit_pos_y = self.TEXTBOX_HEIGHT * per_page
    display_limit_pos_x = self.width - 1
    
    # Since the display of the last pad is cut off, display_limit_pos_y + self.helper.pad_begin_y
    display_limit_pos_y += self.helper.pad_begin_y

    self.pad.refresh(cy, cx, 1 + self.helper.pad_begin_y, 2, display_limit_pos_y, display_limit_pos_x)
    return (cy, cx)

  def update_view_in_loop(self) -> bool:
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
    if ((topy + self.height - self.TEXTBOX_HEIGHT) <= cy):
      top_textbox = textboxes[current_selected]

    # The current window is to far up. There is a better way though...
    # Update the top until you reach the top of the screen.
    if topy >= cy + self.TEXTBOX_HEIGHT:
      if (current_selected < per_page):
        top_textbox = textboxes[0]
      else:
        top_textbox = textboxes[current_selected - per_page]

    if last == 0:
      if (current_selected > per_page + 1):
        top_textbox = textboxes[current_selected- per_page + 1]

    if last != current_selected:
      last = current_selected

    refresh_topy, _ = self._refresh_view(top_textbox)

    if self.helper.change_page:
      self.paging.reset()

    self.textboxes = textboxes

    self.update_per_page(per_page)
    self.helper.update_attributues(
        current_selected, last, refresh_topy, top_textbox)

    return True

  def handle_key_in_loop(self, user_input):
    textboxes = self.textboxes
    textboxes_len = len(textboxes)

    if textboxes_len == 0:
      return

    current_selected = self.current_selected
    per_page = self.per_page

    # Vim like KEY_UP/KEY_DOWN with j(DOWN) and k(UP)
    if textboxes_len > 1 and user_input == curses.KEY_DOWN:
      if (current_selected >= textboxes_len - 1):
        self.helper.change_page = True
        current_selected = 0  # wrap around.
      else:
        current_selected += 1
    elif textboxes_len > 1 and user_input == curses.KEY_UP:
        if current_selected == 0:
          self.helper.change_page = True
          current_selected = textboxes_len - 1  # wrap around.
        else:
          current_selected -= 1
    elif textboxes_len > per_page + 1 and user_input == curses.KEY_RIGHT:
        self.helper.change_page = True
        next_pagetop_index = per_page * (math.ceil(current_selected / per_page) + 1)
        
        if (next_pagetop_index <= textboxes_len-1):
          current_selected = next_pagetop_index
        else:
          current_selected = 0  # wrap around.
    elif textboxes_len > per_page + 1 and user_input == curses.KEY_LEFT:
        self.helper.change_page = True
        current_pagetop_index = per_page * math.floor(current_selected/per_page)
        if (current_pagetop_index <= 0):
          current_selected = textboxes_len - per_page  # wrap around.
        else:
          current_selected = current_pagetop_index - per_page
    elif user_input == curses.KEY_RESIZE:
        self.reset()
    elif user_input in (curses.ascii.BS, curses.ascii.DEL, curses.KEY_BACKSPACE):
        self.reset()
    elif user_input == ord('q'):  # Quit without selecting.
        self.stop_loop = True

    self.helper.current_selected = current_selected

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
      self.helper.update_attributues(current_selected, last, topy, top_textbox)

    while True:
      if self.stop_loop:
        break

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


if __name__ == '__main__':
  import curses
  import signal
  import os, sys
  import json

  # local

  # https://codechacha.com/ja/how-to-import-python-files/
  sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
  from model import Model

  signal.signal(signal.SIGINT, signal.SIG_DFL)

  json_str = open('fixtures/rust.json', 'r').read()
  data = json.loads(json_str)

  # initscr() returns a window object representing the entire screen.
  stdscr = curses.initscr()

  # turn off automatic echoing of keys to the screen
  curses.noecho()
  # Enable non-blocking mode. keys are read directly, without hitting enter.
  curses.cbreak()
  # Disable the mouse cursor.
  curses.curs_set(0)

  stdscr.refresh()
  
  model = Model(data)
  model.update_query('Amazon')
  _ = model.find()

  choice = SearchResult(stdscr, model)._pick(1)
  if choice != None:
    print(model.result[choice].get('title'))
