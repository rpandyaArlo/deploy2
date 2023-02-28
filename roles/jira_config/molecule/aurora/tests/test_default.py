import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_dbconfig_file(host):
    f = host.file('/var/atlassian/application-data/jira/dbconfig.xml')
    assert f.exists
    assert f.user == 'jira'
    assert f.contains("<database-type>postgresaurora96</database-type>")
    assert f.contains("<driver-class>org.postgresql.Driver</driver-class>")
    assert f.contains("<username>atljira</username>")
    assert f.contains("<password>molecule_password</password>")

    assert f.contains("<pool-min-size>1111</pool-min-size>")
    assert f.contains("<pool-max-size>1111</pool-max-size>")
    assert f.contains("<pool-min-idle>1111</pool-min-idle>")
    assert f.contains("<pool-max-idle>1111</pool-max-idle>")

    assert f.contains("<pool-max-wait>1111</pool-max-wait>")
    assert f.contains("<min-evictable-idle-time-millis>1111</min-evictable-idle-time-millis>")
    assert f.contains("<pool-remove-abandoned>false</pool-remove-abandoned>")
    assert f.contains("<time-between-eviction-runs-millis>1111</time-between-eviction-runs-millis>")
    assert f.contains("<min-evictable-idle-time-millis>1111</min-evictable-idle-time-millis>")
    assert f.contains("<pool-remove-abandoned>false</pool-remove-abandoned>")
    assert f.contains("<pool-remove-abandoned-timeout>1111</pool-remove-abandoned-timeout>")
    assert f.contains("<pool-test-while-idle>false</pool-test-while-idle>")
    assert f.contains("<pool-test-on-borrow>true</pool-test-on-borrow>")


def test_setenv_file(host):
    f = host.file('/opt/atlassian/jira-software/current/bin/setenv.sh')
    assert f.exists
    assert f.contains('^JVM_MINIMUM_MEMORY="PLACEHOLDER"')
    assert f.contains('^JVM_MAXIMUM_MEMORY="PLACEHOLDER"')
    assert f.contains('^JIRA_HOME="/var/atlassian/application-data/jira"')
    assert f.contains('^export CATALINA_OPTS="')


def test_cluster_file(host):
    f = host.file('/var/atlassian/application-data/jira/cluster.properties')
    assert f.exists
    assert f.contains('jira.node.id = FAKEID')
    assert f.contains('jira.shared.home = /media/atl/jira/shared')


def test_server_file(host):
    f = host.file('/opt/atlassian/jira-software/current/conf/server.xml')
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
    assert host.file('/opt/atlassian/jira-software/current/conf/server.xml').user == 'root'
    assert host.file('/opt/atlassian/jira-software/current/atlassian-jira/WEB-INF/web.xml').user == 'root'

    assert host.file('/opt/atlassian/jira-software/current/logs/').user == 'jira'
    assert host.file('/opt/atlassian/jira-software/current/work/').user == 'jira'
    assert host.file('/opt/atlassian/jira-software/current/temp/').user == 'jira'
