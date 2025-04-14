## Section Types

### `cmd`  
Runs a command, injecting arguments into `{}` placeholder if present.

| Key   | Description         |
|-------|---------------------|
| `cmd` | Command to run      |

---

### `getcmd`  
Prints the resolved shell command for a task.

| Key     | Description                             |
|---------|-----------------------------------------|
| `getcmd`| Command to evaluate and echo (optional) |

---

### `help`  
Prints a list of tasks.

| Key    | Description       |
|--------|-------------------
| `help` | One sentence help |
| `*kw`  | Help subcommands -> string mapping |

---

### `script`  
Executes the given source code as a script.

| Key      | Description         |
|----------|---------------------|
| `script` | Bash or shell script |

---

### `services`  
Runs `process-compose` with the given services.

| Key       | Description                                      |
|-----------|--------------------------------------------------|
| `services`| Newline-separated service names                  |

---

### `shell`  
Executes a shell snippet using a customizable shell command wrapper.

| Key        | Description                                                        |
|------------|--------------------------------------------------------------------|
| `shell`    | Shell script                                                       |
| `shellcmd` | Template for shell runner (optional, defaults to `sh -exc {} --`)  |

---

### `use`  
Imports and executes another task, passing along keyword arguments.

| Key     | Description                        |
|---------|------------------------------------|
| `use`   | Task name to import                |
| `**kw`  | Additional values passed to task   |

---

## Package Managers

### `venv`  
Sets up a temporary Python virtual environment using `uv` and runs a command inside it.

| Key      | Description                        |
|----------|------------------------------------|
| `venv`   | Python requirements to install     |
| `cmd`    | Command to run inside venv         |
| `python` | Python interpreter path (optional) |

---

### `nix`  
Uses `nix-shell` to run a command in a Nix environment.

| Key   | Description                                              |
|-------|----------------------------------------------------------|
| `nix` | Newline-separated packages                               |
| `cmd` | Command to run in nix-shell (optional, defaults to `{}`) |

---

## Docker Services

### `mysql`

| Key       | Description                               |
|-----------|-------------------------------------------|
| `mysql`   | MySQL image version                       |
| `port`    | Exposed port on host machine (optional)   |
| `user`    | Name of the database user (optional)      |
| `password`| Password for the user (optional)          |
| `db`      | Name of the database to create (optional) |

---

### `redis`

| Key     | Description                             |
|---------|-----------------------------------------|
| `redis` | Redis image version                     |
| `port`  | Exposed port on host machine (optional) |

---

### `postgres`

| Key       | Description                                        |
|-----------|----------------------------------------------------|
| `postgres`| PostgreSQL image version                           |
| `port`    | Exposed port on host machine (optional)            |
| `user`    | Name of the database user (optional)               |
| `password`| Password for the user (optional)                   |
| `db`      | Name of the database to create (optional)          |
| `lang`    | Sets the container's `LANG` env var (optional)     |

---
