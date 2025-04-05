import configparser
import sys
import os
import subprocess
import shlex
import tempfile
import stat


def venv_type(*, pkgs, cmd, python=None):
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


def script_type(*, source):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(source)
    os.chmod(temp_file.name, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)
    yield temp_file.name


def cmd_type(*, cmd):
    yield from shlex.split(cmd)


def create_docker_type(*, image, image_port, env_prefix=None):
    def docker_type(*, version=None, port=image_port, **rest):
        yield "docker"
        yield "run"
        # yield "-ti"
        if port:
            yield "-p"
            yield f"{image_port}:{port}"

        if env_prefix:
            for env, env_val in rest.items():
                yield "-e"
                yield f"{env_prefix}{env.upper()}={env_val}"

        if version:
            yield f"{image}:{version}"
        else:
            yield image

    return docker_type


def nix_type(*, pkgs, cmd):
    yield "nix-shell"
    yield "--packages"
    yield from [i for i in pkgs.splitlines() if i]
    yield "--run"
    yield cmd


def raw_type(**kw):
    yield kw


def process_compose_type(*, processes):
    import json

    processes = [i for i in processes.splitlines() if i]
    config = {"version": "0.5", "processes": {}}
    for service in processes:
        cmd = get_command(service)
        config["processes"][service] = {"command": shlex.join(cmd)}
    source = json.dumps(config)
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(source)
    yield "process-compose"
    yield "--config"
    yield temp_file.name


types = {
    "process-compose": process_compose_type,
    "raw": raw_type,
    "nix": nix_type,
    "cmd": cmd_type,
    "script": script_type,
    "venv": venv_type,
    "postgres": create_docker_type(
        image_port=5432,
        image="postgres",
        env_prefix="POSTGRES_",
    ),
    "mysql": create_docker_type(
        image_port=3306,
        image="mysql",
        env_prefix="MYSQL_",
    ),
    "redis": create_docker_type(
        image_port=6379,
        image="redis",
    ),
}


config = configparser.ConfigParser(
    interpolation=configparser.ExtendedInterpolation(),
    # allow_no_value=True,
)


def get_command(name):
    section = config[name]
    section = dict(section)
    type_ = section.pop("type")
    handler = types[type_]
    cmd = handler(**section)
    return list(cmd)


config.read("taxi.ini")
run = sys.argv[1]
cmd = get_command(run)
print(cmd)
subprocess.call(cmd)
