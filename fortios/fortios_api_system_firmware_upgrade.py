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
module: fortios_api_firmware_upgrade
version_added: "2.6"
short_description: Apply FortiGate firewall firmware upgrade
description:
    - Apply FortiGate firewall firmware upgrade
author:
    - Will Wagner (@willwagner602)
      Eugene Opredelennov (@eoprede)
      Don Yao (@fortinetps)
notes:
    - Tested against Fortigate v5.4.5 VM
    - Can use all of the parameters supported by Fortigate API

options:
    firmware:
        description:
            - Firmware upgrade information
        required: true
        type: dict
        suboptions:
            filename:
                description:
                    - Firmware filename and path
                required: true
'''
EXAMPLES = '''
---
name: upgrade firmware
tags:
- hostname
fortios_api_firmware_upgrade:
  print_current_config: false
#   conn_params:
  fortigate_username: admin
  fortigate_password: test
  fortigate_ip: 1.2.3.4
  verify: false
  firmware:
  - filename: /firmware/FGT_VM64_KVM-v6-build0163-FORTINET.out

'''

RETURN = '''
result:
    description: k/v pairs of firmware upgrade result
    returned: always
    type: dict
'''

from base64 import b64encode
import json
import os
import requests

try:
    from ansible.module_utils.fortios_api import API
except ImportError as error:
    from module_utils.fortios_api import API

system_firmware_upgrade_api_args = {
    'endpoint': ["monitor", "system", "firmware", "upgrade"],
    'list_identifier': 'firmware',
    'object_identifier': '',
    'default_ignore_params': [],
}


def main():
    forti_api = API(api_info=system_firmware_upgrade_api_args)
    if forti_api._update_config and forti_api._update_config[0].get('filename'):
        firmware_file = forti_api._update_config[0]['filename']
        if os.path.isfile(firmware_file):
            firmware = {
                "source": "upload", 
                "file_content": b64encode(open(firmware_file, 'rb').read()).decode('utf-8')
            }
            try:
                response = forti_api.perform_action_on_endpoint(changed=True, api_request_data=json.dumps(firmware), timeout=600)
                status = response['results']['status']
            except requests.exceptions.Timeout as error:
                forti_api._module.fail_json(msg="Firmware Upgrade Timeout: " + str(error), changed=False)
            if status == "success":
                # try: 
                    # message = "Firmware restored successfully"
                forti_api._module.exit_json(msg="Firmware restored successfully", changed=True, failed=False, response=response)
                # I encountered this issue occassionaly, the exit_json call might raise SystemExit exception for some reasons which I am not quite understand, below is part of the error message
                # fatal: [dyao501e02]: FAILED! => {"changed": false, "module_stderr": "Exception SystemExit: SystemExit(1,) in <bound method API.__del__ of <ansible.module_utils.fortios_api.API object at 0x7f3453de9ed0>> ignored\n", "module_stdout": "\n{\"msg\": \"Firmware restored successfully\", \"failed\": false, \"changed\": true, \"response\": {\"status\": \"success\", \"name\": \"firmware\", \"results\": {\"status\": \"success\"}, \"http_method\"
                # except SystemExit as error: # to bypass the SystemExit exception
                #     pass
            else:   # status == "error"
                message = "Firmware restore failed with error: " + response['results']['error']
                forti_api._module.fail_json(msg=message, changed=False, response=response)
        else:
            forti_api._module.fail_json(msg="Firmware file " + firmware_file + " is not found", changed=False)
    else:
        forti_api._module.fail_json(msg="Firmware filename is required", changed=False)


if __name__ == "__main__":
    main()
