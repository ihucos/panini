import hcl
from pprint import pprint
import sys
import os
import subprocess


def uv(conf, command):
    yield "uv"
    yield "run"
    if conf.get("no_project"):
        yield "--no-project"
    for with_ in conf.get("with", []):
        yield "--with"
        yield with_
    if python := conf.get("python"):
        yield "--python"
        yield python
    yield "--"
    for cmd in conf.get("command"):
        yield cmd
    for cmd in command:
        yield cmd


def command(conf, command):
    if "envs" in conf:
        yield "env"
        for env, val in conf["envs"].items():
            yield f"{env}={val}"

    for i in conf["command"]:
        yield i
    for cmd in command:
        yield cmd


def docker(conf, command):
    yield "docker"
    yield "run"
    yield "-ti"
    for env, env_val in conf.get("envs", {}).items():
        yield "--env"
        yield f"{env}={env_val}"
    yield conf["image"]


providers = {"uv": uv, "command": command, "docker": docker}
config = hcl.load(open("taxi.hcl"))
pprint(config)

tasks = {}

for provider in config:
    (task_name,) = config[provider].keys()
    conf = config[provider][task_name]
    # print(conf)
    try:
        p = providers[provider]
    except KeyError:
        # print("ingore provider", provider)
        continue
    command = list(p(conf, ["true"]))
    tasks[task_name] = {
        "help": conf.get("help"),
        "get_command": lambda command, conf=conf, p=p: p(conf, command),
    }


cmd = list(tasks[sys.argv[1]]["get_command"](sys.argv[2:]))
print(cmd)
# os.execvp(cmd[0], cmd)
subprocess.run(cmd)
