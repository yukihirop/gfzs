## Google Fuzzy Search Example

It is an application made as a draft of `Google Fuzzy Search`.

![image](https://user-images.githubusercontent.com/11146767/104926910-1b473880-59e4-11eb-88d4-a2d729866bfa.png)

## Environment

- python3 (over Python 3.7.4)

## Development

First, create a virtual environment.

```bash
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

## Check

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
