import sys
import os

PRETTY_FORMAT = ' '.join([
    '%Cred%h%Creset',
    '%C(yellow)%ai%Creset',
    '-',
    '%s',
    '<%C(bold blue)%ae%Creset>%Cgreen%d%Creset',
])


def main(args=sys.argv[1:]):
    logargs = [
        'git', 'log',
        '--graph',
        '--pretty=format:{}'.format(PRETTY_FORMAT),
    ]
    logargs += args
    os.execvp(logargs[0], logargs)
