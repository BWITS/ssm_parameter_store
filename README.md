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

- name: recommend to use with ssm lookup plugin
  debug: msg="{{ lookup('ssm', 'hello') }}"

- name: lookup a key which is not exist
  debug: msg="{{ lookup('ssm', 'NoKey') }}"

```

### Reference: 

http://docs.ansible.com/ansible/dev_guide/developing_modules.html

https://github.com/ansible/ansible-modules-extras/blob/devel/cloud/amazon/ec2_vpc_nacl.py

# Parameter lookup plungin
ansible lookup plugin to easily get key-value from aws parameter store

Target file: lookup/ssm.py

### Usage:

```
- debug: msg="{{ lookup('ssm', 'foo') }}"

Output: 

TASK [debug] *******************************************************************
ok: [localhost] => {
    "msg": "Hello World!"
}

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
