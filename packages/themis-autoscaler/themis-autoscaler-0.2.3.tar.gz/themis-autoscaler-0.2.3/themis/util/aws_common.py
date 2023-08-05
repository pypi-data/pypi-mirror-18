import re
import json
import logging
import boto3
import os
from themis import config, constants
from themis.config import SECTION_EMR
from themis.util.common import run_func, remove_lines_from_string, get_logger
from themis.util.common import CURL_CONNECT_TIMEOUT, STATIC_INFO_CACHE_TIMEOUT, QUERY_CACHE_TIMEOUT
from themis.util.remote import run_ssh
# constants

PRESTO_STATE_SHUTTING_DOWN = 'SHUTTING_DOWN'
PRESTO_STATE_ACTIVE = 'ACTIVE'

INSTANCE_GROUP_TYPE_MASTER = 'MASTER'
INSTANCE_GROUP_TYPE_CORE = 'CORE'
INSTANCE_GROUP_TYPE_TASK = 'TASK'

INSTANCE_STATE_RUNNING = 'RUNNING'
INSTANCE_STATE_TERMINATED = 'TERMINATED'

INVALID_CONFIG_VALUE = '_invalid_value_to_avoid_restart_'

# TODO move to model
CLUSTER_TYPE_PRESTO = 'Presto'
CLUSTER_TYPE_HIVE = 'Hive'

# Define local test endpoints
TEST_ENDPOINTS = {}

# logger
LOG = get_logger(__name__)


def init_aws_cli():
    endpoint_url = os.environ.AWS_ENDPOINT_URL
    if endpoint_url:
        TEST_ENDPOINTS['emr'] = endpoint_url
        TEST_ENDPOINTS['kinesis'] = endpoint_url
        TEST_ENDPOINTS['cloudwatch'] = endpoint_url
        TEST_ENDPOINTS['ec2'] = endpoint_url


def connect_emr():
    return connect_to_service('emr')


def connect_kinesis():
    return connect_to_service('kinesis')


def connect_cloudwatch():
    return connect_to_service('cloudwatch')


def connect_ec2():
    return connect_to_service('ec2')


def connect_to_service(service):
    endpoint_url = TEST_ENDPOINTS.get(service)
    return boto3.client(service, endpoint_url=endpoint_url)


def ip_to_hostname(ip, domain_name):
    return 'ip-' + re.sub(r'\.', r'-', ip) + '.' + domain_name


def hostname_to_ip(host):
    return re.sub(r'ip-([0-9]+)-([0-9]+)-([0-9]+)-([0-9]+)\..+', r'\1.\2.\3.\4', host)


def get_instance_by_ip(ip):
    ec2_client = connect_ec2()
    result = run_func(ec2_client.describe_instances,
        Filters=[{'Name': 'private-ip-address', 'Values': [ip]}],
        cache_duration_secs=STATIC_INFO_CACHE_TIMEOUT)
    result = json.loads(result)
    return result['Reservations'][0]['Instances'][0]


def get_instance_groups(cluster_id):
    emr_client = connect_emr()
    result = run_func(emr_client.list_instance_groups, ClusterId=cluster_id,
        cache_duration_secs=QUERY_CACHE_TIMEOUT)
    result = json.loads(result)
    result_map = {}
    for group in result['InstanceGroups']:
        group_type = group['InstanceGroupType']
        if group_type not in result_map:
            result_map[group_type] = []
        group['id'] = group['Id']
        group['type'] = group_type
        result_map[group_type].append(group)

    return result_map


def get_instance_groups_tasknodes(cluster_id):
    return get_instance_groups(cluster_id)[INSTANCE_GROUP_TYPE_TASK]


def get_instance_groups_ids(cluster_id, group_type):
    groups = get_instance_groups(cluster_id)
    return groups[group_type]


def get_instance_group_type(cluster_id, group_id):
    return get_instance_group_details(cluster_id, group_id)['type']


def get_instance_group_details(cluster_id, group_id):
    groups = get_instance_groups(cluster_id)
    for key, arr in groups.iteritems():
        for val in arr:
            if val['id'] == group_id:
                return val
    return None


def get_instance_group_for_node(cluster_id, node_host):
    nodes = get_cluster_nodes(cluster_id)
    for node in nodes:
        if node['host'] == node_host or node['ip'] == node_host:
            return node['gid']
    return None


