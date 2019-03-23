#!/usr/bin/python
#
# Ansible module for managing Fortigate devices via API
# (c) 2017, Will Wagner <willwagner602@gmail.com> and Eugene Opredelennov <eoprede@gmail.com>
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: fortios_api_router_static
version_added: "2.6"
short_description: Manages router static configuration.
description:
    - Manages router static configuration.
author:
    - Will Wagner (@willwagner602)
      Eugene Opredelennov (@eoprede)
      Don Yao (dyao@fortinet.com)
notes:
    - Tested against Fortigate v5.4.5 VM
    - Can use all of the parameters supported by Fortigate API

options:
    static:
        description:
            - static route parameters
        required: true
        suboptions:
            dst:
                description:
                    - Destination IP and mask for this route.
                required: false
                default: 0.0.0.0 0.0.0.0
            gateway:
                description:
                    - Gateway IP for this route.
                required: true
            device:
                description:
                    - Gateway out interface or tunnel.
                required: true
'''
EXAMPLES = '''
---
name: Test static route
tags:
- static
fortios_api_router_static:
  print_current_config: false
  conn_params:
    fortigate_username: admin
    fortigate_password: test
    fortigate_ip: 1.2.3.4
  static:
  - seq-num: 1
    dst: 0.0.0.0 0.0.0.0
    gateway: 192.168.1.1
    device: port1
'''

RETURN = '''
proposed:
    description: k/v pairs of parameters passed into module
    returned: always
    type: dict
existing:
    description:
        - k/v pairs of existing configuration
    returned: always
    type: dict
end_state:
    description: k/v pairs of configuration after module execution
    returned: always
    type: dict
updates:
    description: command sent to the device
    returned: always
    type: list
changed:
    description: check to see if a change was made on the device
    returned: always
    type: boolean
'''

from ansible.module_utils.fortios_api import API

router_static_args = {
    "endpoint": ["cmdb", "router", "static"],
    "list_identifier": 'static',
    "object_identifier": 'seq-num',
    "permanent_objects": [],
    "default_ignore_params": [],
}


def main():
    forti_api = API(router_static_args)
    forti_api.apply_configuration_to_endpoint()


if __name__ == "__main__":
    main()
