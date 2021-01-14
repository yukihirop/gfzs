class Colors:
  def __init__(self, curses):
    self.curses = curses
    self.curses.start_color()
    self._setup()

  def _setup(self):
    curses = self.curses
    self.curses.start_color()
    self.curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    self.curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    self.curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    self.curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    self.curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)

  @property
  def highlight(self):
    return self.curses.color_pair(1)

  @property
  def normal(self):
    return self.curses.color_pair(2)

  @property
  def index(self):
    return self.curses.color_pair(3)

  @property
  def title(self):
    return self.curses.color_pair(4)

  @property
  def url(self):
    return self.curses.color_pair(5)

  @property
  def abstract(self):
    return self.curses.color_pair(2)

  @property
  def footer(self):
    return self.curses.color_pair(4)

if __name__ == '__main__':
  import curses

  colors = Colors(curses)
