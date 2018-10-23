# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import os

from datadog_checks.utils.subprocess_output import get_subprocess_output

DEFAULT_COMMAND_LOCATION = os.path.join('opt', 'mqm', 'bin', 'runmqsc')


def run_mqsc_cmd(cmd, qmanager, username=None, command_path=None, installation_dir=None):
    if not command_path:
        command_path = find_mqsc_cmd(installation_dir)

    command = [
        "echo", cmd, "|", command_path
    ]

    if username:
        command += [
            '-u',
            username
        ]

    command += qmanager

    return get_subprocess_output(command)


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
                      username=None,
                      command_path=None,
                      installation_dir=None):

    command = 'DESCRIBE CHANNEL {}'.format(channel)

    # this is an ugly result
    # TODO: write some regex
    result = run_mqsc_cmd(command,
                          qmanager,
                          username=username,
                          command_path=command_path,
                          installation_dir=installation_dir)
