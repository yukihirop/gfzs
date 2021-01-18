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

## Check

### box_selector

```bash
$ python3 gfzs/box_selector.py
```

![image](https://user-images.githubusercontent.com/11146767/104927269-8e50af00-59e4-11eb-8fcf-8b18f4db4420.png)

### footer

```bash
$ python3 gfzs/footer.py
```

![image](https://user-images.githubusercontent.com/11146767/104927398-b93b0300-59e4-11eb-99a8-5b1e85dc000d.png)

### header

```bash
$ python3 gfzs/header.py
```

![image](https://user-images.githubusercontent.com/11146767/104927550-ed162880-59e4-11eb-8d5c-efca84c58ea6.png)

### not_found

```bash
$ python3 gfzs/not_found.py
```

![image](https://user-images.githubusercontent.com/11146767/104927669-0d45e780-59e5-11eb-9dc8-76baec0c04ac.png)


### paging

```bash
$ python3 gfzs/paging.py
```

![image](https://user-images.githubusercontent.com/11146767/104927802-36667800-59e5-11eb-9afb-2b3386c4d8c6.png)

