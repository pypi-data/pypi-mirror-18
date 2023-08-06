from conductr_cli import conduct_request, conduct_url, terminal, validation, sandbox_stop, host
from conductr_cli.constants import DEFAULT_SCHEME, DEFAULT_PORT, DEFAULT_BASE_PATH, DEFAULT_API_VERSION
from conductr_cli.http import DEFAULT_HTTP_TIMEOUT
from conductr_cli.sandbox_common import CONDUCTR_NAME_PREFIX, CONDUCTR_DEV_IMAGE, CONDUCTR_PORTS
from conductr_cli.sandbox_features import collect_features
from requests.exceptions import ConnectionError

import logging
import os
import time


# Will retry 30 times, every two seconds
DEFAULT_WAIT_RETRIES = 30
DEFAULT_WAIT_RETRY_INTERVAL = 2.0


# Arguments for conduct requests, such as waiting for ConductR to start in the sandbox
class ConductArgs:

    def __init__(self, vm_type):
        self.ip = host.resolve_ip_by_vm_type(vm_type)

    scheme = DEFAULT_SCHEME
    port = DEFAULT_PORT
    base_path = DEFAULT_BASE_PATH
    api_version = DEFAULT_API_VERSION


@validation.handle_connection_error
@validation.handle_http_error
def run(args):
    """`sandbox run` command"""

    pull_image(args)
    features = collect_features(args.features)
    ports = collect_ports(args, features)
    bootstrap_features = collect_bootstrap_features(features)
    container_names = scale_cluster(args, ports, bootstrap_features)
    is_started, wait_timeout = wait_for_start(args)
    if is_started:
        for feature in features:
            feature.start()
    print_result(container_names, is_started, args.no_wait, wait_timeout)


def pull_image(args):
    if args.image == CONDUCTR_DEV_IMAGE and not terminal.docker_images(CONDUCTR_DEV_IMAGE):
        log = logging.getLogger(__name__)
        log.info('Pulling down the ConductR development image..')
        terminal.docker_pull('{image_name}:{image_version}'
                             .format(image_name=CONDUCTR_DEV_IMAGE, image_version=args.image_version))


def collect_ports(args, features):
    """Return a Set of ports based on the ports of each enabled feature and the ports specified by the user"""

    all_feature_ports = [feature.ports for feature in features]
    return set(args.ports + [port for feature_ports in all_feature_ports for port in feature_ports])


def collect_bootstrap_features(features):
    """Return features that should be enabled in ConductR bootstrap"""

    return [bootstrap_feature
            for bootstrap_features in [feature.bootstrap_features for feature in features]
            for bootstrap_feature in bootstrap_features]


def scale_cluster(args, ports, features):
    sandbox_stop.stop(args)
    return start_nodes(args, ports, features)


def start_nodes(args, ports, features):
    container_names = []
    log = logging.getLogger(__name__)
    log.info('Starting ConductR..')
    for i in range(args.nr_of_containers):
        container_name = '{prefix}{nr}'.format(prefix=CONDUCTR_NAME_PREFIX, nr=i)
        container_names.append(container_name)
        # Display the ports on the command line. Only if the user specifies a certain feature, then
        # the corresponding port will be displayed when running 'sandbox run' or 'sandbox debug'
        if ports:
            host_ip = host.resolve_ip_by_vm_type(args.vm_type)
            ports_desc = ' exposing ' + ', '.join(['{}:{}'.format(host_ip, map_port(i, port))
                                                   for port in sorted(ports)])
        else:
            ports_desc = ''
        log.info('Starting container {container}{port_desc}..'.format(container=container_name,
                                                                      port_desc=ports_desc))
        cond0_ip = inspect_cond0_ip() if i > 0 else None
        conductr_container_roles = resolve_conductr_roles_by_container(args.conductr_roles, i)
        run_conductr_cmd(
            i,
            args.nr_of_containers,
            container_name,
            cond0_ip,
            args.envs,
            '{image}:{version}'.format(image=args.image, version=args.image_version),
            args.log_level,
            ports,
            args.bundle_http_port,
            features,
            conductr_container_roles
        )
    return container_names


def map_port(instance, port):
    current_port_str_rev = ''.join(reversed(str(port)))
    current_second_last_nr = int(current_port_str_rev[1])
    new_second_last_nr = current_second_last_nr if instance == 0 else (current_second_last_nr + instance) % 10
    new_port_str_rev = current_port_str_rev[0] + str(new_second_last_nr) + current_port_str_rev[2:]
    return ''.join(reversed(new_port_str_rev))


def inspect_cond0_ip():
    return terminal.docker_inspect('{}0'.format(CONDUCTR_NAME_PREFIX), '{{.NetworkSettings.IPAddress}}')


