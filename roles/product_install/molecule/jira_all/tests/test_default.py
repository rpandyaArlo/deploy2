import os
from six.moves import urllib

import testinfra.utils.ansible_runner
import json

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_version_is_correct(host):
    verfile = host.file('/media/atl/jira/shared/jira-software.version')
    assert verfile.exists

    assert verfile.content.decode("UTF-8").strip() == "7.13.1"

def test_is_downloaded(host):
    installer = host.file('/media/atl/downloads/jira-software.7.13.1-x64.bin')
    assert installer.exists
    assert installer.user == 'root'

def test_completed_lockfile(host):
    lockfile = host.file('/media/atl/downloads/jira-software.7.13.1-x64.bin_completed')
    assert lockfile.exists
    assert lockfile.user == 'root'

def test_is_unpacked(host):
    installer = host.file('/opt/atlassian/jira-software/7.13.1/atlassian-jira/')
    assert installer.exists
    assert installer.is_directory
    assert installer.user == 'jira'
    assert installer.mode == 0o0755

def test_obr_is_downloaded(host):
    installer = host.file('/media/atl/downloads/jira-servicedesk-application-3.16.1.obr')
    assert installer.exists
    assert installer.user == 'root'

def test_obr_completed_lockfile(host):
    lockfile = host.file('/media/atl/downloads/jira-servicedesk-application-3.16.1.obr_completed')
    assert lockfile.exists
    assert lockfile.user == 'root'

def test_obr_is_unpacked(host):
    jsdjar = host.file('/media/atl/jira/shared/plugins/installed-plugins/jira-servicedesk-application-3.16.1.jar')
    assert jsdjar.exists
    assert jsdjar.user == 'jira'
    assert jsdjar.mode == 0o0750