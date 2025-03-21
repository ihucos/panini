import yaml
import os
import sys

from pprint import pprint
from shlex import quote
import shlex
import argparse
import subprocess
from socket import gethostname


def transpile_stmt(stmt):
    (key,) = stmt.keys()
    (val,) = stmt.values()
    if key == "from":
        return "plash do pull:lxc {}".format(quote(val))
    elif key == "run":
        return "plash do build sh -c {}".format(quote(val))
    elif key == "check":
        return "plash do check {}".format(quote(val))
    assert 0, "no such stmt: " + val


def transpile_build(config, build):
    build_sh = [f"cd {get_remote_project_dir()}", "plash init"]
    stmts = config.get("builds", {})[build]
    for stmt in stmts:
        build_sh.append(transpile_stmt(stmt))
    return build_sh


def transpile_tasks(config):
    tasks = {}
    builds = transpile_builds(config)
    for name, task in config["tasks"].items():
        task_sh = []
        build = task["build"]
        try:
            task_sh = builds[build]
        except KeyError:
            assert 0, "No such build " + build

        for run in task["run"]:
            task_sh.append("plash do run {}".format(quote(run)))

        tasks[name] = task_sh
    return tasks


def read_config(config):
    with open(config, "r") as file:
        config = yaml.safe_load(file)
    return config


def ssh(args, sh):
    ssh_args = get_ssh_args(args)
    cmd = ["ssh", "-t"] + ssh_args + [args.ssh, " && ".join(sh)]
    # pprint(cmd)
    # os.execlp("ssh", cmd)
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as exc:
        print(f"ssh exited with {exc.returncode}", file=sys.stderr)


def cmd_build(args):
    config = read_config(args.config)
    build_sh = transpile_build(config, args.build)
    rsync_up(args)
    ssh(args, build_sh)


def cmd_run(args):
    if not args.cmd:
        cmd = ["sh"]
    else:
        cmd = args.cmd

    config = read_config(args.config)
    build_sh = transpile_build(config, args.build)
    rsync_up(args)
    # assert 0, cmd
    host_cwd = os.getcwd()
    pre = f"mkdir -p {quote(host_cwd)} && mount --bind . {quote(host_cwd)} && cd {quote(host_cwd)}"
    ssh(
        args,
        build_sh + [f"plash do run sh -c '{pre} && exec \"$@\"' _ {shlex.join(cmd)}"],
    )


def cmd_task(args):
    config = read_config(args.config)
    try:
        task_conf = config["tasks"][args.task]
    except KeyError:
        assert 0, "no such task"

    cmd = " && ".join(task_conf["run"])
    build_sh = transpile_build(config, task_conf["build"])
    rsync_up(args)
    ssh(args, build_sh + [f"plash do run sh -c {shlex.join(cmd)}"])


def cmd_list(args):
    config = read_config(args.config)
    for task_name, task_conf in sorted(config.get("tasks", []).items()):
        help = task_conf.get("help", "<no-help>")
        print(f"{task_name:<11} {help}")


def get_ssh_args(args):
    if args.sshopts:
        return shlex.split(args.sshopts)
    elif args.sshport:
        return ["-p", str(args.sshport)]
    return []


def get_remote_project_dir():
    current_dir = os.path.realpath(os.getcwd())
    ino = os.stat(current_dir).st_ino
    return f"~/.taxidata/{gethostname()}/{ino}/"


def rsync_up(args):
    cmd = ["rsync", "--archive", "--delete"]
    ssh_args = get_ssh_args(args)
    if ssh_args:
        cmd.extend(["--rsh", f"ssh {shlex.join(ssh_args)}"])

    project_dir = os.path.dirname(os.path.realpath(args.config))
    cmd.append(project_dir + "/")

    cmd.append(f"{args.ssh}:{get_remote_project_dir()}")
    pprint(cmd)
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as exc:
        print(f"rsync exited with {exc.returncode}", file=sys.stderr)


def rsync_down(ssh, files):
    pass


def build_parser():
    parser = argparse.ArgumentParser(prog="taxi", description="Taxi CLI Tool")
    parser.add_argument("--config", help="YAML file with config", default="Taxi.yaml")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--ssh", help="Connect to, e.G. root@localhost", default="root@localhost"
    )
    group.add_argument("--sshopts", help="Parameter for rsync")
    parser.add_argument("--sshport", help="Which port to connect for", type=int)
    subparsers = parser.add_subparsers(dest="command", required=True)

    # task command
    run_parser = subparsers.add_parser("task", help="Run a task")
    run_parser.add_argument(
        "task",
        help="Task to run",
    )
    run_parser.set_defaults(func=lambda args: cmd_task(args))

    # build command
    task_parser = subparsers.add_parser("build", help="Build a build")
    task_parser.add_argument("build", help="The build to build")
    task_parser.set_defaults(func=lambda args: cmd_build(args))

    # list command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.set_defaults(func=lambda args: cmd_list(args))

    # run command
    run_parser = subparsers.add_parser("run", help="Run a command in a build")
    run_parser.add_argument("build", help="Build to run command in")
    run_parser.add_argument("cmd", nargs=argparse.REMAINDER, help="Command to run")
    run_parser.set_defaults(func=lambda args: cmd_run(args))

    # help command
    help_parser = subparsers.add_parser("help", help="Show help message")
    help_parser.set_defaults(func=lambda _: parser.print_help())

    return parser


def main():
    # Parse arguments
    parser = build_parser()
    default_config = shlex.split(os.environ.get("TAXI", ""))
    # assert 0, default_config
    args = parser.parse_args(default_config + sys.argv[1:])
    args.func(args)


if __name__ == "__main__":
    main()
