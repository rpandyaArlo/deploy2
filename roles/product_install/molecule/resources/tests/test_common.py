import os
from six.moves import urllib

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_version_downloaded(host):
    verfile = host.file('/media/atl/jira/shared/jira-core.version')
    assert verfile.exists

def test_symlink_created(host):
    target = host.file('/opt/atlassian/jira-core/current')
    assert target.exists
    assert target.is_symlink

def test_unpacked(host):
    verfile = host.file('/opt/atlassian/jira-core/current/bin/catalina.sh')
    assert verfile.exists
