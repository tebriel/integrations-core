# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.ibm_mq import IbmMqCheck


def test_check(aggregator, check, instance):
    check = IbmMqCheck('ibm_mq', {}, {})
    check.check(instance)

    aggregator.assert_all_metrics_covered()
