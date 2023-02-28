import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_conf_server_converted(host):
    assert host.file('/media/atl/confluence/shared-home').is_directory
    assert host.file('/media/atl/confluence/shared-home/shared-content.txt').is_file
    assert host.file('/media/atl/confluence/shared-home/attachments').is_directory
    assert host.file('/media/atl/confluence/shared-home/attachments/image.jpg').is_file

    assert not host.file('/media/atl/confluence/shared-home/unwanted.txt').is_file
