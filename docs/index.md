

<img src="assets/panini.png" alt="panini logo" width="175"/>

# Panini



Panini is a delicious mix of tools like `nix`, `docker`, and `process-compose`. Seamlessly
combined via a simple INI file they create a modern development environments with ease.

Or in four words: *Rapid Development Environment Managment.*



## Install

```
pip install panini
```

## Quickstart

Write your own `pan.ini` file.
```ini
[postgres]
postgres=17.4
password=devpass

[redis]

[devbox]
nix=
  process-compose
  uv
  git

[app]
cmd=uv run python3 app.py
via=devbox

[uv]
cmd=uv {}
via=devbox

[up]
services=
    postgres
    redis
    app
via=devbox

[help]
help       = Manage testapp
app        = Start testapp
devbox     = Run something inside nix
postgres   = Start postgrees server
redis      = Start redis server
up         = Run app and dependencies.
uv         = Run uv
```

Now run any of the defined commands, for example:
```
$ panini up
```
<img src="assets/process-compose.png" alt="process-compose terminal" width="width: 100%;"/>


## Congratulations

**You got**

- An isolated, unified, pinnable development environment with minimal dependencies.
- A handy way to organize development specific tasks
- Run your app and dependant services in one command.

**Forget the days of**

- "It works on my machine"
- Containerizing everything, so it fits into `docker-compose`
- Slow test runs because of docker for mac (use nix).
- Huge YAML files nobody understands.
- I weird collection of weird files. One weird file for everything is enough.
