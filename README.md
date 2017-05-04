# ssm_parameter_store
ansible module to manage key/value in aws parameter store

Target file: library/ssm_parameter_store.py

### Pull request has been raised to ansible.

https://github.com/ansible/ansible/pull/23460

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
# lookup ssm parameter store value in current region
- debug: msg="{{ lookup('ssm', 'Hello') }}"

# lookup ssm parameter store, the key is not exist
- debug: msg="{{ lookup('ssm', 'NoKey') }}"

# lookup ssm parameter store value in nominated region
- debug: msg="{{ lookup('ssm', 'Hello', 'region=us-east-1') }}"

# lookup ssm parameter store value without decrypted"
- debug: msg="{{ lookup('ssm', 'Hello', 'decrypt=False') }}"
```

### Tutorials

1) make sure you have configured aws command line

refer: http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html

2) run the command 
```
cd test
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
