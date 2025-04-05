import configparser
import sys
import os
import subprocess
import shlex
import tempfile
import stat


def venv_driver(*, venv, pkgs, cmd, python=None):
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


def script_driver(*, script):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(script)
    os.chmod(temp_file.name, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)
    yield temp_file.name


def cmd_driver(*, cmd):
    yield from shlex.split(cmd)


def create_docker_driver(*, image, image_port, env_prefix=None):
    def docker_driver(*, version=None, port=image_port, **rest):
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

    return docker_driver


def nix_driver(*, nix, pkgs, cmd):
    assert nix is None
    yield "nix-shell"
    yield "--packages"
    yield from [i for i in pkgs.splitlines() if i]
    yield "--run"
    yield cmd


def raw_driver(**kw):
    yield kw


def list_driver(*, list=None):
    if list is None:
        list = [section for section in config if section not in ("list", "DEFAULT")]
    else:
        list = [i for i in list.splitlines() if i]
    for task in list:
        cmd = shlex.join(get_command(task))
        print(f"{task:16}{cmd}")
    yield "true"


def services_driver(*, services):
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


drivers = {
    "services": services_driver,
    "raw": raw_driver,
    "list": list_driver,
    "nix": nix_driver,
    "cmd": cmd_driver,
    "script": script_driver,
    "venv": venv_driver,
    "postgres": create_docker_driver(
        image_port=5432,
        image="postgres",
        env_prefix="POSTGRES_",
    ),
    "mysql": create_docker_driver(
        image_port=3306,
        image="mysql",
        env_prefix="MYSQL_",
    ),
    "redis": create_docker_driver(
        image_port=6379,
        image="redis",
    ),
}


config = configparser.ConfigParser(
    interpolation=configparser.ExtendedInterpolation(),
    allow_no_value=True,
)


def infer_driver_name(section_name, section):
    if not section:
        return section_name
    return next(iter(section.keys()))


def get_command(name):
    section = config[name]
    section = dict(section)
    driver = infer_driver_name(name, section)
    section.pop("driver", None)
    handler = drivers[driver]
    # try:
    cmd = handler(**section)
    # except TypeError as exc:
    #     breakpoint()
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
