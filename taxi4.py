import configparser
import sys
import os
import subprocess
import shlex
import tempfile
import stat


def create_docker_type(*, image, image_port, env_prefix=None):
    def docker_type(*, version=None, port=image_port, **rest):
        yield "docker"
        yield "run"
        yield "-ti"
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


def venv_type(*, packages, cmd, python=None):
    yield "uv"
    yield "run"
    yield "--no-project"
    if python:
        yield "--python"
        yield python
    packages = [i for i in packages.splitlines() if i]
    for package in packages:
        yield "--with"
        yield package
    yield "--"
    yield from shlex.split(cmd)


def script_type(*, source):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(source)
    os.chmod(temp_file.name, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)
    yield temp_file.name


types = {
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


config = configparser.ConfigParser()

config.read("taxi.hcl")

run = sys.argv[1]


# for section in config.sections():
#     print(section)
#     breakpoint()

section = config[sys.argv[1]]
section = dict(section)
type_ = section.pop("type")
handler = types[type_]
cmd = handler(**section)
cmd = list(cmd)


print(cmd)
subprocess.call(cmd)
