"""Base argparser module for Pea and Pod runtime"""
import argparse
import os

from ..helper import add_arg_group, _SHOW_ALL_ARGS
from ...enums import PollingType
from ...helper import random_identity


def mixin_base_ppr_parser(parser, with_identity: bool = True):
    """Mixing in arguments required by pea/pod/runtime module into the given parser.
    :param parser: the parser instance to which we add arguments
    :param with_identity: if to include identity in the parser
    """

    gp = add_arg_group(parser, title='Essential')
    gp.add_argument(
        '--name',
        type=str,
        help='''
The name of this object.

This will be used in the following places:
- how you refer to this object in Python/YAML/CLI
- visualization
- log message header
- ...

When not given, then the default naming strategy will apply.
                    ''',
    )

    gp.add_argument(
        '--workspace',
        type=str,
        help='The working directory for any IO operations in this object. '
        'If not set, then derive from its parent `workspace`.',
    )

    from ... import __resources_path__

    gp.add_argument(
        '--log-config',
        type=str,
        default=os.path.join(__resources_path__, 'logging.default.yml'),
        help='The YAML config of the logger used in this object.',
    )

    gp.add_argument(
        '--quiet',
        action='store_true',
        default=False,
        help='If set, then no log will be emitted from this object.',
    )

    gp.add_argument(
        '--quiet-error',
        action='store_true',
        default=False,
        help='If set, then exception stack information will not be added to the log',
    )

    # hidden CLI used for internal only
    if with_identity:
        gp.add_argument(
            '--identity',
            type=str,
            default=random_identity(),
            help='A UUID string to represent the logger identity of this object'
            if _SHOW_ALL_ARGS
            else argparse.SUPPRESS,
        )

    gp.add_argument(
        '--workspace-id',
        type=str,
        default=random_identity(),
        help='the UUID for identifying the workspace. When not given a random id will be assigned.'
        'Multiple Pea/Pod/Flow will work under the same workspace if they share the same '
        '`workspace-id`.'
        if _SHOW_ALL_ARGS
        else argparse.SUPPRESS,
    )

    gp.add_argument(
        '--timeout-ctrl',
        type=int,
        default=int(os.getenv('JINA_DEFAULT_TIMEOUT_CTRL', '60')),
        help='The timeout in milliseconds of the control request, -1 for waiting forever',
    )

    gp.add_argument(
        '--k8s-disable-connection-pool',
        action='store_false',
        dest='k8s_connection_pool',
        default=True,
        help='Defines if connection pooling for replicas should be disabled in K8s. This mechanism implements load balancing between replicas of the same executor. This should be disabled if a service mesh (like istio) is used for load balancing.'
        if _SHOW_ALL_ARGS
        else argparse.SUPPRESS,
    )

    gp.add_argument(
        '--polling',
        type=str,
        default=PollingType.ANY.name,
        help='''
    The polling strategy of the Pod and its endpoints (when `shards>1`).
    Can be defined for all endpoints of a Pod or by endpoint.
    Define per Pod:
    - ANY: only one (whoever is idle) Pea polls the message
    - ALL: all Peas poll the message (like a broadcast)
    Define per Endpoint:
    JSON dict, {endpoint: PollingType}
    {'/custom': 'ALL', '/search': 'ANY', '*': 'ANY'}
    
    ''',
    )
