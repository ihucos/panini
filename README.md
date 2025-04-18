# panini

Check out the docs here: https://ihucos.github.io/panini/

Panini is a powerful yet simple way to rapidly define isolated, pinned, and
unified development environments.

```ini
; pan.ini file

[hello]
cmd=hello world

[cowsay]
nix=cowsay
cmd=cowsay {}
```

```
$ panini cowsay hello
```
