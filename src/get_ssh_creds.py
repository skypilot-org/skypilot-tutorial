"""
Script to fetch the SSH credentials and IP addresses of all workers in
a SkyPilot cluster and write them to a CSV file.

usage:
    python get_ssh_creds.py <cluster_name> <output_file>
"""

import csv
import argparse
import os.path

import sky
from sky.backends import backend_utils
from sky.utils import common_utils


def get_cluster(name):
    clusters = sky.global_user_state.get_clusters()
    for cluster in clusters:
        if cluster['name'] == name:
            return cluster
    raise Exception(f'Cluster {name} not found')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cluster_name',
                        help='Name of the SkyPilot cluster used to launch the tutorial')
    parser.add_argument('--output',
                        help='Output file name to write the SSH credentials',
                        default='ssh_creds.csv')
    args = parser.parse_args()

    print(f'Getting SkyPilot cluster handle...')
    cluster = get_cluster(args.cluster_name)
    handle = cluster['handle']

    print(f'Getting IPs for cluster {args.cluster_name}...')
    ip_list = backend_utils.get_node_ips(handle.cluster_yaml,
                                         handle.launched_nodes, handle)
    config = common_utils.read_yaml(handle.cluster_yaml)
    auth_section = config['auth']
    ssh_user = config['auth']['ssh_user']
    ssh_key_path = config['auth']['ssh_private_key']
    print("Got IPs: ", ip_list)
    print("SSH User: ", ssh_user)
    print("SSH Key Path: ", ssh_key_path)

    # CSV format - [IP, Username, ssh_key_path]
    csv_data = []
    for ip in ip_list:
        csv_data.append([ip, ssh_user, ssh_key_path])

    # Write to file
    print("Writing IPs to file: ", args.output)
    with open(args.output, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)

    # Prepare connect script
    print("Preparing connect script")
    # Read template and replace placeholders
    # Read SSH key:
    with open(os.path.expanduser(ssh_key_path), 'r') as f:
        ssh_key = f.read()
    with open('connect_template.sh', 'r') as f:
        template = f.read()
        template = template.replace('ADD_SKYPILOT_KEY_HERE', ssh_key)
    with open('connect.sh', 'w') as f:
        f.write(template)
