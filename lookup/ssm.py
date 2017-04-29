# (c) 2016, Bill Wang <ozbillwang(at)gmail.com>
#
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

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.ec2 import HAS_BOTO3
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase

try:
    from botocore.exceptions import ClientError
    import boto3
except ImportError:
    pass  # will be captured by imported HAS_BOTO3


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):

        ret = {}
        response = {}

        ssm_args = terms[0].split()
        ssm_dict = {}

        if not HAS_BOTO3:
            raise AnsibleError('botocore and boto3 are required.')

        # connect to current region
        client = boto3.client('ssm')

        # get decrypted string as default
        ssm_dict['WithDecryption'] = True

        # lookup sample:
        # lookup ssm parameter store in current region
        # - debug: msg="{{ lookup('ssm', 'Hello') }}"
        if len(ssm_args) == 1 and "=" not in ssm_args[0]:
            ssm_dict['Names'] = ssm_args

        # lookup sample:
        # lookup ssm parameter store in nominated region
        # - debug: msg="{{ lookup('ssm', 'key=Hello region=us-east-1') }}"
        else:
            for param in ssm_args:
                if "=" in param:
                    key, value = param.split('=')
                else:
                    raise AnsibleError("ssm parameter store plugin needs key=value pairs, but received %s" % terms)

                if key == "key":
                    ssm_dict['Names'] = [value]

                if key == "region":
                    # connect to nomintated region
                    client = boto3.client('ssm', region_name=value)

        try:
            response = client.get_parameters(**ssm_dict)
        except ClientError:
            raise AnsibleError("ssm parameter store plugin can't get parameters, is AWS access key correct and not expired?")

        ret.update(response)

        if ret['Parameters']:
            return [ret['Parameters'][0]['Value']]
        else:
            return None
