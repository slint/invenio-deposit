# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
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

"""Test deposit UI views."""

from __future__ import absolute_import, print_function

from flask import url_for
from invenio_accounts.testutils import login_user_via_session


def test_index_new(app, test_client, users):
    """Test index view."""
    with app.test_request_context():
        index_url = url_for('invenio_deposit_ui.index')
        new_url = url_for('invenio_deposit_ui.new')

    for u in [index_url, new_url]:
        res = test_client.get(u)
        assert res.status_code == 302
        assert '/login/' in res.location

    login_user_via_session(test_client, user=users[0])
    for u in [index_url, new_url]:
        assert test_client.get(u).status_code == 200


def test_edit(app, test_client, users, deposit, db):
    """Test edit view."""
    with app.test_request_context():
        edit_url = url_for(
            'invenio_deposit_ui.depid', pid_value=deposit.pid.pid_value)

    res = test_client.get(edit_url)
    assert res.status_code == 200

    # Test tombstone
    deposit.pid.delete()
    db.session.commit()

    res = test_client.get(edit_url)
    assert res.status_code == 410
