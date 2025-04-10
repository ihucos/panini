import sys
import subprocess
import configparser

from .utils import get_config, get_command, TaskError, init_config
from . import drivers as _


def main():
    try:
        run = sys.argv[1]
    except IndexError:
        print('panini error: missing arg, try "list".')
        sys.exit(1)

    try:
        init_config()
        cmd = get_command(run, sys.argv[2:])
    except TaskError as exc:
        print(f"panini error: {exc.args[0]}")
        sys.exit(1)
    except configparser.Error as exc:
        print(f"panini error: parsing: {exc.message}")
        sys.exit(1)
    # print(f"panini is ready: {cmd}")
    subprocess.call(cmd)


if __name__ == "__main__":
    main()
