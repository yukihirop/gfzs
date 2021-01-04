# ref: https://github.com/NikolaiT/Scripts/blob/master/scripts/python/curses/text_selector.py

import curses
import unicodedata
import textwrap

# local

import debug
from colors import Colors

ARROW_DOWN = 258
ARROW_UP = 259
ARROW_LEFT = 260
ARROW_RIGHT = 261

class BoxSelector:
  """Display options build from a list of strings in a (unix) terminal.
     The user can browser though the textboxes and select one with enter.
  """

  def __init__(self, stdscr, colors, data):
    """Create a BoxSelector object.
       'data' is list of string. Each string is used to build
       a textbox.
    """
    self.stdscr = stdscr
    self.colors = colors
    self.data = data
    # Element parameters. Channge them here.
    self.TEXTBOX_HEIGHT = 8
    self.PAD_WIDTH = 400
    self.PAD_HEIGHT = 1000

  def pick(self):
    """ Just run this when you want to spawn the selection process. """
    self._init_curses()
    self._create_pad()

    windows = self._make_textboxes()
    picked = self._select_textbox(windows)
    self._end_curses()

    return picked

  def _init_curses(self):
    """ Inits the curses application """
    # Something


  def _end_curses(self):
    """ Terminates the curses application. """
    curses.nocbreak()
    self.stdscr.keypad(0)
    curses.echo()
    curses.endwin()


  def _create_pad(self):
    """ Creates a big self.pad to place the textboxes in. """
    self.pad = curses.newpad(self.PAD_HEIGHT, self.PAD_WIDTH)
    self.pad.box()


  def _make_textboxes(self):
    """ Build the textboxes in the pad center and put them in the
        horizontal middle of the pad. """
    # Get the actual screensize.
    maxy, maxx = self.stdscr.getmaxyx()

    windows = []
    i = 1
    for s in self.data:
        window = self.pad.derwin(
            self.TEXTBOX_HEIGHT,
            maxx - 4,
            i,
            2
        )

        windows.append(window)
        i += self.TEXTBOX_HEIGHT
    
    # When all are displayed as multi-byte character strings
    abstract_line_len = maxx//2
    for k in range(len(windows)):
        windows[k].box()
        
        title = self.data[k].get('title')
        url = self.data[k].get('url')
        abstract = self.data[k].get('abstract')

        windows[k].addstr(2, 2, '%s%-3s' % ('', str(k + 1) + '.'), self.colors.index)
        windows[k].addstr(2, 6, title, self.colors.title)
        windows[k].addstr(3, 6, url, self.colors.url)
        lines = textwrap.wrap(abstract, abstract_line_len)
        for l in range(len(lines)):
          windows[k].addstr(4 + l, 6, lines[l], self.colors.abstract)

    return windows

  def _wait_input_prompt(self, footer):
    maxy, _ = self.stdscr.getmaxyx()
    
    self.stdscr.move(maxy - 1, 100)
    footer.refresh()

    c = self.stdscr.getch()

    while True:
      if c == ord('q'):
        break

  def _refresh_view(self, window):
    """ Centers and aligns the view according to the window argument given.
        Returns the(y, x) coordinates of the centered window. """
    cy, cx = window.getbegyx()
    maxy, maxx = self.stdscr.getmaxyx()
    per_page = maxy // self.TEXTBOX_HEIGHT
    display_limit_pos_y = self.TEXTBOX_HEIGHT * (per_page - 1)
    display_limit_pos_x = maxx - 1

    self.pad.refresh(cy, cx, 1, 2, display_limit_pos_y, display_limit_pos_x)
    return (cy, cx)

  def _select_textbox(self, windows):
    # See at the root textbox.
    topy, topx = self._refresh_view(windows[0])
    maxy, maxx = self.stdscr.getmaxyx()

    current_selected = 0
    last = 1
    top_textbox = windows[0]

    while True:
      # Highligth the selected one, the last selected textbox should
      # become normal again.
      windows[current_selected].border(self.colors.highlight)
      windows[last].border()

      # Paging

      # While the textbox can be displayed on the page with the current top_textbox,
      # don't after the view. When this becomes impossible,
      # center the view to last displayable textbox on the previous view.
      cy, cx = windows[current_selected].getbegyx()
      per_page = maxy//self.TEXTBOX_HEIGHT

      # The current window is to far down. Switch the top textbox.
      # When you reach the bottom, redisplay the current box at the top
      if ((topy + maxy - self.TEXTBOX_HEIGHT) <= cy):
        top_textbox = windows[current_selected]

      # The current window is to far up. There is a better way though...
      # Update the top until you reach the top of the screen.
      if topy >= cy + self.TEXTBOX_HEIGHT:
        if (current_selected < per_page - 1):
          top_textbox = windows[0]
        else:
          top_textbox = windows[current_selected - per_page + 1]

      if last != current_selected:
        last = current_selected
      
      topy, topx = self._refresh_view(top_textbox)

      c = self.stdscr.getch()

      # Vim like KEY_UP/KEY_DOWN with j(DOWN) and k(UP)
      if c == ARROW_DOWN:
        if (current_selected >= len(windows)-1):
          current_selected = 0  # wrap around.
        else:
          current_selected += 1
      elif c == ARROW_UP:
        if current_selected <= 0:
          current_selected = len(windows) - 1  # wrap around.
        else:
          current_selected -= 1
      elif c == ARROW_RIGHT:
        next_pagetop_index = (per_page - 1) * \
            (current_selected//(per_page - 1) + 1)
        if (next_pagetop_index <= len(windows)-1):
          current_selected = next_pagetop_index
        else:
          current_selected = 0  # wrap around.
      elif c == ARROW_LEFT:
        current_pagetop_index = (per_page - 1) * \
            (current_selected//(per_page - 1))
        if (current_pagetop_index == 0):
          current_selected = len(windows) - per_page + 1  # wrap around.
        else:
          current_selected = current_pagetop_index - (per_page - 1)
      elif c == ord('q'):  # Quit without selecting.
        break
      # Ah hitting enter, return the index of the selected list element.
      elif c == curses.KEY_ENTER or c == 10:
        return int(current_selected)

if __name__ == '__main__':
  import curses
  import signal

  # local

  from colors import Colors

  signal.signal(signal.SIGINT, signal.SIG_DFL)
  
  data = [
    {
      "abstract": "Rustは非常に高速でメモリ効率が高くランタイムやガベージコレクタがないため、パフォーマンス重視のサービスを実装できますし、組込み機器上で実行したり他の言語との調和も簡単にできます。 信頼性. Rustの豊かな型システムと所有権 ...",
      "matches": [
        {
          "offset": 0,
          "phrase": "Rust"
        },
        {
          "offset": 97,
          "phrase": "Rust"
        }
      ],
      "title": "Rustプログラミング言語",
      "url": "https://www.rust-lang.org/ja"
    },
    {
      "abstract": "Rust（ラスト）はMozillaが支援するオープンソースのシステムプログラミング言語である。 Rust言語は速度、並行性、安全性を言語仕様として保証するC言語、C++に代わるシステムプログラミング（英語版）に適したプログラミング言語を ...",
      "matches": [
        {
          "offset": 0,
          "phrase": "Rust"
        },
        {
          "offset": 48,
          "phrase": "Rust"
        }
      ],
      "metadata": "型付け： 静的型付け、強い型付け、型推論、構造... | 登場時期： 2010年7月7日 | ライセンス： Apache-2.0、MIT License | 影響を受けた言語： Alef、C++、C Sharp、Cyclon...",
      "title": "Rust (プログラミング言語) - Wikipedia",
      "url": "https://ja.wikipedia.org/wiki/Rust_(%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0%E8%A8%80%E8%AA%9E)"
    },
    {
      "abstract": "趣味でRustを使ってコンパイラを作ってるらいパン粉です。 プログラミング言語Rustの良さを雑にあっぴるしていきます。 では、早速cargo run！(このコマンドでRustのプログラムが実行される) C,C++のコードが出てくる ...",
      "matches": [
        {
          "offset": 3,
          "phrase": "Rust"
        },
        {
          "offset": 39,
          "phrase": "Rust"
        },
        {
          "offset": 84,
          "phrase": "Rust"
        }
      ],
      "metadata": "2020/02/04",
      "title": "プログラミング言語Rustのススメ - Qiita",
      "url": "https://qiita.com/elipmoc101/items/3c8b6d8332a9019e578c"
    },
    {
      "abstract": "開発者のRusthへの愛情が、実世界での採用に反映されつつある。2020年6月2日、TIOBEは、初めてRustがTIOBE indexのトップ20に入ったことを発表した。",
      "matches": [
        {
          "offset": 52,
          "phrase": "Rust"
        }
      ],
      "metadata": "2020/07/07",
      "title": "Rustが最も人気のあるプログラミング言語トップ20に - InfoQ",
      "url": "https://www.infoq.com/jp/news/2020/07/rust-top-20-language/"
    },
    {
      "abstract": "開発者向けQ＆Aサイト「Stack Overflow」は、先ごろ発表した年次開発者調査の結果を受け、プログラミング言語「Rust」が人気を集めているさまざまな理由について、ユーザーの生のコメントを紹介した。速度を犠牲にせず ...",
      "matches": [
        {
          "offset": 60,
          "phrase": "Rust"
        }
      ],
      "metadata": "2020/06/11",
      "title": "「Rust」はなぜ人気があるのか、Stack Overflowがユーザーの ...",
      "url": "https://www.atmarkit.co.jp/ait/articles/2006/11/news051.html"
    },
    {
      "abstract": "Rustは「最も愛されている」プログラミング言語として不動の地位を誇っているものの、その普及は遅々として進んでいないようだ。",
      "matches": [
        {
          "offset": 0,
          "phrase": "Rust"
        }
      ],
      "metadata": "2020/05/18",
      "title": "プログラミング言語「Rust」の普及に立ちはだかる壁 - ZDNet ...",
      "url": "https://japan.zdnet.com/article/35153014/"
    },
    {
      "abstract": "AWSはプログラミング言語「Rust」について、同社の長期的な戦略の重要に不可欠なコンポーネントだとしている。",
      "matches": [
        {
          "offset": 14,
          "phrase": "Rust"
        }
      ],
      "metadata": "2020/11/30",
      "title": "AWS、プログラミング言語「Rust」を重視する理由示す ...",
      "url": "https://japan.zdnet.com/article/35163089/"
    },
    {
      "abstract": "AmazonでJim Blandy, Jason Orendorff, 中田 秀基のプログラミングRust。アマゾンならポイント還元本が多数。Jim Blandy, Jason Orendorff, 中田 秀基作品ほか、お急ぎ便対象商品は当日お届けも可能。またプログラミングRustもアマゾン配送 ...",
      "matches": [
        {
          "offset": 49,
          "phrase": "Rust"
        },
        {
          "offset": 137,
          "phrase": "Rust"
        }
      ],
      "title": "プログラミングRust | Jim Blandy, Jason Orendorff, 中田 秀基 ...",
      "url": "https://www.amazon.co.jp/%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0Rust-Jim-Blandy/dp/4873118557"
    },
    {
      "abstract": "オブジェクト指向と関数型の言語特徴を持ち、JavaやC#のようにVM（Virtual Machine）上の動作ではないため、既存のC言語のライブラリを直接扱える利点を持っています。またRustは、CやC++で発生しうる不正メモリアクセスに関する問題 ...",
      "matches": [
        {
          "offset": 92,
          "phrase": "Rust"
        }
      ],
      "title": "プログラミング言語Rust入門 | 増田 智明 |本 | 通販 | Amazon",
      "url": "https://www.amazon.co.jp/%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0%E8%A8%80%E8%AA%9ERust%E5%85%A5%E9%96%80-%E5%A2%97%E7%94%B0-%E6%99%BA%E6%98%8E/dp/4822296857"
    },
    {
      "abstract": "このテキストのこの版では、Rust 2018 Editionのイディオムを使うため、Rust 1.41.0かそれ以降を使っており、すべてのプロジェクトの Cargo.toml に edition=\"2018\" とあることを前提にしています。 Rustをインストールしたりアップデート ...",
      "matches": [
        {
          "offset": 13,
          "phrase": "Rust"
        },
        {
          "offset": 42,
          "phrase": "Rust"
        },
        {
          "offset": 121,
          "phrase": "Rust"
        }
      ],
      "title": "The Rust Programming Language 日本語版 - The Rust ...",
      "url": "https://doc.rust-jp.rs/book-ja/"
    }
  ]

  # initscr() returns a window object representing the entire screen.
  stdscr = curses.initscr()
  # turn off automatic echoing of keys to the screen
  curses.noecho()
  # Enable non-blocking mode. keys are read directly, without hitting enter.
  curses.cbreak()
  # Disable the mouse cursor.
  curses.curs_set(0)
  stdscr.keypad(1)

  colors = Colors(curses)
  stdscr.bkgd(colors.normal)
  stdscr.refresh()

  choice = BoxSelector(stdscr, colors, data).pick()
  print(data[choice].get('title'))
