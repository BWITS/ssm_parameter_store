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

try:
    import botocore
    import boto3
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase

class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):

        if not HAS_BOTO3:
            raise AnsibleError('botocore and boto3 are required.')

        client = boto3.client('ssm')

        ret = {}

        for term in terms:
            try:
                response = client.get_parameters(
                      Names=[term],
                      WithDecryption=True
                )
            except botocore.exceptions.ClientError as e:
                module.fail_json(msg=str(e))
            ret.update(response)

        if ret['Parameters']:
            return [ret['Parameters'][0]['Value']]
        else:
            return None

