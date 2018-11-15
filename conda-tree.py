# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from conda.cli.install import calculate_channel_urls
from conda.base.context import context
from conda.common.io import Spinner
from conda.compat import text_type
from conda.core.subdir_data import SubdirData
from conda.models.match_spec import MatchSpec
from conda.models.version import VersionOrder

from conda.cli import main_search
from conda.cli import conda_argparse



PARSER = None

def generate_parser():
    # Generally using `global` is an anti-pattern.  But it's the lightest-weight way to memoize
    # or do a singleton.  I'd normally use the `@memoize` decorator here, but I don't want
    # to copy in the code or take the import hit.
    global PARSER
    if PARSER is not None:
        return PARSER
    PARSER = conda_argparse.generate_parser()
    return PARSER

def execute(args, parser):
    spec = MatchSpec(args.match_spec)
    if spec.get_exact_value('subdir'):
        subdirs = spec.get_exact_value('subdir'),
    elif args.platform:
        subdirs = args.platform,
    else:
        subdirs = context.subdirs

    with Spinner("Loading channels", not context.verbosity and not context.quiet, context.json):
        spec_channel = spec.get_exact_value('channel')
        channel_urls = (spec_channel,) if spec_channel else context.channels

        matches = sorted(SubdirData.query_all(spec, channel_urls, subdirs),
                         key=lambda rec: (rec.name, VersionOrder(rec.version), rec.build))

    if not matches:
        channels_urls = tuple(calculate_channel_urls(
            channel_urls=context.channels,
            prepend=not args.override_channels,
            platform=subdirs[0],
            use_local=args.use_local,
        ))
        from ..exceptions import PackagesNotFoundError
        raise PackagesNotFoundError((text_type(spec),), channels_urls)
    else:
        return matches

def get_spec_string(name,
                    version=None, 
                    channel=None, 
                    platform=None, 
                    build=None):
    kwargs = dict(version=version, channel=channel, subdir=platform, build=build)
    if not kwargs:
        return match_spec.dist_str()
    kwargs = {k:v for k,v in kwargs.items() if v}
    match_spec = MatchSpec(args.name, **kwargs)
    return match_spec.dist_str()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Recursively search the Anaconda repo to build a package dependecy tree.')
    parser.add_argument('name', type=str, 
        help='The name of the package to search for.')
    parser.add_argument('-c', '--channel', default=None,
        help='Search for the package and depencies in this channel. If not specified, the default channels are used.')
    # parser.add_argument('--override_channels', action='store_true', default=False,
    #     help='Do not search default or .condarc channels. Requires --channel')
    parser.add_argument('--version', type=str, default=None,
        help='The version of the package to search.  If not specified, the highest version found is used.')
    parser.add_argument('--platform', type=str, default=None,
        help="Search the given platform. Should be formatted like 'osx-64', 'linux-32', 'win-64', and so on. The default is to search the current platform.")
    parser.add_argument('--build', type=str, default=None,
        help="The build version of the package to search. Should be formatted like 'py27', 'py3', 'py36', and so on. If not specified, the highest build version will be used.")

    # get the args from the command line
    args = parser.parse_args()

    # build the match spec and format the search string
    p = generate_parser()
    a = p.parse_args(['search', args.name])
    spec_str = get_spec_string(args.name, args.version, args.channel, args.platform, args.build)

    context.__init__(argparse_args=a)

    matches = execute(a, p)

    best_match = matches[-1]
    print(best_match.depends)
