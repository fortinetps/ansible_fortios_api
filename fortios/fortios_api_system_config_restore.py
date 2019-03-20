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
module: fortios_api_system_config_restore
version_added: "2.6"
short_description: Restore system configuration
description:
    - Restore system configuration from uploaded file or from USB.
author:
    - Will Wagner (@willwagner602)
      Eugene Opredelennov (@eoprede)
      Don Yao (@fortinetps)
notes:
    - Tested against Fortigate v5.4.5 VM
    - Can use all of the parameters supported by Fortigate API

options:
    config:
        description:
            - Configuration to be restored
        required: true
        type: dict
        suboptions:
            filename:
                description:
                    - Configuration filename
                required: true
'''
EXAMPLES = '''
---
name: restore config
tags:
- hostname
fortios_api_system_config_restore:
  conn_params:
    fortigate_username: admin
    fortigate_password: test
    fortigate_ip: 1.2.3.4
    verify: false
  config:
  - filename: /firmware/backup_config.conf

'''

RETURN = '''
result:
    description: k/v pairs of firmware upgrade result
    returned: always
    type: dict
'''

from ansible.module_utils.fortios_api import API
from base64 import b64encode
import json
import os

system_config_api_args = {
    'endpoint': ["monitor", "system", "config", "restore"],
    'list_identifier': 'config',
    'object_identifier': '',
    'default_ignore_params': [],
}


def main():
    forti_api = API(api_info=system_config_api_args)
    if forti_api._update_config and forti_api._update_config[0].get('filename'):
        config_file = forti_api._update_config[0]['filename']
        if os.path.isfile(config_file):
            config = {
                "source": "upload", 
                "scope": "global",
                "file_content": b64encode(open(config_file, 'rb').read()).decode('utf-8')
            }
            response = forti_api.perform_action_on_endpoint(changed=True, api_request_data=json.dumps(config))
            config_restored = response['results']['config_restored']
            if config_restored:
                message = "Config restored successfully"
                forti_api._module.exit_json(msg=message, changed=True, failed=False, response=response)
            else:
                message = "Config restore failed with error: " + response['results']['error']
                forti_api._module.fail_json(msg=message, changed=False, response=response)
        else:
            forti_api._module.fail_json(msg="Configuratin file " + config_file + " is not found", changed=False)
    else:
        forti_api._module.fail_json(msg="Configuratin filename is required", changed=False)


if __name__ == "__main__":
    main()
