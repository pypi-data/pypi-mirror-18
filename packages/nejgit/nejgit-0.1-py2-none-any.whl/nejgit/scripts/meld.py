import sys
import os


def main(args=sys.argv[1:]):
    myargs = [
        'git', 'difftool',
        '--dir-diff',
        '--tool=meld',
    ]
    myargs += args
    os.execvp(myargs[0], myargs)
