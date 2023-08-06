import json
import os
import subprocess
import time

import click
import pystache
import requests
import stups_cli.config
import yaml
import zign.api
from clickclick import AliasedGroup, error, info, print_table

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def request(method, url, data=None, headers=None, **kwargs):
    token = zign.api.get_token('uid', ['uid'])
    if not headers:
        headers = {}
        if data:
            headers['Content-Type'] = 'application/json'
    headers['Authorization'] = 'Bearer {}'.format(token)
    return method(url, data=data, headers=headers, timeout=5, **kwargs)


def approve(api_url, change_request_id):
    url = '{}/change-requests/{}/approvals'.format(api_url, change_request_id)
    response = request(requests.post, url, data=json.dumps({}))
    response.raise_for_status()


def execute(api_url, change_request_id):
    url = '{}/change-requests/{}/execute'.format(api_url, change_request_id)
    response = request(requests.post, url)
    response.raise_for_status()


def approve_and_execute(api_url, change_request_id):
    approve(api_url, change_request_id)
    execute(api_url, change_request_id)


def parse_parameters(parameter):
    context = {}
    for param in parameter:
        key, val = param.split('=', 1)
        context[key] = val
    return context


def _render_template(template, context):
    contents = template.read()
    rendered_contents = pystache.render(contents, context)
    data = yaml.safe_load(rendered_contents)
    return data


def get_scaling_operation(replicas, deployment_name):
    return {'resources_update': [{'kind': 'deployments', 'name': deployment_name,
            'operations': [{'op': 'replace', 'path': '/spec/replicas', 'value': replicas}]}]}


@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    ctx.obj = stups_cli.config.load_config('zalando-deploy-cli')


@cli.command()
@click.option('--deploy-api')
@click.option('--cluster-registry')
@click.option('--aws-account')
@click.option('--aws-region')
@click.option('--kubernetes-api-server')
@click.option('--kubernetes-cluster')
@click.option('--kubernetes-namespace')
@click.pass_obj
def configure(config, **kwargs):
    for key, val in kwargs.items():
        if val is not None:
            config[key] = val
    stups_cli.config.store_config(config, 'zalando-deploy-cli')


@cli.command()
@click.argument('template_or_directory')
@click.argument('parameter', nargs=-1)
@click.pass_obj
@click.option('--execute', is_flag=True)
def apply(config, template_or_directory, parameter, execute):
    '''Apply CloudFormation or Kubernetes resource'''

    template_paths = []
    if os.path.isdir(template_or_directory):
        for entry in os.listdir(template_or_directory):
            if entry.endswith('.yaml') and not entry.startswith('.'):
                template_paths.append(os.path.join(template_or_directory, entry))
    else:
        template_paths.append(template_or_directory)

    for path in template_paths:
        with open(path, 'r') as fd:
            data = _render_template(fd, parse_parameters(parameter))

        if not isinstance(data, dict):
            error('Invalid YAML contents in {}'.format(path))
            raise click.Abort()

        api_url = config.get('deploy_api')
        if 'kind' in data:
            info('Applying Kubernetes manifest {}..'.format(path))
            cluster_id = config.get('kubernetes_cluster')
            namespace = config.get('kubernetes_namespace')
            url = '{}/kubernetes-clusters/{}/namespaces/{}/resources'.format(api_url, cluster_id, namespace)
            response = request(requests.post, url, data=json.dumps(data))
            response.raise_for_status()
            change_request_id = response.json()['id']
        else:
            info('Applying Cloud Formation template {}..'.format(path))
            aws_account = config.get('aws_account')
            aws_region = config.get('aws_region')
            stack_name = data.get('Metadata', {}).get('StackName')
            if not stack_name:
                error('Cloud Formation template requires Metadata/StackName property')
                raise click.Abort()
            url = '{}/aws-accounts/{}/regions/{}/cloudformation-stacks/{}'.format(
                api_url, aws_account, aws_region, stack_name)
            response = request(requests.put, url, data=json.dumps(data))
            response.raise_for_status()
            change_request_id = response.json()['id']

        if execute:
            approve_and_execute(api_url, change_request_id)
        else:
            print(change_request_id)


@cli.command('create-deployment')
@click.argument('template', type=click.File('r'))
@click.argument('application')
@click.argument('version')
@click.argument('release')
@click.argument('parameter', nargs=-1)
@click.pass_obj
@click.option('--execute', is_flag=True)
def create_deployment(config, template, application, version, release, parameter, execute):
    '''Create a new Kubernetes deployment'''
    context = parse_parameters(parameter)
    context['application'] = application
    context['version'] = version
    context['release'] = release
    data = _render_template(template, context)

    api_url = config.get('deploy_api')
    cluster_id = config.get('kubernetes_cluster')
    namespace = config.get('kubernetes_namespace')
    url = '{}/kubernetes-clusters/{}/namespaces/{}/resources'.format(api_url, cluster_id, namespace)
    response = request(requests.post, url, data=json.dumps(data))
    response.raise_for_status()
    change_request_id = response.json()['id']

    if execute:
        approve_and_execute(api_url, change_request_id)
    else:
        print(change_request_id)


