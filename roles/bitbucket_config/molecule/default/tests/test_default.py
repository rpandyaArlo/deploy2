import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_config_file(host):
    f = host.file('/media/atl/bitbucket/shared/bitbucket.properties')
    assert f.exists
    assert f.user == 'bitbucket'

    assert f.contains("jdbc.driver=org.postgresql.Driver")
    assert f.contains("jdbc.user=bb_db_user")
    assert f.contains("jdbc.password=molecule_password")
