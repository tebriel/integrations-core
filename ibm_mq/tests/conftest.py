# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import os
import time
import pytest

from datadog_checks.dev import docker_run
from datadog_checks.ibm_mq import IbmMqCheck

HERE = os.path.dirname(os.path.abspath(__file__))
COMPOSE_DIR = os.path.join(HERE, 'compose')


@pytest.fixture
def check():
    return IbmMqCheck('ibm_mq', {}, {})


@pytest.fixture
def instance():
    return {
        'channel': 'DEV.ADMIN.SVRCONN',
        'queue_manager': 'datadog',
        'host': 'localhost',
        'port': '1414',
        'username': 'admin',
        'password': 'passw0rd',
        'queues': [
            'DEV.QUEUE.1'
        ]
    }


@pytest.fixture(scope='session')
def spin_up_ibmmq():
    mq_version = os.environ.get('IBM_MQ_VERSION', '9')
    compose_file_name = 'docker-compose-v{}.yml'.format(mq_version)
    env = {
        'COMPOSE_DIR': COMPOSE_DIR
    }

    if mq_version == '9':
        log_pattern = "AMQ5026I: The listener 'DEV.LISTENER.TCP' has started. ProcessId"
    elif mq_version == '8':
        log_pattern = r".*QMNAME\(datadog\)\s*STATUS\(Running\).*"

    with docker_run(
        os.path.join(COMPOSE_DIR, compose_file_name),
        # endpoints='http://localhost:1414',
        env_vars=env,
        log_patterns=log_pattern
    ):
        time.sleep(10)
        yield