@cli.command('wait-for-deployment')
@click.argument('application')
@click.argument('version')
@click.argument('release')
@click.option('-t', '--timeout',
              type=click.IntRange(0, 7200, clamp=True),
              metavar='SECS',
              default=300,
              help='Maximum wait time (default: 300s)')
@click.option('-i', '--interval', default=10,
              type=click.IntRange(1, 600, clamp=True),
              help='Time between checks (default: 10s)')
@click.pass_obj
def wait_for_deployment(config, application, version, release, timeout, interval):
    '''Wait for all pods to become ready'''
    namespace = config.get('kubernetes_namespace')
    # TODO: api server needs to come from Cluster Registry
    subprocess.check_output(['zkubectl', 'login', config.get('kubernetes_api_server')])
    deployment_name = '{}-{}-{}'.format(application, version, release)
    cutoff = time.time() + timeout
    while time.time() < cutoff:
        cmd = ['zkubectl', 'get', 'pods', '--namespace={}'.format(namespace),
               '-l', 'application={},version={},release={}'.format(application, version, release), '-o', 'json']
        out = subprocess.check_output(cmd)
        data = json.loads(out.decode('utf-8'))
        pods = data['items']
        pods_ready = 0
        for pod in pods:
            if pod['status'].get('phase') == 'Running':
                all_containers_ready = True
                for cont in pod['status'].get('containerStatuses', []):
                    if not cont.get('ready'):
                        all_containers_ready = False
                if all_containers_ready:
                    pods_ready += 1
        if pods and pods_ready >= len(pods):
            return
        info('Waiting up to {:.0f} more secs for deployment '
             '{} ({}/{} pods ready)..'.format(cutoff - time.time(), deployment_name, pods_ready, len(pods)))
        time.sleep(interval)
    raise click.Abort()


@cli.command('switch-deployment')
@click.argument('application')
@click.argument('version')
@click.argument('release')
@click.argument('ratio')
@click.pass_obj
@click.option('--execute', is_flag=True)
def switch_deployment(config, application, version, release, ratio, execute):
    '''Switch to new release'''
    namespace = config.get('kubernetes_namespace')
    # TODO: api server needs to come from Cluster Registry
    subprocess.check_output(['zkubectl', 'login', config.get('kubernetes_api_server')])

    target_replicas, total = ratio.split('/')
    target_replicas = int(target_replicas)
    total = int(total)

    cmd = ['zkubectl', 'get', 'deployments', '--namespace={}'.format(namespace),
           '-l', 'application={}'.format(application), '-o', 'json']
    out = subprocess.check_output(cmd)
    data = json.loads(out.decode('utf-8'))
    deployments = data['items']
    target_deployment_name = '{}-{}-{}'.format(application, version, release)

    remaining_replicas = total
    for deployment in sorted(deployments, key=lambda d: d['metadata']['name'], reverse=True):
        deployment_name = deployment['metadata']['name']
        if deployment_name == target_deployment_name:
            replicas = target_replicas
        else:
            # maybe spread across all other deployments?
            replicas = remaining_replicas

        remaining_replicas -= replicas

        info('Scaling deployment {} to {} replicas..'.format(deployment_name, replicas))
        api_url = config.get('deploy_api')
        cluster_id = config.get('kubernetes_cluster')
        namespace = config.get('kubernetes_namespace')
        url = '{}/kubernetes-clusters/{}/namespaces/{}/resources'.format(api_url, cluster_id, namespace)
        response = request(requests.patch, url, data=json.dumps(
            get_scaling_operation(replicas, deployment_name)))
        response.raise_for_status()
        change_request_id = response.json()['id']

        if execute:
            approve_and_execute(api_url, change_request_id)
        else:
            print(change_request_id)


