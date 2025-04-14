
```ini
[base-envs]
env
A=1
B=2

[app-envs]
use=base-envs
B=X

[app]
cmd=printenv C
via=app-envs
```
