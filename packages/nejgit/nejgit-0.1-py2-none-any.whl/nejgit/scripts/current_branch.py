import sys
import os


def main(args=sys.argv[1:]):
    gitargs = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
    os.execvp(gitargs[0], gitargs)
