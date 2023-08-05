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

"""Test example app."""

import json
import os
import signal
import subprocess
import time

import pytest


@pytest.yield_fixture
def example_app():
    """Example app fixture."""
    current_dir = os.getcwd()
    # go to example directory
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    exampleappdir = os.path.join(project_dir, 'examples')
    os.chdir(exampleappdir)
    # setup example
    cmd = './app-setup.sh'
    exit_status = subprocess.call(cmd, shell=True)
    assert exit_status == 0
    # setup example
    cmd = './app-fixtures.sh'
    exit_status = subprocess.call(cmd, shell=True)
    assert exit_status == 0
    time.sleep(10)
    # return webapp
    yield exit_status
    # tear down example app
    cmd = './app-teardown.sh'
    subprocess.call(cmd, shell=True)
    # return to the original directory
    os.chdir(current_dir)


def test_example_app(example_app):
    """Test example app."""
    cmd = 'curl -X GET localhost:9200/_cat/indices?v'
    output = subprocess.check_output(cmd, shell=True).decode('utf-8')
    assert 'testrecords-testrecord-v1.0.0' in output
    cmd = 'curl -X GET localhost:9200/testrecords-testrecord-v1.0.0/_search'
    output = json.loads(
        subprocess.check_output(cmd, shell=True).decode('utf-8'))
    assert len(output['hits']['hits']) == 10
