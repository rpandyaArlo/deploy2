import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_user_prereq(host):
    f = host.file('/usr/sbin/useradd')
    assert f.exists


def test_support_packages(host):
    assert host.file('/usr/bin/jq').exists
    assert host.file('/usr/bin/curl').exists