def resolve_conductr_roles_by_container(conductr_roles, instance):
    if not conductr_roles:
        # No ConductR roles have been specified => Return an empty Set
        return set()
    elif instance + 1 <= len(conductr_roles):
        # Roles have been specified for the current ConductR instance => Get and use these roles.
        return conductr_roles[instance]
    else:
        # The current ConductR instance is greater than the length of conductr_roles.
        # In this case the roles of conductr_roles are subsequently applied to the remaining instances.
        remainder = (instance + 1) % len(conductr_roles)
        remaining_instance = len(conductr_roles) if remainder == 0 else remainder
        return conductr_roles[remaining_instance - 1]


def run_conductr_cmd(instance, nr_of_instances, container_name, cond0_ip, envs, image, log_level, ports,
                     bundle_http_port, feature_names, conductr_roles):
    general_args = ['-d', '--name', container_name]
    env_args = resolve_docker_run_envs(instance, nr_of_instances, envs, log_level, cond0_ip, feature_names, conductr_roles)
    all_conductr_ports = CONDUCTR_PORTS | {bundle_http_port}
    port_args = resolve_docker_run_port_args(ports | all_conductr_ports, instance)
    optional_args = general_args + env_args + port_args
    additional_optional_args = resolve_conductr_docker_run_opts()
    positional_args = resolve_docker_run_positional_args(cond0_ip)
    terminal.docker_run(optional_args + additional_optional_args, image, positional_args)


def resolve_docker_run_envs(instance, nr_of_instances, envs, log_level, cond0_ip, feature_names, conductr_roles):
    instance_env = ['CONDUCTR_INSTANCE={}'.format(instance), 'CONDUCTR_NR_OF_INSTANCES={}'.format(nr_of_instances)]
    log_level_env = ['AKKA_LOGLEVEL={}'.format(log_level)]
    syslog_ip_env = ['SYSLOG_IP={}'.format(cond0_ip)] if cond0_ip else []
    conductr_features_env = ['CONDUCTR_FEATURES={}'.format(','.join(feature_names))] if feature_names else []
    conductr_roles_env = ['CONDUCTR_ROLES={}'.format(','.join(conductr_roles))] if conductr_roles else []
    all_envs = envs + instance_env + log_level_env + syslog_ip_env + conductr_features_env + conductr_roles_env
    env_args = []
    for env in all_envs:
        env_args.append('-e')
        env_args.append(env)
    return env_args


def resolve_docker_run_port_args(ports, instance):
    port_args = []
    for port in ports:
        port_args.append('-p')
        port_args.append('{external_port}:{internal_port}'.format(external_port=map_port(instance, port),
                                                                  internal_port=port))
    return port_args


def resolve_docker_run_positional_args(cond0_ip):
    seed_node_arg = ['--seed', '{}:{}'.format(cond0_ip, 9004)] if cond0_ip else []
    return ['--discover-host-ip'] + seed_node_arg


def resolve_conductr_docker_run_opts():
    conductr_docker_run_opts = os.getenv('CONDUCTR_DOCKER_RUN_OPTS')
    if conductr_docker_run_opts:
        return conductr_docker_run_opts.split(' ')
    else:
        return []


def stop_nodes(running_containers):
    log = logging.getLogger(__name__)
    log.info('Stopping ConductR nodes..')
    return terminal.docker_rm(running_containers)


def wait_for_start(args):
    if not args.no_wait:
        retries = int(os.getenv('CONDUCTR_SANDBOX_WAIT_RETRIES', DEFAULT_WAIT_RETRIES))
        interval = float(os.getenv('CONDUCTR_SANDBOX_WAIT_RETRY_INTERVAL', DEFAULT_WAIT_RETRY_INTERVAL))
        return wait_for_conductr(args, 0, retries, interval), retries * interval
    else:
        return True, 0


def wait_for_conductr(args, current_retry, max_retries, interval):
    log = logging.getLogger(__name__)
    last_message = 'Waiting for ConductR to start'
    log.progress(last_message, flush=False)
    for attempt in range(0, max_retries):
        time.sleep(interval)

        last_message = '{}.'.format(last_message)
        log.progress(last_message, flush=False)

        conduct_args = ConductArgs(args.vm_type)
        url = conduct_url.url('members', conduct_args)
        try:
            conduct_request.get(dcos_mode=False, host=conduct_args.ip, url=url, timeout=DEFAULT_HTTP_TIMEOUT)
            break
        except ConnectionError:
            current_retry += 1

    # Reprint previous message with flush to go to next line
    log.progress(last_message, flush=True)
    return True if current_retry < max_retries else False


def print_result(container_names, is_started, no_wait, wait_timeout):
    if not no_wait:
        log = logging.getLogger(__name__)
        if is_started:
            log.info('ConductR has been started')
            log.info('Check current bundle status with:')
            log.info('  conduct info')
            plural_string = 's' if len(container_names) > 1 else ''
            log.info('Check resource consumption of Docker container{} that run the ConductR node{} with:'
                     .format(plural_string, plural_string))
            log.info('  docker stats {}'.format(' '.join(container_names)))
        else:
            log.error('ConductR has not been started within {} seconds.'.format(wait_timeout))
            log.error('Set the env CONDUCTR_SANDBOX_WAIT_RETRY_INTERVAL to increase the wait timeout.')
