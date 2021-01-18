import curses
import curses.ascii

# local

try:
  from gfzs import debug
  from gfzs.multibyte import Multibyte
except:
  import debug
  from multibyte import Multibyte

KEY_ENTER = 10
KEY_ESC = 27

class Footer:
  def __init__(self, stdscr, colors, model):
    self.message = 'QUERY>'
    self.stdscr = stdscr
    self.parent_height, self.parent_width = stdscr.getmaxyx()
    self.colors = colors
    self.model = model
    self.multibyte = Multibyte(stdscr)

  @property
  def query(self):
    return self.model.query
  
  def update_query(self, query):
    self.model.update_query(query)

  def create(self):
    self.update_query('')
    self._make_footer()

  def reset(self):
    self._make_footer()
    self.stdscr.move(self.parent_height - 1, len(self.message) + 1 + self.multibyte.get_east_asian_width_count(self.query))
    self.stdscr.refresh()

  def activate(self, is_init=False):
    # Able mouse cursor
    curses.curs_set(1)
    self.stdscr.move(self.parent_height - 1, len(self.message) + 1 + self.multibyte.get_east_asian_width_count(self.query))
    
    if is_init:
      self.stdscr.clrtoeol()
    
    self.stdscr.refresh()

  def delete_char(self):
    if self.query == None or self.query == '':
      self.stdscr.delch(self.parent_height - 1, len(self.message) + 1 + 1)  #?
      self.stdscr.delch(self.parent_height - 1, len(self.message) + 1) #^
    else:
      query_len = self.multibyte.get_east_asian_width_count(self.query)
      if query_len > 0:
        if self.multibyte.is_full_width(self.query[-1]):
          k = 2
        else:
          k = 1
        # backspace = ^?
        self.stdscr.delch(self.parent_height - 1, len(self.message) + 1 + query_len - k + 2) #?
        self.stdscr.delch(self.parent_height - 1, len(self.message) + 1 + query_len - k + 1) #^
        self.stdscr.delch(self.parent_height - 1, len(self.message) + 1 + query_len - k)
        self.update_query(self.query[:-1])
  
  def write(self, text):
    self.stdscr.addstr(text)
    self.model.push_query(text)

  def _wait_input_prompt(self):
    self.create()
    inp = self._loop()
    self._end_curses()
    return inp

  def _end_curses(self, end = True):
    """ Terminates the curses application. """
    curses.nocbreak()
    self.stdscr.keypad(0)
    if end:
      curses.echo()
      curses.endwin()

  # stdscr.getch doesn't work when I addstr to subwin
  def _make_footer(self):
    self.stdscr.hline(self.parent_height - 2, 0, curses.ACS_HLINE | self.colors.hline, self.parent_width)
    self.stdscr.addstr(self.parent_height - 1, 0, self.message, self.colors.footer | curses.A_BOLD)

  def _loop(self):
    self.activate(is_init=True)

    inp = ''
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
        elif user_input in (curses.ascii.BS, curses.ascii.DEL, curses.KEY_BACKSPACE):
          self.delete_char()
          inp = inp[:-1]
        elif user_input == curses.KEY_RESIZE:
          self.reset()
        else:
          self.write(chr(user_input))
          inp += chr(user_input)
          self.update_query(inp)

if __name__ == '__main__':
  import curses
  import signal

  # local

  from colors import Colors
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

  colors = Colors(curses)
  stdscr.bkgd(colors.normal)
  model = Model([])

  inp = Footer(stdscr, colors, model)._wait_input_prompt()
  print('query:', model.query)
  print('result:', inp)
