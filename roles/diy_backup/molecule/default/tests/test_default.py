import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_git_clone(host):
    f = host.file('/opt/atlassian/bitbucket-diy-backup')
    assert f.exists
    assert f.is_directory

def test_diy_config(host):
    f = host.file('/opt/atlassian/bitbucket-diy-backup/bitbucket.diy-backup.vars.sh')
    assert f.exists
