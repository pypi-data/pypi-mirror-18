from conductr_cli import sandbox_common, terminal
import logging


def stop(args):
    """`sandbox stop` command"""

    log = logging.getLogger(__name__)
    running_containers = sandbox_common.resolve_running_docker_containers()
    if running_containers:
        log.info('Stopping ConductR..')
        terminal.docker_rm(running_containers)
