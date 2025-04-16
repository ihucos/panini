# Tutorial


## Basics

Panini is very similiar to `make`. The configuration file is in the INI
format. Every section is a command that can be called with `panini cmd`


```ini
; Write this to the file `pan.ini`

[hello]
cmd=printf "hello world\n"
```

```
$ panini hello
hello world
```


One difference to `make` is that there are different *section types*. Here is
an examle using the section type called `venv`.

```ini
[cowsay]
venv=pycowsay
cmd=pycowsay {}
```

```
$ panini cowsay huh?
 ______
< huh? >
 ------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

*Note how `{}` got replaced with the trailing arguments.*

That looks magical at first but with the builtin command `getcmd` we can
inspect what is actually happening there.

```
$ panini getcmd cowsay huh?
uv run --no-project --with pycowsay -- cowsay 'huh?'
```

All the section types do is to generate the actual command that is going to be
executed, based on the users input. You can see all [currently supported
section types here](drivers.md).

## Section Type Declaration

Every INI section has a section type. The section type is recognised by the following way:

**Does the section has keys? If yes, the section type is the first key. Else its the section name**

### Examples

section type: `redis`

```ini
[redis]
```

section type: `script`
```ini
[blah]
script=ls
via=blub
```

Let's look at this error case:

```ini
; wrong
[blah]
via=blub
script=ls
```

Here the section type would be `via`, which does not exist.


## The `via` key

Every section type supports the `via` key, which can be used to chain commands.

```ini
[ssh]
cmd=ssh root@server {}

[nix]
nix=uv
via=ssh

[uv]
cmd=uv {}
via=nix

[myscript]
cmd=run myscript.py {}
via=uv
```

Calling `panini myscript` would run:

```
ssh root@server nix-shell --packages uv --run 'uv run myscript.py'
```

## The `env` key

The `env` key is easy to explain. 

```ini
[envtest]
cmd=printenv FOO
env=
  FOO=123
```

leads to:

```
$ panini envtest
123
$ panini getcmd envtest
env FOO=123 printenv FOO
```

## Conclusion

* Every INI section is a command
* Section types are really just templates to build the command


