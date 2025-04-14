# Local Environment Variables

```ini
[with-secrets]
shell=source .envs && "$@"
shellcmd=sh -ac {} ""

[printsecret]
cmd=printenv SECRET
via=with-secrets
```