def get_cluster_nodes(cluster_id):
    emr_client = connect_emr()
    result = run_func(emr_client.list_instances, ClusterId=cluster_id,
        InstanceStates=['AWAITING_FULFILLMENT', 'PROVISIONING', 'BOOTSTRAPPING', 'RUNNING'],
        cache_duration_secs=QUERY_CACHE_TIMEOUT)
    result = json.loads(result)
    result = result['Instances']

    # read domain name config
    custom_dn = config.get_value(constants.KEY_CUSTOM_DOMAIN_NAME, section=SECTION_EMR, resource=cluster_id)

    i = 0
    while i < len(result):
        inst = result[i]
        if inst['Status']['State'] == INSTANCE_STATE_TERMINATED:
            del result[i]
            i -= 1
        else:
            inst['cid'] = inst['Id'] if 'Id' in inst else 'n/a'
            inst['iid'] = inst['Ec2InstanceId'] if 'Ec2InstanceId' in inst else 'n/a'
            inst['gid'] = inst['InstanceGroupId'] if 'InstanceGroupId' in inst else 'n/a'
            inst['ip'] = inst['PrivateIpAddress'] if 'PrivateIpAddress' in inst else 'n/a'
            inst['host'] = inst['PrivateDnsName'] if 'PrivateDnsName' in inst else 'n/a'
            if custom_dn:
                inst['host'] = ip_to_hostname(hostname_to_ip(inst['host']), custom_dn)
            inst['type'] = get_instance_group_type(cluster_id, inst['InstanceGroupId'])
            inst['state'] = inst['Status']['State']
            inst['market'] = get_instance_group_details(cluster_id, inst['InstanceGroupId'])['Market']
        i += 1
    return result


def get_all_task_nodes(cluster_id, cluster_ip):
    all_nodes = get_cluster_nodes(cluster_id)
    task_nodes = [n for n in all_nodes if n['type'] == INSTANCE_GROUP_TYPE_TASK]
    return task_nodes


def terminate_task_node(instance_group_id, instance_id):
    # terminate instance
    emr_client = connect_emr()
    LOG.info('Terminate instance %s of instance group %s' % (instance_id, instance_group_id))
    result = emr_client.modify_instance_groups(InstanceGroups=[
        {'InstanceGroupId': instance_group_id, 'EC2InstanceIdsToTerminate': [instance_id]}
    ])
    return result


def spawn_task_node(instance_group_id, current_size, additional_nodes=1):
    # start new instance
    emr_client = connect_emr()
    new_size = current_size + additional_nodes
    LOG.info('Increase instances of instance group %s from %s to %s' %
        (instance_group_id, current_size, new_size))
    result = emr_client.modify_instance_groups(InstanceGroups=[
        {'InstanceGroupId': instance_group_id, 'InstanceCount': new_size}
    ])
    return result


def is_presto_cluster(cluster):
    return cluster.type == 'Presto'


def terminate_inactive_nodes(cluster, cluster_state):
    if not is_presto_cluster(cluster):
        return
    nodes = cluster_state['nodes']
    for key, node in nodes.iteritems():
        if (node['state'] == INSTANCE_STATE_RUNNING and node['presto_state'] not in
                [PRESTO_STATE_SHUTTING_DOWN, PRESTO_STATE_ACTIVE]):
            try:
                cmd = "cat /etc/presto/conf/config.properties | grep http-server.threads"
                out = run_ssh(cmd, cluster.ip, user='hadoop',
                    via_hosts=[node['host']], cache_duration_secs=QUERY_CACHE_TIMEOUT)
                if INVALID_CONFIG_VALUE in out:
                    LOG.info("Terminating instance of idle node %s in instance group %s" %
                        (node['iid'], node['gid']))
                    terminate_task_node(instance_group_id=node['gid'], instance_id=node['iid'])
            except Exception, e:
                LOG.info("Unable to read Presto config from node %s: %s" % (node, e))


def get_presto_node_state(cluster_ip, node_ip):
    cmd = 'curl -s --connect-timeout %s http://%s:8889/v1/info/state' % (CURL_CONNECT_TIMEOUT, node_ip)
    out = run_ssh(cmd, cluster_ip, user='hadoop', cache_duration_secs=QUERY_CACHE_TIMEOUT)
    out = remove_lines_from_string(out, r'.*Permanently added.*')
    out = re.sub(r'\s*"(.+)"\s*', r'\1', out)
    return out


def set_presto_node_state(cluster_ip, node_ip, state):
    cmd = ("sudo sed -i 's/http-server.threads.max=.*/http-server.threads.max=%s/g' " +
        "/etc/presto/conf/config.properties") % INVALID_CONFIG_VALUE
    out = run_ssh(cmd, cluster_ip, user='hadoop', via_hosts=[node_ip], cache_duration_secs=QUERY_CACHE_TIMEOUT)

    cmd = ("curl -s --connect-timeout %s -X PUT -H 'Content-Type:application/json' " +
        "-d '\\\"%s\\\"' http://%s:8889/v1/info/state") % (CURL_CONNECT_TIMEOUT, state, node_ip)
    LOG.info(cmd)
    out = run_ssh(cmd, cluster_ip, user='hadoop', cache_duration_secs=QUERY_CACHE_TIMEOUT)
    out = re.sub(r'\s*"(.+)"\s*', r'\1', out)
    return out
