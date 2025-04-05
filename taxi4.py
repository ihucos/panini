import sys
import subprocess

from utils import get_config, get_command
import drivers


def main():
    try:
        run = sys.argv[1]
    except IndexError:
        print("missing arg")
        sys.exit(1)
    cmd = get_command(run)
    print(cmd)
    subprocess.call(cmd)


if __name__ == "__main__":
    main()
