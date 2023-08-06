# coding=utf-8
import sys
from tox import cmdline


def main():
    sys.argv = ['/usr/local/bin/tox', '-e', 'py35-django184']
    sys.exit(cmdline())


if __name__ == '__main__':
    main()
