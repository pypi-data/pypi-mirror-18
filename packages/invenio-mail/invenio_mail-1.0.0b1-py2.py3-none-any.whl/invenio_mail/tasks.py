# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Background tasks for mail module."""

from __future__ import absolute_import, print_function

from celery import shared_task
from flask import current_app
from flask_celeryext import RequestContextTask
from flask_mail import Message


@shared_task(base=RequestContextTask)
def send_email(data):
    """Celery task for sending emails.

    .. warning::

       Due to an incompatibility between MessagePack serialization and Message,
       support for attachments and dates is limited. Consult the tests for
       details.
    """
    msg = Message()
    msg.__dict__.update(data)
    current_app.extensions['mail'].send(msg)
