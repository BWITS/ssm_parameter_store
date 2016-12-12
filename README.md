## ssm_parameter_store
ansible module to manage key/value in aws parameter store

Target file: library/ssm_parameter_store.py

### Usage:

```
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
    string_type: "SecureString"
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

```

### Reference: 

http://docs.ansible.com/ansible/dev_guide/developing_modules.html

https://github.com/ansible/ansible-modules-extras/blob/devel/cloud/amazon/ec2_vpc_nacl.py

## parameter lookup plungin
ansible lookup plugin to easily get key-value from aws parameter store

Target file: lookup/ssm.py

### Usage:

```
- debug: msg="{{ lookup('ssm', 'foo') }}"
```

### Reference:

https://docs.ansible.com/ansible/dev_guide/developing_plugins.html#lookup-plugins

https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/lookup/credstash.py

https://github.com/jhaals/ansible-vault/blob/master/vault.py
