import sys
import os
import argparse
import urlparse


def main(args=sys.argv[1:]):
    '''Parse a git url.'''
    opts = parse_args(args)
    print parse_urlish(opts.URL)


def parse_args(args):
    p = argparse.ArgumentParser(description=main.__doc__)
    p.add_argument('URL', help='Git URL.')
    return p.parse_args(args)


def parse_urlish(urlish):
    urlp = urlparse.urlparse(urlish)

    if urlp.scheme in ('http', 'https', 'git', 'ssh'):
        netloc = urlp.netloc
        path = urlp.path

        queryparams = parse_url_query_params(urlp.query)
        path += queryparams.get('p', '')

    elif urlp.scheme == '':
        [userloc, path] = urlp.path.split(':', 1)
        [_, netloc] = userloc.split('@', 1)
    else:
        raise SystemExit(
            'Unsupported URL {0!r} which parses to {1!r}'
            .format(urlish, urlp)
        )

    subdirs = path.rstrip('/').split('/')
    return os.path.join(netloc, *subdirs)


def parse_url_query_params(query):
    if len(query) == 0:
        return {}
    else:
        return dict(kv.split('=', 1) for kv in query.split('&'))
