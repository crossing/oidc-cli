import argparse
import logging

from oidc_cli.provider import Provider, AzureChinaProvider


def setup(args=None):
    parser = _make_parser()
    parse_result = parser.parse_args(args)

    logger = logging.getLogger()
    if parse_result.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)

    provider = _make_provider(parse_result)
    return provider.client_config(parse_result.client_id)


def _make_parser():
    parser = argparse.ArgumentParser(prog='oidc')
    subparsers = parser.add_subparsers(dest='provider', required=True)

    def add_common_arguments(subparser):
        subparser.add_argument('--client-id', '-c', required=True, help='client id')
        subparser.add_argument('--verbose', '-v', required=False, action='store_true')

    generic_parser = subparsers.add_parser('generic', help='Generic Provider')
    generic_parser.add_argument('--issuer', '-i', required=True, help='issuer url')
    add_common_arguments(generic_parser)

    azure_china_parser = subparsers.add_parser('azure_china', help='Azure China')
    azure_china_parser.add_argument('--tenant-id', '-t', required=True, help='Azure China tenant id')
    add_common_arguments(azure_china_parser)

    return parser


def _make_provider(args):
    if args.provider == 'generic':
        return Provider(args.issuer)

    if args.provider == 'azure_china':
        return AzureChinaProvider(args.tenant_id)

    raise ValueError(f'Unknown provider {args.provider}')
