#!/usr/bin/python
#
# Ansible module to manage arbitrary objects via API in fortigate devices
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
module: fortios_api_reboot
version_added: "2.6"
short_description: Reboot firewall
description:
    - Reboot FortiGate firewall
author:
    - Will Wagner (@willwagner602)
      Eugene Opredelennov (@eoprede)
      Don Yao (@fortinetps)
notes:
    - Tested against Fortigate v5.4.5 VM
    - Can use all of the parameters supported by Fortigate API

options:
'''
EXAMPLES = '''
---
name: upgrade firmware
tags:
- hostname
fortios_api_reboot:
  print_current_config: false
  conn_params:
    fortigate_username: admin
    fortigate_password: test
    fortigate_ip: 1.2.3.4
    verify: false

'''

RETURN = '''
result:
    description: k/v pairs of firmware upgrade result
    returned: always
    type: dict
'''

from ansible.module_utils.fortios_api import API
import json

system_reboot_api_args = {
    'endpoint': ["monitor", "system", "os", "reboot"],
    'list_identifier': 'log',
    'object_identifier': '',
    'default_ignore_params': [],
}


def main():
    forti_api = API(api_info=system_reboot_api_args)
    if forti_api._update_config and forti_api._update_config[0].get('message'):
        _reboot_event_log_message = forti_api._update_config[0]['message']
    else:
        _reboot_event_log_message = 'Reboot by FortiOS API'
    log = {
        "event_log_message": _reboot_event_log_message
    }
    response = forti_api.perform_action_on_endpoint(changed=True, api_request_data=json.dumps(log))
    forti_api._module.exit_json(msg="System rebooted", changed=True, failed=False, response=response)

if __name__ == "__main__":
    main()
