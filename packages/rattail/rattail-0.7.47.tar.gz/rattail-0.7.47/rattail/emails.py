# -*- coding: utf-8 -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2016 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
#  more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Common email config objects
"""

from __future__ import unicode_literals, absolute_import

import sys
import socket
from traceback import format_exception

from rattail.db import model
from rattail.mail import Email
from rattail.time import localtime


class datasync_error_watcher_get_changes(Email):
    """
    When any datasync watcher thread encounters an error trying to get changes,
    this email is sent out.
    """
    default_subject = "Watcher failed to get changes"

    def sample_data(self, request):
        from rattail.datasync import DataSyncWatcher
        try:
            raise RuntimeError("Fake error for preview")
        except:
            exc_type, exc, traceback = sys.exc_info()
        watcher = DataSyncWatcher(self.config, 'test')
        watcher.consumes_self = True
        return {
            'watcher': watcher,
            'error': exc,
            'traceback': ''.join(format_exception(exc_type, exc, traceback)).strip(),
        }


class filemon_action_error(Email):
    """
    When any filemon thread encounters an error (and the retry attempts have
    been exhausted) then it will send out this email.
    """
    default_subject = "Error invoking action(s)"

    def sample_data(self, request):
        from rattail.filemon import Action
        action = Action(self.config)
        action.spec = 'rattail.filemon.actions:Action'
        action.retry_delay = 10
        try:
            raise RuntimeError("Fake error for preview")
        except:
            exc_type, exc, traceback = sys.exc_info()
        return {
            'hostname': socket.gethostname(),
            'path': '/tmp/foo.csv',
            'action': action,
            'attempts': 3,
            'error': exc,
            'traceback': ''.join(format_exception(exc_type, exc, traceback)).strip(),
        }


class tempmon(object):
    """
    Generic base class for all tempmon-related emails; adds common sample data.
    """
    
    def sample_data(self, request):
        now = localtime(self.config)
        client = model.TempmonClient(config_key='testclient', hostname='testclient')
        probe = model.TempmonProbe(config_key='testprobe', description="Test Probe")
        client.probes.append(probe)
        return {
            'probe': probe,
            'status': self.enum.TEMPMON_PROBE_STATUS[self.enum.TEMPMON_PROBE_STATUS_ERROR],
            'reading': model.TempmonReading(),
            'taken': now,
            'now': now,
        }


class tempmon_critical_temp(tempmon, Email):
    """
    Sent when a tempmon probe takes a reading which is "critical" in either the
    high or low sense.
    """
    default_subject = "Critical temperature detected"
    
    def sample_data(self, request):
        data = super(tempmon_critical_temp, self).sample_data(request)
        data['status'] = self.enum.TEMPMON_PROBE_STATUS[self.enum.TEMPMON_PROBE_STATUS_CRITICAL_TEMP]
        return data


class tempmon_error(tempmon, Email):
    """
    Sent when a tempmon probe is noticed to have some error, i.e. no current readings.
    """
    default_subject = "Probe error detected"
    
    def sample_data(self, request):
        data = super(tempmon_error, self).sample_data(request)
        data['status'] = self.enum.TEMPMON_PROBE_STATUS[self.enum.TEMPMON_PROBE_STATUS_ERROR]
        data['taken'] = None
        return data


class tempmon_high_temp(tempmon, Email):
    """
    Sent when a tempmon probe takes a reading which is above the "maximum good
    temp" range, but still below the "critically high temp" threshold.
    """
    default_subject = "High temperature detected"
    
    def sample_data(self, request):
        data = super(tempmon_high_temp, self).sample_data(request)
        data['status'] = self.enum.TEMPMON_PROBE_STATUS[self.enum.TEMPMON_PROBE_STATUS_HIGH_TEMP]
        return data


class tempmon_low_temp(tempmon, Email):
    """
    Sent when a tempmon probe takes a reading which is below the "minimum good
    temp" range, but still above the "critically low temp" threshold.
    """
    default_subject = "Low temperature detected"

    def sample_data(self, request):
        data = super(tempmon_low_temp, self).sample_data(request)
        data['status'] = self.enum.TEMPMON_PROBE_STATUS[self.enum.TEMPMON_PROBE_STATUS_LOW_TEMP]
        return data
