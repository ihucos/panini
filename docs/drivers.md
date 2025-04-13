# Section Types

---

### cmd  
Runs a command, injecting arguments into `{}` placeholder if present.

Keys:<br/>


- `cmd` – command to run

---

### getcmd  
Prints the resolved shell command for a task.

Keys:<br/>


- `getcmd` – command to evaluate and echo (optional)

---

### list  
Prints a list of tasks.

Keys:<br/>

- `list` – newline-separated list of task names (optional)

---

### script  
Executes the given source code as a script.

Keys:<br/>

- `script` – bash or shell script

---

### services  
Runs `process-compose` with the given services.

Keys:<br/>

- `services` – newline-separated service names

---

### shell  
Executes a shell snippet using a customizable shell command wrapper.

Keys:<br/>

- `shell` – shell script  
- `shellcmd` – template for shell runner (optional, defaults to `sh -exc {} --`)

---

### use  
Imports and executes another task, passing along keyword arguments.

Keys:<br/>

- `use` – task name to import  
- Additional `**kw` values – passed to the task

---

## Package Managers

### venv  
Sets up a temporary Python virtual environment using `uv` and runs a command inside it.

Keys:<br/>

- `venv` – python requirements to install  
- `cmd` – command to run inside venv  
- `python` – python interpreter path (optional)

---

### nix  
Uses `nix-shell` to run a command in a Nix environment.

Keys:<br/>

- `nix` – newline separated packages  
- `cmd` – command to run in nix-shell (optional, defaults to `{}`)

---


## Docker services

### mysql  
Runs a MySQL Docker container.

Keys:<br/>

- `mysql` – mysql image version  
- `port` – exposed port on host machine (optional)  
- `user` – name of the database user (optional)  
- `password` – password for the user (optional)  
- `db` – name of the database to create (optional)  

---

### redis  
Runs a Redis Docker container.

Keys:<br/>

- `redis` – redis image version  
- `port` – exposed port on host machine (optional)

---

### postgres  
Runs a PostgreSQL Docker container.

Keys:<br/>

- `postgres` – postgres image version  
- `port` – exposed port on host machine (optional)  
- `user` – name of the database user (optional)  
- `password` – password for the user (optional)  
- `db` – name of the database to create (optional)  
- `lang` – sets the container's `LANG` environment variable (optional)

---

