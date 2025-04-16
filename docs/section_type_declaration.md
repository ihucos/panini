# Section Type Declaration

Every INI section has a section type. The section type is recognised by the following way:

*Does the section has keys? If yes, the section type is the first key. Else its the section name.*

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

