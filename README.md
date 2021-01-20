![gfzs](https://user-images.githubusercontent.com/11146767/105204059-25556c80-5b87-11eb-862e-828a80aa6a94.png)

`Google Fuzzy Search` is a tool for fuzzy find for the result of searching with [googler](https://github.com/jarun/googler).

![image](https://user-images.githubusercontent.com/11146767/104926910-1b473880-59e4-11eb-88d4-a2d729866bfa.png)

## 🐍 Install

```bash
pip install gfzs
```

or

```bash
brew tap yukihirop/homebrew-tap
brew install gfzs
```

## 🌍 Environment

- python3 (over Python 3.7.4)
- black(Formatter) (version 20.8b1)

## 📖 Usage

Initialize first. A configuration file (`.gfzsrc`) is created in your home directory.

```bash
$ gfzs init
Initialize config in /Users/yukihirop/.gfzsrc
```

Next, Prepare json with `title`, `url` and `abstract` as keys and pass it.
For Example, Assuming that data.json is as follows.

`data.json`

<details>

```json
[
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
  }
]
```

</details>

Pipe as standard input

```bash
cat data.json | gfzs
```

## 🚀 Practical Example (using googler)

#### Search 100 python articles on github.com

```bash
googler --json --count 100 --site github.com python | gfzs
```

#### Display only those with a score of 50 or more in the search results

Please see here for [score](https://github.com/seatgeek/fuzzywuzzy).

```bash
googler --json --count 100 --site github.com python | gfzs -s 50
```

## ⚙ Configure

The default setting is the following file, and each key can enter the following values.

`.gfzsrc (default)`

<details>

```json
{
  "view": {
    "footer": {
      "message": "QUERY>",
      "color": {
        "message": {
          "text": 2,
          "background": 0,
          "style": "normal"
        },
        "hline": {
          "text": 7,
          "background": 0,
          "style": "normal"
        }
      }
    },
    "header": {
      "color": {
        "hline": {
          "text": 7,
          "background": 0,
          "style": "normal"
        }
      }
    },
    "search_result": {
      "color": {
        "index": {
          "text": 6,
          "background": 0,
          "style": "normal"
        },
        "title": {
          "text": 2,
          "background": 0,
          "style": "bold"
        },
        "url": {
          "text": 3,
          "background": 0,
          "style": "link"
        },
        "abstract": {
          "text": 7,
          "background": 0,
          "style": "normal"
        },
        "markup_partial": {
          "text": 2,
          "background": 5,
          "style": "normal"
        },
        "markup_char": {
          "text": 1,
          "background": 0,
          "style": "normal"
        }
      }
    },
    "paging": {
      "color": {
        "common": {
          "text": 2,
          "background": 0,
          "style": "bold"
        }
      }
    }
  }
}
```

</details>

|key|description|value|
|---|-----------|-----|
|<kbd>text</kbd>|curses color|`0〜7`|
|<kbd>background</kbd>|curses color|`0〜7`|
|<kbd>style</kbd>|text style|`"normal", "link", "bold"`|

### curses color

|number|description|
|------|-----------|
|`0`|`curses.COLOR_BLACK`|
|`1`|`curses.COLOR_RED`|
|`2`|`curses.COLOR_GREEN`|
|`3`|`curses.COLOR_YELLOW`|
|`4`|`curses.COLOR_BLUE`|
|`5`|`curses.COLOR_MAGENTA`|
|`6`|`curses.COLOR_CYAN`|
|`7`|`curses.COLOR_WHITE`|

## 💪 Development

First, create a virtual environment.

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
```

```bash
$ python3 gfzs/controller.py
```

or

```bash
$ cat fixtures/rust.json | python3 -m gfzs
```

or

```bash
$ cat fixtures/rust.json | bin/gfzs
```

## 💪 Development (Check Partial View)

### search_result

```bash
$ python3 gfzs/views/search_result.py
```

![image](https://user-images.githubusercontent.com/11146767/104927269-8e50af00-59e4-11eb-8fcf-8b18f4db4420.png)

### footer

```bash
$ python3 gfzs/views/footer.py
```

![image](https://user-images.githubusercontent.com/11146767/104927398-b93b0300-59e4-11eb-99a8-5b1e85dc000d.png)

### header

```bash
$ python3 gfzs/views/header.py
```

![image](https://user-images.githubusercontent.com/11146767/104927550-ed162880-59e4-11eb-8d5c-efca84c58ea6.png)

### not_found

```bash
$ python3 gfzs/views/not_found.py
```

![image](https://user-images.githubusercontent.com/11146767/104927669-0d45e780-59e5-11eb-9dc8-76baec0c04ac.png)


### paging

```bash
$ python3 gfzs/views/paging.py
```

![image](https://user-images.githubusercontent.com/11146767/104927802-36667800-59e5-11eb-9afb-2b3386c4d8c6.png)

## 📚 Reference

I really referred to the implementation of the following repository.

- [mooz/percol](https://github.com/mooz/percol)
- [mingrammer/awesome-finder](https://github.com/mingrammer/awesome-finder)
- [frankdice/fuzzyui](https://github.com/frankdice/fuzzyui)
- [NikolaiT/Scripts](https://github.com/NikolaiT/Scripts/blob/master/scripts/python/curses/text_selector.py)
