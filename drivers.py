import shlex
import os
import tempfile
import stat
from utils import get_config, get_command, register


@register
def venv(*, venv, pkgs, cmd, python=None):
    assert venv is None
    yield "uv"
    yield "run"
    yield "--no-project"
    if python:
        yield "--python"
        yield python
    pkgs = [i for i in pkgs.splitlines() if i]
    for pkg in pkgs:
        yield "--with"
        yield pkg
    yield "--"
    yield from shlex.split(cmd)


@register
def script(*, script):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(script)
    os.chmod(temp_file.name, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)
    yield temp_file.name


@register
def cmd(*, cmd):
    yield from shlex.split(cmd)


def _docker(*, version="latest", image, image_port, user_port, envs):
    yield "docker"
    yield "run"
    if version is None:
        version = "latest"
    if user_port is None:
        user_port = image_port

    yield "-p"
    yield f"{image_port}:{user_port}"

    for env, env_val in envs.items():
        if env_val is not None:
            yield "-e"
            yield f"{env.upper()}={env_val}"

    yield f"{image}:{version}"


# return docker


@register
def postgres(*, postgres, port=None, user=None, password=None, db=None, lang=None):
    return _docker(
        version=postgres,
        user_port=port,
        image="postgres",
        image_port=5432,
        envs={
            "POSTGRES_PASSWORD": password,
            "POSTGRES_USER": user,
            "POSTGRES_DB": db,
            "LANG": lang,
        },
    )


@register
def mysql(*, mysql, port=None, user=None, password=None, db=None, lang=None):
    return _docker(
        version=mysql,
        user_port=port,
        image="mysql",
        image_port=3306,
        envs={
            "MYSQL_PASSWORD": password,
            "MYSQL_USER": user,
            "MYSQL_DATABASE": db,
        },
    )


@register
def redis(*, redis, port=None):
    return _docker(
        version=redis,
        user_port=port,
        image="redis",
        image_port=6379,
        envs={},
    )


@register
def nix(*, nix, pkgs, cmd):
    assert nix is None
    yield "nix-shell"
    yield "--packages"
    yield from [i for i in pkgs.splitlines() if i]
    yield "--run"
    yield cmd


@register
def raw(**kw):
    yield kw


@register
def list(*, list=None):
    if list is None:
        list = [section for section in config if section not in ("list", "DEFAULT")]
    else:
        list = [i for i in list.splitlines() if i]
    for task in list:
        cmd = shlex.join(get_command(task))
        print(f"{task:16}{cmd}")
    yield "true"


@register
def services(*, services):
    import json

    services = [i for i in services.splitlines() if i]
    config = {"version": "0.5", "processes": {}}
    for service in services:
        cmd = get_command(service)
        config["processes"][service] = {"command": shlex.join(cmd)}
    source = json.dumps(config)
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(source)
    yield "process-compose"
    yield "--config"
    yield temp_file.name
