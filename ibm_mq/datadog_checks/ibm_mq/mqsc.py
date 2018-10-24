# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import os
import logging

from datadog_checks.utils.subprocess_output import get_subprocess_output

file_log = logging.getLogger(__file__)

DEFAULT_COMMAND_LOCATION = os.path.join('opt', 'mqm', 'bin', 'runmqsc')


def run_mqsc_cmd(cmd,
                 qmanager,
                 log=None,
                 username=None,
                 docker_exec_command=None,
                 command_path=None,
                 installation_dir=None):

    if not log:
        log = file_log

    if not command_path:
        command_path = find_mqsc_cmd(installation_dir)

    command_wrapper = [
        "bash",
        "-c",
    ]

    if docker_exec_command:
        command_wrapper = docker_exec_command + command_wrapper + ['-l']

    command = [
        "echo",
        "'{}'".format(cmd),
        "|"
    ]

    # command path might be a list if it's not just a path,
    # we should account for that possibility
    if isinstance(command_path, list):
        command += command_path
    else:
        command.append(command_path)

    if username:
        command += [
            '-u',
            username
        ]

    command.append(qmanager)

    test_command = command_wrapper + ["echo 'hi'"]

    result = get_subprocess_output(test_command, log, raise_on_empty_output=False)

    log.warning('test command result: {}'.format(result))


    command_wrapper.append(' '.join(command))

    log.warning("command: {}".format(command_wrapper))


    return get_subprocess_output(command_wrapper, log, raise_on_empty_output=False)


def find_mqsc_cmd(installation_dir=None):
    if installation_dir:
        CMD_PATH = os.path.join(installation_dir, 'bin', 'runmqsc')
    else:
        CMD_PATH = None

    # if passed installation_dir and the CMD_PATH is a file, use that
    if installation_dir and os.path.isfile(CMD_PATH):
        return CMD_PATH
    # Check in the default location
    elif os.path.isfile(DEFAULT_COMMAND_LOCATION):
        return DEFAULT_COMMAND_LOCATION
    else:
        # if it's not there, assume it's on the path
        # it's probably not, but it's not a terrible assumption
        return 'runmqsc'


def get_channel_stats(channel,
                      qmanager,
                      log=None,
                      username=None,
                      docker_exec_command=None,
                      command_path=None,
                      installation_dir=None):

    command = 'DESCRIBE CHANNEL {}'.format(channel)

    # this is an ugly result
    # TODO: write some regex
    result, error, retcode = run_mqsc_cmd(command,
                                          qmanager,
                                          username=username,
                                          command_path=command_path,
                                          docker_exec_command=docker_exec_command,
                                          installation_dir=installation_dir)

    return (result, error, retcode)
