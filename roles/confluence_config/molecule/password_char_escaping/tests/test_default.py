import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_confluence_config_file_for_escaped_ampersand_chars(host):
    f = host.file('/var/atlassian/application-data/confluence/confluence.cfg.xml')
    assert f.exists
    assert f.contains('<property name="hibernate.connection.password">passwords_with_ampersands_&amp;_should_be_escaped</property>')