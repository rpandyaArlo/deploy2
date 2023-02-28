import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_dbconfig_file_for_escaped_ampersand_chars(host):
    f = host.file('/var/atlassian/application-data/jira/dbconfig.xml')
    assert f.exists
    assert f.contains("<password>passwords_with_ampersands_&amp;_should_be_escaped</password>")