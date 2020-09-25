# pyoin

`pyoin` is the example programs for [`qoin`](https://github.com/hayashikun/qoin).

## Run

`qoin` is needed to generate proto files, and you have to run `qoin` with server mode to try `pyoin`.

```
$ pip install poetry  # If poetry is not installed.
$ poetry install --no-root
$ poetry run python codegen.py --qoin_path="../qoin"
$ poetry run python app/janken.py
```

## demo
<img src="doc/janken.gif" alt="janken_demo" />
