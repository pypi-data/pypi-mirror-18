import concurrent.futures
import json
import logging
import threading
import time
from typing import Optional

import requests

from .dcos import MarathonClient

logger = logging.getLogger('wobble')


def await_deploy(marathon: MarathonClient, app_id: str, deploy_id: str, *,
                 max_spins: int = 10, timeout: Optional[int] = None,
                 cancel: Optional[threading.Event] = None) -> None:
    """
    Wait for the deployment to be confirmed, error cases will be raised
    as exceptions, either DeploySpinningException or DeployTimeoutException

    :param marathon: marathon client
    :param app_id: application id to watch
    :param deploy_id: Deployment ID to wait for
    :param max_spins: Maximum number of detected app task failures for the
    deployment. If met or exceeded before the timeout, an exception will be
    raised.
    :param timeout: Optional timeout before determining the deploy is taking
    :param cancel: Optional threading event you can use to cancel the wait.
    too long.

    :return: None
    """
    if cancel is None:
        cancel = threading.Event()

    # First check that the deploy is actually queued, if it isn't
    # this typically means the new version isn't unique - but marathon
    # doesn't tell us - it's just accepted. This is an edge-case since
    # in most cases - deploys happen during CI
    logger.debug('Checking deploy list to ensure the deploy is queued')
    if not marathon.deploying(deploy_id):
        logger.info('Deployment not in queue, it\'s either already deployed, '
                    'cancelled, or a duplicate. Presuming OK.')
        return
    logger.debug('Deployment enqueued, continuing to wait.')

    logger.info('Connecting to stream')
    event_stream = marathon.events()
    logger.info('Connected, waiting...')

    def cancel_deploy(id_):
        """Cancels the deploy, and waits for it to terminate..."""
        try:
            logger.info('Processing deployment cancellation...')
            rollback = marathon.kill_deployment(id_)
            logger.debug('Rollback ID: "{deploymentId}"; Version: "{version}"'
                         .format(**rollback))

            logger.info('Awaiting rollback, this could take a bit...')
            while True:
                if not marathon.deploying(rollback['deploymentId']):
                    break
                time.sleep(1)
            logger.info('Rollback finished.')
        except requests.HTTPError:
            logger.error('Received error when killing deployment, it may '
                         'require manual intervention')

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as e:
        future = e.submit(_deployment_waiter, event_stream, deploy_id, app_id,
                          max_spins, cancel)

        try:
            if timeout is not None:
                logger.info('Waiting up to %s seconds for deployment',
                            timeout)
            else:
                logger.info('Waiting indefinitely for deployment.')

            try:
                exc = future.exception(timeout=timeout)
                if exc:
                    raise exc
            except concurrent.futures.TimeoutError:
                cancel.set()
                logger.error('Deployment confirmation timed out, cancelling.')
                raise future.exception()

        except (DeploySpinningException, DeployTimeoutException):
            logger.error('Cancelling deployment due to exit')
            cancel_deploy(deploy_id)
            raise


def _deployment_waiter(event_stream: requests.Response, deploy_id: str,
                       app_id: str, max_spins: int,
                       timeout_evt: threading.Event) -> None:
    """
    SSE listener on the marathon event stream, this waits until
    either the maximum amount of spins have been seen (a spin is
    defined as a repeated task failure for the app_id), or the
    timeout_evt is set.

    :param event_stream: Requests streaming response
    :param deploy_id: Deployment ID
    :param app_id: Application ID defined in marathon
    :param max_spins: Maximum number of times a repeated failure is
    seen before it is considered as broken. If this is exceeded a
    DeploySpinningException will be raised
    :param timeout_evt: Threading event, if this is set the function
    will raise a DeployTimeoutException
    :return: None
    """
    current_spin = 0
    for line in event_stream.iter_lines(decode_unicode=True):
        if timeout_evt.is_set():
            logger.debug('Received cancel event, disconnecting SSE.')
            raise DeployTimeoutException

        if not (line and line.startswith('data: ')):
            # Filter out Keep-Alive and non-"data: " messages
            continue

        body = json.loads(line.replace('data: ', ''))

        event_type = body.get('eventType')
        if event_type == 'deployment_step_success':
            plan_id = body.get('plan', {}).get('id', '')
            if plan_id == deploy_id:
                return
        elif event_type == 'status_update_event':
            if body.get('taskStatus') != 'TASK_FAILED':
                continue

            if app_id == body.get('appId'):
                current_spin += 1
                if current_spin == (max_spins / 2):
                    logger.warning('Deployment appears to be boot '
                                   'looping...')
                if current_spin >= max_spins:
                    raise DeploySpinningException('Too many boot-loops')


class MarathonException(Exception):
    """General exception for marathon specific issues"""


class DeploySpinningException(MarathonException):
    """Exception for any deploys that are spinning"""


class DeployTimeoutException(MarathonException):
    """Exception for deploys that timed-out"""
