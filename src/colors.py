class Colors:
  def __init__(self, curses):
    self.curses = curses
    self.curses.start_color()
    self._setup()

  def _setup(self):
    curses = self.curses
    self.curses.start_color()
    self.curses.use_default_colors()
    self.curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    self.curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    self.curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    self.curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    self.curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    # https://www.it-swarm-ja.tech/ja/python/curses%E3%81%A7%E7%AB%AF%E6%9C%AB%E3%81%AE%E3%82%AB%E3%83%A9%E3%83%BC%E3%83%91%E3%83%AC%E3%83%83%E3%83%88%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95/1042208550/
    self.curses.init_pair(28, 27, -1) # G(g) color of Google
    self.curses.init_pair(10, 9, -1)  # o(e) color of Google
    self.curses.init_pair(12, 11, -1) # o color of Google
    self.curses.init_pair(36, 35, -1) # l color of Google

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

  @property
  def googler_g(self):
    return self.curses.color_pair(28)

  @property
  def googler_o(self):
    return self.curses.color_pair(10)
  
  @property
  def googler_o2(self):
    return self.curses.color_pair(12)

  @property
  def googler_e(self):
    return self.curses.color_pair(10)

  @property
  def googler_l(self):
    return self.curses.color_pair(36)

  @property
  def googler_r(self):
    return self.curses.color_pair(2)

  @property
  def not_found(self):
    return self.curses.color_pair(4)

if __name__ == '__main__':
  import curses

  colors = Colors(curses)
