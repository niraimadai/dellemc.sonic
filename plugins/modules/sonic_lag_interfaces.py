#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2020 Dell Inc. or its subsidiaries. All Rights Reserved
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the resource
#   module builder playbook.
#
# Do not edit this file manually.
#
# Changes to this file will be over written
#   by the resource module builder.
#
# Changes should be made in the model used to
#   generate this file or in the resource module
#   builder template.
#
#############################################

"""
The module file for sonic_lag_interfaces
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = """
---
module: sonic_lag_interfaces
version_added: 1.0.0
short_description: Manages link aggregation groups of SONiC Interfaces
description:
  - This module manages attributes of link aggregation groups of SONiC Interfaces.
author: Abirami N (@abirami-n)
notes:
  - Tested against SONiC-OS-3.0.1

options:
  config:
    description: A list of link aggregation group configurations.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - ID of the link aggregation group (LAG).
        type: str
        required: True
      members:
        description:
          - The dict of interfaces that are part of the group.
        type: dict
        suboptions:
          interfaces:
            description: The list of interfaces that are part of the group.
            type: list
            elements: dict
            suboptions:
              member:
                description:
                  - The interface name.
                type: str
  state:
    description:
      - The state the configuration should be left in.
    type: str
    choices:
     - merged
     - replaced
     - overridden
     - deleted
    default: merged
"""
EXAMPLES = """
# Using merged
#
# Before state:
# -------------
#
# interface Ethernet40
# interface Ethernet60
#   channel-group 12
#
#- name: Merge provided configuration with device configuration.
#  sonic_lag_interfaces:
#    config:
#      - name: PortChannel10
#        members:
#          interfaces:
#            - member: Ethernet40
#    state: merged
#
# After state:
# ------------
#
# interface Ethernet40
#   channel-group 10
# interface Ethernet60
#   channel-group 12
#
#
# Using deleted
#
# Before state:
# -------------
#
# interface Ethernet40
#   channel-group 10
#
#- name: Delete LAG attributes of given interface (Note: This won't delete the port-channel itself).
#  sonic_lag_interfaces:
#    config:
#      - name: PortChannel10
#    state: deleted
#
# After state:
# ------------
#
# interface Ethernet40
#   no channel-group
#
#
# Using deleted
#
# Before state:
# -------------
#
# interface Ethernet40
#   channel-group 10
# interface Ethernet60
#   channel-group 12
#
#- name: Delete LAG attributes of all the interfaces
#  sonic_lag_interfaces:
#    config:
#    state: deleted
#
# After state:
# -------------
#
# interface Ethernet40
#    no channel-group
# interface Ethernet60
#    no channel-group
#
#
"""
RETURN = """
before:
  description: The configuration prior to the model invocation.
  returned: always
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
after:
  description: The resulting configuration model invocation.
  returned: when changed
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample: ['command 1', 'command 2', 'command 3']
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.sonic.plugins.module_utils.network.sonic.argspec.lag_interfaces.lag_interfaces import Lag_interfacesArgs
from ansible_collections.dellemc.sonic.plugins.module_utils.network.sonic.config.lag_interfaces.lag_interfaces import Lag_interfaces


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(argument_spec=Lag_interfacesArgs.argument_spec,
                           supports_check_mode=True)

    result = Lag_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == '__main__':
    main()
