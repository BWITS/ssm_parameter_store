#!/usr/bin/python

DOCUMENTATION = '''
---
module: ssm_parameter_store
short_description: Manage key/vaule pairs in aws parameter store.
'''

EXAMPLES = '''
- name: Create or update key/vaule pair in aws parameter store
  ssm_parameter_store:
    name: "Hello"
    description: "This is your first key"
    value: "World"
  register: result

- name: Delete the key 
  ssm_parameter_store:
    name: "Hello"
    state: absent
  register: result

- name: Create or update secure key/vaule pair in aws parameter store
  ssm_parameter_store:
    name: "Hello"
    description: "This is your first key"
    type: "SecureString"
    value: "World"
  register: result

- name: Retrieving plain-text secret
  ssm_parameter_store:
    name: "Hello"
    state: show
  register: result

- name: Retrieving plain-text secret with custom kms key
  ssm_parameter_store:
    name: "Hello"
    key_id: "aws/ssm"
    state: show
  register: result

- name: Retrieving secret without decrypted
  ssm_parameter_store:
    name: "Hello"
    decryption: False
    state: show
  register: result
'''

try:
    import botocore
    import boto3
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ec2 import boto3_conn, AnsibleAWSError, ec2_argument_spec, get_aws_connection_info

def create_update_parameter(client, module):
    print "create_update_parameter"

def get_parameter(client, module):
    changed = False
    try:
      parameter = client.get_parameters(
                  Names=[module.params.get('name')],
                  WithDecryption=module.params.get('decryption')
      )
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=str(e))
    return (changed, parameter)

def delete_parameter(client, module):
    print "delete_parameter"

def main():

    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(
        name = dict(required=True),
        description = dict(required=False),
        value =       dict(required=False),
        state =       dict(default='present', choices=['present', 'absent', 'show']),
        type =        dict(default='String', choices=['String', 'StringList', 'SecureString']),
        decryption =  dict(default=True, type='bool'),
        key_id =      dict(default='aws/ssm'),
        ),
    )

    module = AnsibleModule(argument_spec=argument_spec)

    if not HAS_BOTO3:
        module.fail_json(msg='boto3 are required.')
    state = module.params.get('state').lower()
    try: 
        region, ec2_url, aws_connect_kwargs = get_aws_connection_info(module, boto3=True)
        client = boto3_conn(module, conn_type='client', resource='ssm', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except botocore.exceptions.NoCredentialsError as e:
        module.fail_json(msg="Can't authorize connection - %s" % str(e)) 

    invocations = {
      "present": create_update_parameter,
      "absent":  delete_parameter,
      "show":    get_parameter,
    }
    (changed, results) = invocations[state](client, module)
    module.exit_json(changed=changed, nacl_id=results)

if __name__ == '__main__':
    main()