@cli.command('scale-deployment')
@click.argument('application')
@click.argument('version')
@click.argument('release')
@click.argument('replicas', type=int)
@click.pass_obj
@click.option('--execute', is_flag=True)
def scale_deployment(config, application, version, release, replicas, execute):
    '''Scale a single deployment'''
    namespace = config.get('kubernetes_namespace')
    # TODO: api server needs to come from Cluster Registry
    subprocess.check_output(['zkubectl', 'login', config.get('kubernetes_api_server')])

    deployment_name = '{}-{}-{}'.format(application, version, release)

    info('Scaling deployment {} to {} replicas..'.format(deployment_name, replicas))
    api_url = config.get('deploy_api')
    cluster_id = config.get('kubernetes_cluster')
    namespace = config.get('kubernetes_namespace')
    url = '{}/kubernetes-clusters/{}/namespaces/{}/resources'.format(api_url, cluster_id, namespace)
    response = request(requests.patch, url, data=json.dumps(
        get_scaling_operation(replicas, deployment_name)))
    response.raise_for_status()
    change_request_id = response.json()['id']

    if execute:
        approve_and_execute(api_url, change_request_id)
    else:
        print(change_request_id)


@cli.command('delete-old-deployments')
@click.argument('application')
@click.argument('version')
@click.argument('release')
@click.pass_obj
@click.option('--execute', is_flag=True)
def delete_old_deployments(config, application, version, release, execute):
    '''Delete old releases'''
    namespace = config.get('kubernetes_namespace')
    # TODO: api server needs to come from Cluster Registry
    subprocess.check_output(['zkubectl', 'login', config.get('kubernetes_api_server')])

    cmd = ['zkubectl', 'get', 'deployments', '--namespace={}'.format(namespace),
           '-l', 'application={}'.format(application), '-o', 'json']
    out = subprocess.check_output(cmd)
    data = json.loads(out.decode('utf-8'))
    deployments = data['items']
    target_deployment_name = '{}-{}-{}'.format(application, version, release)
    deployments_to_delete = []
    deployment_found = False

    for deployment in sorted(deployments, key=lambda d: d['metadata']['name'], reverse=True):
        deployment_name = deployment['metadata']['name']
        if deployment_name == target_deployment_name:
            deployment_found = True
        else:
            deployments_to_delete.append(deployment_name)

    if not deployment_found:
        error('Deployment {} was not found.'.format(target_deployment_name))
        raise click.Abort()

    for deployment in deployments_to_delete:
        info('Deleting deployment {}..'.format(deployment_name))
        api_url = config.get('deploy_api')
        cluster_id = config.get('kubernetes_cluster')
        namespace = config.get('kubernetes_namespace')
        url = '{}/kubernetes-clusters/{}/namespaces/{}/deployments/{}'.format(
            api_url, cluster_id, namespace, deployment_name)
        response = request(requests.delete, url)
        response.raise_for_status()
        change_request_id = response.json()['id']

        if execute:
            approve_and_execute(api_url, change_request_id)
        else:
            print(change_request_id)


@cli.command('render-template')
@click.argument('template', type=click.File('r'))
@click.argument('parameter', nargs=-1)
@click.pass_obj
def render_template(config, template, parameter):
    '''Interpolate YAML Mustache template'''
    data = _render_template(template, parse_parameters(parameter))
    print(yaml.safe_dump(data))


@cli.command('list-change-requests')
@click.pass_obj
def list_change_requests(config):
    '''List change requests'''
    api_url = config.get('deploy_api')
    url = '{}/change-requests'.format(api_url)
    response = request(requests.get, url)
    response.raise_for_status()
    items = response.json()['items']
    rows = []
    for row in items:
        rows.append(row)
    print_table('id platform kind user executed'.split(), rows)


@cli.command('get-change-request')
@click.argument('change_request_id', nargs=-1)
@click.pass_obj
def get_change_request(config, change_request_id):
    '''Get one or more change requests'''
    api_url = config.get('deploy_api')
    for id_ in change_request_id:
        url = '{}/change-requests/{}'.format(api_url, id_)
        response = request(requests.get, url)
        response.raise_for_status()
        data = response.json()
        print(yaml.safe_dump(data, default_flow_style=False))


@cli.command('approve-change-request')
@click.argument('change_request_id', nargs=-1)
@click.pass_obj
def approve_change_request(config, change_request_id):
    '''Approve one or more change requests'''
    api_url = config.get('deploy_api')
    for id_ in change_request_id:
        approve(api_url, id_)


@cli.command('list-approvals')
@click.argument('change_request_id')
@click.pass_obj
def list_approvals(config, change_request_id):
    api_url = config.get('deploy_api')
    url = '{}/change-requests/{}/approvals'.format(api_url, change_request_id)
    response = request(requests.get, url)
    response.raise_for_status()
    items = response.json()['items']
    rows = []
    for row in items:
        rows.append(row)
    print_table('user created_at'.split(), rows)


@cli.command('execute-change-request')
@click.argument('change_request_id', nargs=-1)
@click.pass_obj
def execute_change_request(config, change_request_id):
    '''Execute one or more change requests'''
    api_url = config.get('deploy_api')
    for id_ in change_request_id:
        execute(api_url, id_)


def main():
    cli()
