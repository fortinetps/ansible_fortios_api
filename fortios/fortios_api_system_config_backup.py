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
module: fortios_api_system_config_backup
version_added: "2.6"
short_description: Backup system configuration
description:
    - Backup system configuration from uploaded file or from USB.
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
            - Configuration to be backup
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
name: backup config
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

system_config_api_args = {
    'endpoint': ["monitor", "system", "config", "backup"],
    'list_identifier': 'config',
    'object_identifier': '',
    'default_ignore_params': [],
}


def main():
    forti_api = API(api_info=system_config_api_args)
    if forti_api._update_config and forti_api._update_config[0].get('filename'):
        config_file = forti_api._update_config[0]['filename']
        parameters = {
            'destination': 'file',
            'scope': 'global'
        }
        response = forti_api._show2(forti_api._endpoint, params=parameters)
        if response.status_code != 200:
            message = "Configuration backup API call failed: " + response['reason']
            forti_api._module.fail_json(msg=message, changed=False, response=response)
        else:
            try:
                with open(config_file, mode='wb') as f:
                    f.write(response.text.encode('utf-8'))
            except Exception as err:
                forti_api._module.fail_json(msg="Can't write to configuration file: " + config_file + ", with exception: " + str(err), changed=False)
                
            message = "Configuration file backup successfully to: " + config_file
            forti_api._module.exit_json(msg=message, changed=False, failed=False)        
    else:
        forti_api._module.fail_json(msg="Configuratin filename is required", changed=False)


if __name__ == "__main__":
    main()
