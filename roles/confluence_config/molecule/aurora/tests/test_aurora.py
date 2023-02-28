import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_seraph_file(host):
    f = host.file('/opt/atlassian/confluence/current/confluence/WEB-INF/classes/seraph-config.xml')
    assert f.exists
    assert f.contains('<param-value>COOKIEAGE</param-value>')

def test_conf_init_file(host):
    f = host.file('/opt/atlassian/confluence/current/confluence/WEB-INF/classes/confluence-init.properties')
    assert f.exists
    assert f.contains('confluence.home = /var/atlassian/application-data/confluence')

def test_setenv_file(host):
    f = host.file('/opt/atlassian/confluence/current/bin/setenv.sh')
    assert f.exists
    assert f.contains('-XmsPLACEHOLDER')
    assert f.contains('-XmxPLACEHOLDER')
    assert f.contains('-Dconfluence.cluster.node.name=1.1.1.1')

def test_server_file(host):
    f = host.file('/opt/atlassian/confluence/current/conf/server.xml')
    assert f.exists
    assert f.contains('Connector port="8080"')
    assert f.contains('Server port="8005"')
    assert f.contains('<Context path=""')
    assert f.contains('maxThreads="200"')
    assert f.contains('minSpareThreads="10"')
    assert f.contains('connectionTimeout="20000"')
    assert f.contains('enableLookups="false"')
    assert f.contains('protocol="HTTP/1.1"')
    assert f.contains('redirectPort=""')
    assert f.contains('acceptCount="10"')
    assert f.contains('secure="false"')
    assert f.contains('scheme="http"')
    assert not f.contains('proxyName=')
    assert not f.contains('proxyPort=')

def test_install_permissions(host):
    assert host.file('/opt/atlassian/confluence/current/conf/server.xml').user == 'root'
    assert host.file('/opt/atlassian/confluence/current/confluence/WEB-INF/web.xml').user == 'root'

    assert host.file('/opt/atlassian/confluence/current/logs/').user == 'confluence'
    assert host.file('/opt/atlassian/confluence/current/work/').user == 'confluence'
    assert host.file('/opt/atlassian/confluence/current/temp/').user == 'confluence'

@pytest.mark.parametrize('directory', [
    '/var/atlassian/application-data/confluence/',
    '/media/atl/confluence/shared-home/'
])
def test_home_directories(host, directory):
    d = host.file(directory)
    assert d.exists
    assert d.user == 'confluence'

def test_confluence_config_file(host):
    f = host.file('/var/atlassian/application-data/confluence/confluence.cfg.xml')
    assert f.exists
    assert f.user == 'confluence'
    assert f.contains('<property name="confluence.cluster.home">/media/atl/confluence/shared-home</property>')
    assert f.contains('<property name="hibernate.connection.driver_class">org.postgresql.Driver</property>')
    assert f.contains('<property name="confluence.cluster.aws.host.header">ec2.amazonaws.com</property>')
    assert f.contains('<property name="hibernate.connection.url">jdbc:postgresql://aurora-postgres-db.ap-southeast-2.rds.amazonaws.com:5432/confluence?targetServerType=master</property>')
