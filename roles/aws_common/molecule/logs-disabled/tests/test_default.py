import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('exe', [
    '/usr/bin/ec2-metadata',
    '/usr/bin/amazon-ssm-agent',
    '/sbin/mount.efs',
    '/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent'
])
def test_package_exes(host, exe):
    assert host.file(exe).exists


def test_service_file(host):
    f = host.file('/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json')
    assert not f.contains('"log_group_name": "jira-software-MY_STACK"')
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o0644
