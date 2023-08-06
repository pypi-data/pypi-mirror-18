"""
Stuck deployments can be auto-reaped on error (the default). A stuck
deployment is defined as one that is boot-looping or one that cannot
be confidently confirmed within the allotted timeout.

The initial attempt for monitoring listens to the event bus (via SSE),
in which case both timeout and boot-loop detection is enabled.

However if for some reason the SSE stream cannot be connected to - the
fallback is to poll the API for deployments. In this mode only the
timeout mechanism can fire. This simply means that if a deployment is
looping - it won't be reaped until the timeout. The end result is the
same, but the loop may be killed later than it otherwise would have.

Unfortunately, there is no way for wobble to know anything about side-effects
that your application may have performed on boot. If it does database
migrations during the startup process, for example, you will still need
to clean that up (just use the status code of wobble to know if that may
be a possibility).
"""
import contextlib
import json
import logging
import os
import signal
import sys
import threading
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, FileType
from functools import partial

from wobble.wobble import DeploySpinningException, DeployTimeoutException, \
    MarathonClient, await_deploy

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)-20s %(levelname)5s :: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('wobble')


def parse_args():
    """
    Parse and validate the command line arguments
    :return: Parsed and validated arguments namespace
    """
    parser = ArgumentParser(prog='wobble',
                            description='Deployment manager that fires off '
                                        'deploys to DCOS (marathon) and waits'
                                        ' for a deployment confirmation '
                                        'within a timeout.',
                            # epilog=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)

    # Required
    # Note that there is an API specific to marathon, but we are presuming
    # that the user is going through DCOS. For now we are auto-appending
    # the service route through dcos to this url: `/service/marathon`
    parser.add_argument('--dcos-url', type=str,
                        default=os.getenv('WOBBLE_DCOS_URL'),
                        help='DCOS Url, e.g. https://dcos.mycompany.com')

    # Optionals, usually you can rely on the defaults being somewhat sane.
    parser.add_argument('--token', type=str,
                        help='Auth token, if required for DCOS.')
    parser.add_argument('--timeout', type=int,
                        default=int(os.getenv('WOBBLE_TIMEOUT', 300)),
                        help='Maximum amount of time to wait on the '
                             'deployment confirmation, in seconds. Set to '
                             '0 for no timeout.')

    # Note, the implementation detail of this is that the loop count
    # only matters if we are listening to SSEs
    parser.add_argument('--loop-count', type=int,
                        default=int(os.getenv('WOBBLE_MAX_LOOPS', 10)),
                        help='Maximum number of loops before killing the '
                             'boot-looping application.')

    # Allow us to accept stdin if run in a pipe/redirection
    def get_default_marathon_file():
        if sys.stdin.isatty():
            return os.getenv('WOBBLE_MARATHON_FILE', './marathon.json')
        return '-'

    parser.add_argument('--marathon-file', type=FileType('r'),
                        default=get_default_marathon_file(),
                        help='Marathon deployment definition file, can be '
                             'piped from stdin with "-"')

    # https://stackoverflow.com/questions/14097061/easier-way-to-enable-verbose-logging/20663028#20663028
    parser.add_argument('--debug', default=logging.WARNING, dest='loglevel',
                        action='store_const', const=logging.DEBUG,
                        help='Show insane levels of logging, note this may '
                             'print private info')

    parser.add_argument('--verbose', action='store_const', dest='loglevel',
                        const=logging.INFO, help='Show more logging')

    args = parser.parse_args()

    # Since we are checking the envvar as well, we can't simply set
    # required=True on args that are "required" - so they need to be
    # manually checked.
    if not args.dcos_url:
        parser.print_help()
        raise SystemExit(1)

    return args


def main():
    args = parse_args()
    logger.setLevel(args.loglevel)

    try:
        logger.info('Loading marathon config from "%s"',
                    args.marathon_file.name)
        marathon_definition = json.load(args.marathon_file)
    except json.JSONDecodeError as e:
        logger.error('Unable to load marathon definition, bad json: "%s"', e)
        raise SystemExit(1)

    marathon = MarathonClient(args.dcos_url + '/service/marathon',
                              token=args.token)

    app_id = marathon_definition['id']
    logger.info('Starting deploy for app "%s"', app_id)
    logger.debug('Deploying marathon definition: %s', marathon_definition)

    res = marathon.deploy(marathon_definition)
    deploy_id, deploy_version = res['deploymentId'], res['version']
    logger.info('Deployment ID: "%s"; Application Version: "%s"',
                deploy_id, deploy_version)

    # Hacky way to know if the exit reason was interrupt
    # or deployment error.
    interrupted = False

    def on_interrupt(evt: threading.Event, *args):
        nonlocal interrupted
        logger.info('User cancelled, cleaning up.')
        interrupted = True
        evt.set()

    cancel_evt = threading.Event()
    signal.signal(signal.SIGINT, partial(on_interrupt, cancel_evt))

    try:
        await_deploy(marathon, app_id, deploy_id, timeout=args.timeout,
                     max_spins=args.loop_count, cancel=cancel_evt)
    except DeploySpinningException:
        raise SystemExit('\n\n✘✘ Deployment cancelled due to boot looping past'
                         ' the allowed threshold. ✘✘\n\n')
    except DeployTimeoutException:
        if interrupted:
            logger.info('Cleaned up.')
            raise SystemExit
        raise SystemExit('\n\n\t✘✘ Deployment cancelled due to a timeout, '
                         'unable to confirm the deployment within the '
                         'allowed time. ✘✘\n\n')

    print('\n\n\t♥♥♥ Deployment confirmed ♥♥♥\n\n')


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt):
        main()
