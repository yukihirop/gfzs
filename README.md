![gfzs](https://user-images.githubusercontent.com/11146767/105204059-25556c80-5b87-11eb-862e-828a80aa6a94.png)

`Google Fuzzy Search` is a tool for fuzzy find for the result of searching with [googler](https://github.com/jarun/googler).

![gfzs](https://user-images.githubusercontent.com/11146767/105366627-e2f16580-5c42-11eb-92ef-8cd1aa87ce77.gif)

![image](https://user-images.githubusercontent.com/11146767/105366973-47142980-5c43-11eb-89d1-9e24e6a48106.png)

## ⚠ Warning

![alert_tape](https://user-images.githubusercontent.com/11146767/105363618-93f60100-5c3f-11eb-8cb9-4f01ec49b486.png)

If you get the following response, stop using it.
This is an error from `google`. So [you can't do anything with googler](https://github.com/jarun/googler/issues/276#issuecomment-482754595). Please use it after a while.

```
$ googler --json --count 100 python | gfzs
Error: Expecting value: line 1 column 2 (char 1)
Input data: [ERROR] Connection blocked due to unusual activity. THIS IS NOT A BUG, please do NOT report it as a bug unless you have specific information that may lead to the development of a workaround. You IP address is temporarily or permanently blocked by Google and requires reCAPTCHA-solving to use the service, which googler is not capable of. Possible causes include issuing too many queries in a short time frame, or operating from a shared / low reputation IP with a history of abuse. Please do NOT use googler for automated scraping.
```

To avoid such problems, __it is better not to set `googler's count option`.__

__We are not responsible if you ignore the advice and block your IP. please note that.__

![alert_tape](https://user-images.githubusercontent.com/11146767/105363618-93f60100-5c3f-11eb-8cb9-4f01ec49b486.png)

## 🐍 Install

```bash
pip install gfzs
```

or

```bash
pipx instal gfzs
```

## 😎 Demo

seeing is believing.  
You can easily try what kind of app it is.

```bash
gfzs demo
```

## 🌍 Environment

- python3 (over Python 3.6.1)
- poetry

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
    "abstract": "Python is an interpreted, high-level and general-purpose programming language. Python's design philosophy emphasizes code readability with its notable use ...",
    "matches": [
      {
        "offset": 0,
        "phrase": "Python"
      },
      {
        "offset": 79,
        "phrase": "Python's"
      }
    ],
    "metadata": "Developer: Python Software Foundation | Designed by: Guido van Rossum | Filename extensions: .py,.pyi,.pyc,.pyd,.pyo ... | Typing discipline: Duck, dynamic, gradual (since ...",
    "title": "Python (programming language) - Wikipedia",
    "url": "https://en.wikipedia.org/wiki/Python_(programming_language)"
  },
  {
    "abstract": "プログラミング言語 Pythonの紹介・ダウンロードとインストール・Python入門講座など.",
    "matches": [
      {
        "offset": 10,
        "phrase": "Python"
      },
      {
        "offset": 34,
        "phrase": "Python"
      }
    ],
    "title": "プログラミング言語 Python - python.jp",
    "url": "https://www.python.jp/"
  }
]
```

</details>

Pipe as standard input

```bash
cat data.json | gfzs
```

## 🚀 Practical Example (using googler)

__It is recommended to use [alias](https://github.com/yukihirop/gfzs/wiki/%F0%9F%8D%96-Tips) to avoid accidentally passing the -n (--count) option to googler.__

#### Search python articles on github.com

```bash
googler --json --site github.com python | gfzs
```

#### Display only those with a score of 50 or more in the search results

Please see here for [score](https://github.com/seatgeek/fuzzywuzzy).

```bash
googler --json --site github.com python | gfzs -s 50
```

## ⚙ Configure

The default setting is the following file, and each key can enter the following values.  

After changing the settings, you can check if the settings are correct with the `valid` command. 

```bash
$ gfzs valid
Config is valid
```

`~/.gfzsrc`

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

## ⚙ Environment Variable

|name|description|
|----|-----------|
|`DEBUG`|You will be able to use the `debug` module.|
|`EDITOR`|Set the command to open the editor.|

## 💪 Development

First, create a virtual environment.

```bash
$ python3 -m venv .venv
$ poetry shell
$ poetry install
```

```bash
$ python3 gfzs/controller.py
```

or

```bash
$ cat fixtures/python.json | python3 -m gfzs
```

or

```bash
$ cat fixtures/python.json | bin/gfzs
```

## 💪 Development (Check Each View)

### header

```bash
$ python3 gfzs/views/header.py
```

![image](https://user-images.githubusercontent.com/11146767/104927550-ed162880-59e4-11eb-8d5c-efca84c58ea6.png)

### search_result

```bash
$ python3 gfzs/views/search_result.py
```

![image](https://user-images.githubusercontent.com/11146767/104927269-8e50af00-59e4-11eb-8fcf-8b18f4db4420.png)

### paging

```bash
$ python3 gfzs/views/paging.py
```

![image](https://user-images.githubusercontent.com/11146767/104927802-36667800-59e5-11eb-9afb-2b3386c4d8c6.png)

### footer

```bash
$ python3 gfzs/views/footer.py
```

![image](https://user-images.githubusercontent.com/11146767/104927398-b93b0300-59e4-11eb-99a8-5b1e85dc000d.png)


### not_found

```bash
$ python3 gfzs/views/not_found.py
```

![image](https://user-images.githubusercontent.com/11146767/104927669-0d45e780-59e5-11eb-9dc8-76baec0c04ac.png)


## 📚 Reference

I really referred to the implementation of the following repository.

- [mooz/percol](https://github.com/mooz/percol)
- [mingrammer/awesome-finder](https://github.com/mingrammer/awesome-finder)
- [frankdice/fuzzyui](https://github.com/frankdice/fuzzyui)
- [NikolaiT/Scripts](https://github.com/NikolaiT/Scripts/blob/master/scripts/python/curses/text_selector.py)
