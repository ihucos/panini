import configparser
import sys
import os
import subprocess
import shlex
import tempfile
import stat


def venv_mode(*, venv, pkgs, cmd, python=None):
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


def script_mode(*, script):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(script)
    os.chmod(temp_file.name, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)
    yield temp_file.name


def cmd_mode(*, cmd):
    yield from shlex.split(cmd)


def create_docker_mode(*, image, image_port, env_prefix=None):
    def docker_mode(*, version=None, port=image_port, **rest):
        version = rest.get(image) or "latest"
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

        yield f"{image}:{version}"

    return docker_mode


def nix_mode(*, nix, pkgs, cmd):
    assert nix is None
    yield "nix-shell"
    yield "--packages"
    yield from [i for i in pkgs.splitlines() if i]
    yield "--run"
    yield cmd


def raw_mode(**kw):
    yield kw


def list_mode(*, list=None):
    if list is None:
        list = [section for section in config if section not in ("list", "DEFAULT")]
    else:
        list = [i for i in list.splitlines() if i]
    for task in list:
        cmd = shlex.join(get_command(task))
        print(f"{task:16}{cmd}")
    yield "true"


def services_mode(*, services):
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


modes = {
    "services": services_mode,
    "raw": raw_mode,
    "list": list_mode,
    "nix": nix_mode,
    "cmd": cmd_mode,
    "script": script_mode,
    "venv": venv_mode,
    "postgres": create_docker_mode(
        image_port=5432,
        image="postgres",
        env_prefix="POSTGRES_",
    ),
    "mysql": create_docker_mode(
        image_port=3306,
        image="mysql",
        env_prefix="MYSQL_",
    ),
    "redis": create_docker_mode(
        image_port=6379,
        image="redis",
    ),
}


config = configparser.ConfigParser(
    interpolation=configparser.ExtendedInterpolation(),
    allow_no_value=True,
)


def infer_mode(section_name, section):
    mode = section.get("mode", None)
    if not section:
        return section_name
    if not mode:
        return next(iter(section.keys()))
    return mode


def get_command(name):
    section = config[name]
    section = dict(section)
    mode = infer_mode(name, section)
    section.pop("mode", None)
    handler = modes[mode]
    cmd = handler(**section)
    return list(cmd)


def main():
    config.read("taxi.ini")
    try:
        run = sys.argv[1]
    except IndexError:
        print("missing arg")
        sys.exit(1)
    cmd = get_command(run)
    print(cmd)
    subprocess.call(cmd)


if __name__ == "__main__":
    main()
