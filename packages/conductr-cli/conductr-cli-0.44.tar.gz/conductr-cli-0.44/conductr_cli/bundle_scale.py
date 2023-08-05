from __future__ import unicode_literals
from conductr_cli import conduct_request, conduct_url, sse_client
from conductr_cli.exceptions import WaitTimeoutError
from datetime import datetime
import json
import logging


def get_scale(bundle_id, args):
    bundles_url = conduct_url.url('bundles', args)
    response = conduct_request.get(args.dcos_mode, args.ip, bundles_url)
    response.raise_for_status()
    bundles = json.loads(response.text)
    matching_bundles = [bundle for bundle in bundles if bundle['bundleId'] == bundle_id]
    if matching_bundles:
        matching_bundle = matching_bundles[0]
        if 'bundleExecutions' in matching_bundle:
            started_executions = [bundle_execution
                                  for bundle_execution in matching_bundle['bundleExecutions']
                                  if bundle_execution['isStarted']]
            return len(started_executions)

    return 0


def wait_for_scale(bundle_id, expected_scale, args):
    log = logging.getLogger(__name__)
    start_time = datetime.now()

    bundle_scale = get_scale(bundle_id, args)
    if bundle_scale == expected_scale:
        log.info('Bundle {} expected scale {} is met'.format(bundle_id, expected_scale))
        return
    else:
        sse_heartbeat_count_after_event = 0

        log.info('Bundle {} waiting to reach expected scale {}'.format(bundle_id, expected_scale))
        bundle_events_url = conduct_url.url('bundles/events', args)
        sse_events = sse_client.get_events(args.dcos_mode, args.ip, bundle_events_url)
        for event in sse_events:
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed > args.wait_timeout:
                raise WaitTimeoutError('Bundle {} waiting to reach expected scale {}'.format(bundle_id, expected_scale))

            # Check for bundle scale every 3 heartbeats from the last received event.
            if event.event or (sse_heartbeat_count_after_event % 3 == 0):
                if event.event:
                    sse_heartbeat_count_after_event = 0
                else:
                    sse_heartbeat_count_after_event += 1

                bundle_scale = get_scale(bundle_id, args)
                if bundle_scale == expected_scale:
                    log.info('Bundle {} expected scale {} is met'.format(bundle_id, expected_scale))
                    return
                else:
                    log.info('Bundle {} has scale {}, expected {}'.format(bundle_id, bundle_scale, expected_scale))

        raise WaitTimeoutError('Bundle {} waiting to reach expected scale {}'.format(bundle_id, expected_scale))
