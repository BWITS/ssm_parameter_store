# Related PR has been merged，this repository is abandoned.

# ssm_parameter_store
ansible module to manage key/value in aws parameter store

[![Build Status](https://travis-ci.org/BWITS/ssm_parameter_store.svg?branch=master)](https://travis-ci.org/BWITS/ssm_parameter_store)

Target file: library/ssm_parameter_store.py

### Add this module to ansible.

https://github.com/ansible/ansible/pull/23460

This PR has been merged to ansible.

### Usage:

```
- name: Create or update key/value pair in aws parameter store
  ssm_parameter_store:
    name: "Hello"
    description: "This is your first key"
    value: "World"

- name: Delete the key
  ssm_parameter_store:
    name: "Hello"
    state: absent

- name: Delete non-exist key
  ssm_parameter_store:
    name: "notkey"
    state: absent

- name: Create or update secure key/value pair with nominated kms key
  ssm_parameter_store:
    name: "Hello"
    description: "This is your first key"
    key_id: "alias/demo"
    string_type: "SecureString"
    value: "World"
```

Example:

[test/roles/test/tasks/main.yml](test/roles/test/tasks/main.yml)


### Reference: 

http://docs.ansible.com/ansible/dev_guide/developing_modules.html

https://github.com/ansible/ansible-modules-extras/blob/devel/cloud/amazon/ec2_vpc_nacl.py

# Parameter lookup plungin
ansible lookup plugin to easily get key-value from aws parameter store

Target file: lookup/ssm.py

### lookup sample:

```
# lookup sample:
- name: lookup ssm parameter store in the current region
  debug: msg="{{ lookup('ssm', 'Hello' ) }}"

- name: lookup a key which doesn't exist, return ""
  debug: msg="{{ lookup('ssm', 'NoKey') }}"

- name: lookup ssm parameter store in nominated region
  debug: msg="{{ lookup('ssm', 'Hello', 'region=us-east-2' ) }}"

- name: lookup ssm parameter store without decrypted
  debug: msg="{{ lookup('ssm', 'Hello', 'decrypt=False' ) }}"

- name: lookup ssm parameter store in nominated aws profile
  debug: msg="{{ lookup('ssm', 'Hello', 'aws_profile=myprofile' ) }}"

- name: lookup ssm parameter store with all options.
  debug: msg="{{ lookup('ssm', 'Hello', 'decrypt=false', 'region=us-east-2', 'aws_profile=myprofile') }}"
```

### Tutorials

1) make sure you have configured aws command line

refer: http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html

2) run the command 
```
cd test
pip install -r requirements.txt
./cmd.sh

# with verbosse
./cmd.sh -vvvv
```

### Reference:

https://docs.ansible.com/ansible/dev_guide/developing_plugins.html#lookup-plugins

https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/lookup/credstash.py

https://github.com/jhaals/ansible-vault/blob/master/vault.py

http://russell.ballestrini.net/setting-region-programmatically-in-boto3/

https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/lookup/hashi_vault.py

https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/lookup/__init__.py

http://boto3.readthedocs.io/en/latest/reference/core/session.html

http://boto3.readthedocs.io/en/latest/reference/core/boto3.html#boto3.setup_default_session

http://russell.ballestrini.net/filtering-aws-resources-with-boto3/

### Contributors

- capusta
- mtb-xt

