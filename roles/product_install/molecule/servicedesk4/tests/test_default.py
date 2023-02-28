import os
from six.moves import urllib

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_version_is_correct(host):
    verfile = host.file('/media/atl/jira/shared/jira-servicedesk.version')
    assert verfile.exists

    assert verfile.content.decode("UTF-8").strip() == "4.1.0"

def test_is_downloaded(host):
    installer = host.file('/media/atl/downloads/servicedesk.4.1.0-x64.bin')
    assert installer.exists
    assert installer.user == 'root'

def test_completed_lockfile(host):
    lockfile = host.file('/media/atl/downloads/servicedesk.4.1.0-x64.bin_completed')
    assert lockfile.exists
    assert lockfile.user == 'root'

def test_is_unpacked(host):
    installer = host.file('/opt/atlassian/jira-servicedesk/4.1.0')
    assert installer.exists
    assert installer.is_directory
    assert installer.user == 'jira'

def test_plugin_is_present(host):
    installer = host.file('/opt/atlassian/jira-servicedesk/current/atlassian-jira/WEB-INF/application-installation/jira-servicedesk-application/jira-servicedesk-application-4.1.0.jar')
    assert installer.exists
    assert installer.user == 'jira'
