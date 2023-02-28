import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('exe', [
    '/usr/bin/ec2-metadata',
    '/usr/bin/amazon-ssm-agent',
    '/sbin/mount.efs'
])
def test_package_exes(host, exe):
    assert host.file(exe).exists

@pytest.mark.parametrize('path', [
    '/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent',
    '/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json'
])
def test_package_not_installed(host, path):
    assert not host.file(path).exists
