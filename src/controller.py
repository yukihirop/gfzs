import curses
import curses.ascii
import threading

# local

import debug
from box_selector import BoxSelector
from footer import Footer
from colors import Colors
from model import Model
from multibyte import Multibyte

KEY_ENTER = 10
KEY_ESC = 27

class Controller:
    def __init__(self, data):
        self._init_curses()
        self.model = Model(data)
        self.box_selector = BoxSelector(self.stdscr, self.colors, self.model)
        self.footer = Footer(self.stdscr, self.colors, self.model)
        self.multibyte = Multibyte(self.stdscr)
        self.global_lock = threading.Lock()

    def _init_curses(self):
        """ Inits the curses application """
        # initscr() returns a window object representing the entire screen.
        self.stdscr = curses.initscr()
        # turn off automatic echoing of keys to the screen
        curses.noecho()
        # Enable non-blocking mode. keys are read directly, without hitting enter.
        curses.cbreak()
        # Disable the mouse cursor.
        curses.curs_set(0)
        self.stdscr.keypad(1)
        # Enable colorous output.
        self.colors = Colors(curses)
        self.stdscr.bkgd(self.colors.normal)
        self.stdscr.refresh()

    def _end_curses(self):
        """ Terminates the curses application. """
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    def _loop(self) -> int:
        input_mode = True
        user_input = ''
        result_updating_timer = None
        arrow_keys = (self.box_selector.ARROW_DOWN, self.box_selector.ARROW_UP,
                      self.box_selector.ARROW_LEFT, self.box_selector.ARROW_RIGHT)
        
        self.box_selector.create()
        self.box_selector.init_properties_after_create()
        self.box_selector.update_view_in_loop()

        self.footer.create()
        self.footer.activate()

        def search_and_refresh_display(user_input, is_init_property=False, is_init_query=True):
            self.box_selector.reset()

            if is_init_property:
                self.box_selector.init_properties_after_create()
            
            result = self.box_selector.update_view_in_loop()
            
            if is_init_query:
                self.box_selector.update_query('')
            
            if result:
                self.box_selector.handle_key_in_loop(user_input)

        while True:
            if not input_mode:
                self.box_selector.update_view_in_loop()

            try:
                user_input = self.multibyte.getch()
            except curses.error:
                continue
            except KeyboardInterrupt:
                break

            if input_mode:
                if user_input in arrow_keys:
                    input_mode = False
                    search_and_refresh_display(user_input)
                elif user_input == KEY_ESC:
                    pass
                elif user_input == KEY_ENTER:
                    input_mode = False
                    search_and_refresh_display(user_input, is_init_property=True, is_init_query=True)

                # https://www.programcreek.com/python/?code=mingrammer%2Fawesome-finder%2Fawesome-finder-master%2Fawesome%2Ftui.py
                elif user_input in (curses.ascii.BS, curses.ascii.DEL, curses.KEY_BACKSPACE):
                    self.footer.delete_char()
                    search_and_refresh_display(
                        user_input, is_init_property=True, is_init_query=False)
                else:
                    text = chr(user_input)
                    self.footer.write(text)
                    search_and_refresh_display(
                        user_input, is_init_property=True, is_init_query=False)
            else:
                if user_input in arrow_keys:
                    self.box_selector.handle_key_in_loop(user_input)
                elif user_input == KEY_ESC:
                    input_mode = True
                    self.footer.activate()
                elif user_input == KEY_ENTER:
                    self._end_curses()
                    return self.box_selector.current_selected
                else:
                    input_mode = True
                    text = chr(user_input)
                    self.footer.activate()
                    self.footer.write(text)

if __name__ == '__main__':
  import signal
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

  controller = Controller(data)
  choice = controller._loop()
  result = controller.model.result
  if not choice is None:
    print(result[choice].get('title'))
