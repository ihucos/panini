import sys
import subprocess

from utils import get_config, get_command, TaskError
import drivers


def main():
    try:
        run = sys.argv[1]
    except IndexError:
        print("taxi error: missing arg")
        sys.exit(1)
    try:
        cmd = get_command(run)
    except TaskError as exc:
        print(f"taxi error: {exc.args[0]}")
        sys.exit(1)
    print(cmd)
    subprocess.call(cmd)


if __name__ == "__main__":
    main()
