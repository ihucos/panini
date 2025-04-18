# panini

** Check out the docs here **: https://ihucos.github.io/panini/

Panini is a powerful yet simple way to rapidly define isolated, pinned, and
unified development environments.

```ini
; pan.ini file

[hello-world]
cmd=printf "hello world\n"

[cowsay]
nix=cowsay
cmd=cowsay {}
```

```
$ panini hello-world
hello world

$ panini cowsay hi
 ____
< hi >
 ----
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```
