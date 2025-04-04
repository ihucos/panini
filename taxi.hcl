








[database]
type=postgres
port=3454
password=hello

[database2]
type=mysql


[redis]
type=redis


[pycowsay]
type=venv
packages=
  pycowsay
cmd=pycowsay

[test]
type=script
source=#!/bin/sh
  echo hello world

[app]
type=plash
from=alpine:edge
run=apk update
