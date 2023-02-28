import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_slingshot_installed(host):
    assert host.file('/usr/bin/atlassian-slingshot').exists
    assert host.file('/usr/bin/psql').exists
