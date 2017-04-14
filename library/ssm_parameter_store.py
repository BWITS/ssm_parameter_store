#!/usr/bin/python
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.0'}

DOCUMENTATION = '''
---
module: ssm_parameter_store
short_description: Manage key-value pairs in aws parameter store.
description:
  - Manage key-value pairs in aws parameter store.
version_added: "2.4"
options:
  name:
    description:
      - parameter key name.
    required: true
  description:
    description:
      - parameter key desciption.
    required: false
  value:
    description:
      - Parameter value.
    required: false
  state:
    description:
      - Creates or modifies an existing parameter
      - Deletes a parameter
    required: false
    choices: ['present', 'absent']
    default: present
  string_type:
    description:
      - Parameter String type
    required: false
    choices: ['String', 'StringList', 'SecureString']
    default: String
  decryption:
    description:
      - Work with SecureString type to get plain text secrets
      - Boolean
    required: false
    default: True
  key_id:
    description:
      - aws KMS key to decrypt the secrets.
    required: false
    default: aws/ssm (this key is automatically generated at the first parameter created).
  overwrite:
    description:
      - Overwrite the value when create or update parameter
      - Boolean
    required: false
    default: True
author: Bill Wang (ozbillwang@gmail.com)
extends_documentation_fragment: aws
requirements: [ botocore, boto3 ]
'''

EXAMPLES = '''
- name: Create or update key/value pair in aws parameter store
  ssm_parameter_store:
    name: "Hello"
    description: "This is your first key"
    value: "World"

- name: Delete the key
  ssm_parameter_store:
    name: "Hello"
    state: absent

- name: Create or update secure key/value pair with default kms key (aws/ssm)
  ssm_parameter_store:
    name: "Hello"
    description: "This is your first key"
    string_type: "SecureString"
    value: "World"

- name: Create or update secure key/value pair with nominated kms key
  ssm_parameter_store:
    name: "Hello"
    description: "This is your first key"
    string_type: "SecureString"
    key_id: "alias/demo"
    value: "World"

- name: recommend to use with ssm lookup plugin
  debug: msg="{{ lookup('ssm', 'hello') }}"
'''

RETURN = '''
put_parameter:
    description: Add one or more paramaters to the system.
    returned: success
    type: dictionary
get_parameter:
    description: Get details of a parameter.
    returned: success
    type: dictionary
    contains:
        name:
            description: The name of the parameter.
            returned: success
            type: string
            sample: "Hello"
        type:
            description: The type of parameter. Valid values include [ String, StringList, SecureString ]
            returned: success
            type: string
            sample: "String"
        value:
            description: The parameter value.
            returned: success
            type: string
            sample: "World"
delete_parameter:
    description: Delete a parameter from the system.
    returned: success
    type: dictionary
'''

from ansible.module_utils.ec2 import HAS_BOTO3
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ec2 import boto3_conn, ec2_argument_spec, get_aws_connection_info

try:
    from botocore.exceptions import ClientError
except ImportError:
    pass  # will be captured by imported HAS_BOTO3


def create_update_parameter(client, module):
    changed = False
    reponse = {}

    args = dict(
        Name=module.params.get('name'),
        Value=module.params.get('value'),
        Type=module.params.get('string_type'),
        Overwrite=module.params.get('overwrite')
    )

    if module.params.get('description'):
        args.update(Description=module.params.get('description'))

    if module.params.get('string_type') == 'SecureString':
        args.update(KeyId=module.params.get('key_id'))

    try:
        reponse = client.put_parameter(**args)
        changed = True
    except ClientError, e:
        module.fail_json(msg=e.message, exception=traceback.format_exc(),
                         **camel_dict_to_snake_dict(e.response))

    return changed, reponse


def get_parameter(client, module):
    changed = False
    reponse = {}

    try:
        reponse = client.get_parameters(
            Names=[module.params.get('name')],
            WithDecryption=module.params.get('decryption')
        )
    except ClientError, e:
        module.fail_json(msg=e.message, exception=traceback.format_exc(),
                         **camel_dict_to_snake_dict(e.response))

    return changed, reponse['Parameters']


def delete_parameter(client, module):
    changed = False
    reponse = {}

    try:
        get_reponse = client.get_parameters(
            Names=[module.params.get('name')]
        )
    except ClientError, e:
        module.fail_json(msg=e.message, exception=traceback.format_exc(),
                         **camel_dict_to_snake_dict(e.response))

    if get_reponse['Parameters']:
        try:
            reponse = client.delete_parameter(
                Name=module.params.get('name')
            )
            changed = True
        except ClientError, e:
            module.fail_json(msg=e.message, exception=traceback.format_exc(),
                             **camel_dict_to_snake_dict(e.response))

    return changed, reponse


def main():

    argument_spec = ec2_argument_spec()
    argument_spec.update(
        dict(
            name=dict(required=True),
            description=dict(),
            value=dict(required=False),
            state=dict(default='present', choices=['present', 'absent']),
            string_type=dict(default='String', choices=['String', 'StringList', 'SecureString']),
            decryption=dict(default=True, type='bool'),
            key_id=dict(default='aws/ssm'),
            overwrite=dict(default=True, type='bool'),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec)

    if not HAS_BOTO3:
        module.fail_json(msg='boto3 are required.')
    state = module.params.get('state')
    try:
        region, ec2_url, aws_connect_kwargs = get_aws_connection_info(module, boto3=True)
        client = boto3_conn(module, conn_type='client', resource='ssm', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except botocore.exceptions.NoCredentialsError as e:
        module.fail_json(msg="Can't authorize connection - %s" % str(e))

    invocations = {
        "present": create_update_parameter,
        "absent": delete_parameter,
    }
    (changed, reponse) = invocations[state](client, module)
    module.exit_json(changed=changed, response=reponse)

if __name__ == '__main__':
    main()
