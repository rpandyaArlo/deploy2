import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('exe', [
    '/usr/bin/pg_dump',
    '/usr/bin/pg_restore',
    '/usr/bin/psql'
])
def test_postgresql_amazon_linux_extras_exes(host, exe):
    assert host.file(exe).exists

def test_postgresql_version(host):
    pg_dump_version_output = host.check_output('pg_dump --version')
    assert '(PostgreSQL) 9.6' in pg_dump_version_output

@pytest.mark.parametrize('file', [
    '/media/atl/jira/shared',
    '/media/atl/jira/shared/hello',
    '/media/atl/jira/shared/hello/hello.txt'
])
def test_shared_home_owner(host, file):
    assert host.file(file).exists
    assert host.file(file).user == 'jira'
    assert host.file(file).group == 'jira'

def test_file_modes(host):
    assert host.file('/media/atl/jira/shared/hello').mode == 0o755
    assert host.file('/media/atl/jira/shared/hello/hello.txt').mode == 0o640

def test_version_file_owned_by_root(host):
    assert host.file('/media/atl/jira/shared/jira-software.version').exists
    assert host.file('/media/atl/jira/shared/jira-software.version').user == 'root'
    assert host.file('/media/atl/jira/shared/jira-software.version').group == 'root'