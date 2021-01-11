import curses
import curses.ascii

# local

import debug
from multibyte import Multibyte

KEY_ENTER = 10
KEY_ESC = 27

class Footer:
  def __init__(self, stdscr, colors, model):
    self.message = 'googler (? for help)'
    self.stdscr = stdscr
    self.colors = colors
    self.model = model
    self.multibyte = Multibyte(self.stdscr)

  @property
  def query(self):
    return self.model.query
  
  def update_query(self, query):
    self.model.update_query(query)

  def create(self):
    self._init_curses()
    self._make_footer()

  def activate(self):
    self._init_curses()
    maxy, _ = self.stdscr.getmaxyx()
    self.stdscr.move(maxy - 1, len(self.message) + 1)
    self.stdscr.refresh()

  def delete_char(self):
    maxy, _ = self.stdscr.getmaxyx()

    if self.query == None or self.query == '':
      self.stdscr.delch(maxy - 1, len(self.message) + 1 + 1)  #?
      self.stdscr.delch(maxy - 1, len(self.message) + 1) #^
      self.stdscr.move(maxy - 1, len(self.message) + 1)
    else:
      query_len = len(self.query)
      if query_len > 0:
        # backspace = ^?
        self.stdscr.delch(maxy - 1, len(self.message) + 1 + query_len - 1 + 2) #?
        self.stdscr.delch(maxy - 1, len(self.message) + 1 + query_len - 1 + 1) #^
        self.stdscr.delch(maxy - 1, len(self.message) + 1 + query_len - 1)
        self.stdscr.move(maxy - 1, len(self.message) + 1 + query_len - 1)
        self.update_query(self.query[:-1])

  def _wait_input_prompt(self):
    self.create()
    inp = self._loop()
    self._end_curses()
    return inp

  def _init_curses(self):
    """ Inits the curses application """
    # turn off automatic echoing of keys to the screen
    curses.echo()
    # Buffering off
    # https://docs.python.org/ja/3/library/curses.html#curses.cbreak
    curses.cbreak()
    # Aable the mouse cursor.
    curses.curs_set(1)

  def _finish_curses(self):
    self._end_curses(self, False)

  def _end_curses(self, end = True):
    """ Terminates the curses application. """
    curses.nocbreak()
    self.stdscr.keypad(0)
    curses.echo()
    if end:
      curses.endwin()

  # stdscr.getch doesn't work when I addstr to subwin
  def _make_footer(self):
    maxy, maxx = self.stdscr.getmaxyx()
    self.stdscr.addstr(maxy - 1, 0, self.message, self.colors.prompt)

  def _loop(self):
    self.activate()

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
        else:
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
  colors = Colors(curses)
  stdscr.bkgd(colors.normal)
  model = Model([])

  inp = Footer(stdscr, colors, model)._wait_input_prompt()
  print('query:', model.query)
  print('result:', inp)
