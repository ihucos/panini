import yaml
import os
import sys

from pprint import pprint
from shlex import quote
import shlex
import argparse
import subprocess
from socket import gethostname


class Job:
    def __init__(self, conf):
        self.conf = conf

    def subprocess_run(self, command):
        subprocess.run(command, check=True)

    def warmup(self):
        self.subprocess_run(self.get_command(["true"]))

    def run(self, command):
        self.subprocess_run(self.get_command([command]))


class Uv(Job):
    def get_command(self, command):
        yield "uv"
        yield "run"
        if self.conf.get("no_project"):
            yield "--no-project"
        for with_ in self.conf.get("with", []):
            yield "--with"
            yield with_
        if python := self.conf.get("python"):
            yield "--python"
            yield python
        yield "--"
        for cmd in command:
            yield cmd


with open("Taxi2.yaml", "r") as file:
    config = yaml.safe_load(file)

print(config)


jobs = {}
for name, conf in config["jobs"]["uv"].tems():
    jobs[name] = Uv(conf)
