#!/usr/bin/python
# -*- coding: utf-8 -*-
# © Copyright 2020 Dell Inc. or its subsidiaries. All Rights Reserved
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
The module file for sonic_l2_interfaces
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
module: sonic_l2_interfaces
version_added: 1.0.0
short_description: 'Manages interface attributes of SONiC l2_interfaces.'
description: 'Manages interface attributes of SONiC l2_interfaces.'
author: 'Niraimadaiselvam M(@niraimadaiselvam-m)'
notes:
  - 'Tested against SONiC-OS-3.0.1'
options:
  config:
    description: 'A list of l2_interfaces configurations.'
    type: list
    elements: dict
    suboptions:
      name:
        type: str
        description: 'The name of the l2_interfaces'
        required: true
      trunk:
        type: dict
        description: 'It is a trunk mode configuration of the l2_interfaces'
        suboptions:
          allowed_vlans:
            description: 'It is a list of allowed vlans of trunk mode of l2_interfaces'
            type: list
            elements: dict
            suboptions:
              vlan:
                type: int
                description: 'This is a vlan in trunk mode'
      access:
        type: dict
        description: 'It is a access mode configuration of the l2_interfaces'
        suboptions:
          vlan:
            type: int
            description: 'This is a vlan in access mode'
  state:
    type: str
    description: 'The state of the configuration after module completion.'
    choices:
    - merged
    - deleted
    default: merged
"""
EXAMPLES = """
# Using deleted
#
# Before state:
# -------------
#
#do show Vlan
#Q: A - Access (Untagged), T - Tagged
#NUM        Status      Q Ports
#10         Inactive    A  Ethernet12
#11         Inactive    T  Ethernet12
#12         Inactive    A  Ethernet13
#13         Inactive    T  Ethernet13
#14         Inactive    A  Ethernet14
#15         Inactive    T  Ethernet14
#
#- name: Configure switch port of interfaces
#  sonic_l2_interfaces:
#    config:
#      - name: Ethernet12
#      - name: Ethernet13
#    state: deleted
#
# After state:
# ------------
#
#do show Vlan
#Q: A - Access (Untagged), T - Tagged
#NUM        Status      Q Ports
#10         Inactive
#11         Inactive
#12         Inactive
#13         Inactive
#14         Inactive    A  Ethernet14
#15         Inactive    T  Ethernet14
#
#
# Using deleted
#
# Before state:
# -------------
#
#do show Vlan
#Q: A - Access (Untagged), T - Tagged
#NUM        Status      Q Ports
#10         Inactive    A  Ethernet12
#11         Inactive    T  Ethernet12
#12         Inactive    A  Ethernet13
#13         Inactive    T  Ethernet13
#14         Inactive    A  Ethernet14
#15         Inactive    T  Ethernet14
#
#- name: Configure switch port of interfaces
#  sonic_l2_interfaces:
#    config:
#    state: deleted
#
# After state:
#do show Vlan
#Q: A - Access (Untagged), T - Tagged
#NUM        Status      Q Ports
#10         Inactive
#11         Inactive
#12         Inactive
#13         Inactive
#14         Inactive
#15         Inactive
#
#
# Using merged
#
# Before state:
# -------------
#
#do show Vlan
#Q: A - Access (Untagged), T - Tagged
#NUM        Status      Q Ports
#11         Inactive    T  Ethernet24
#12         Inactive    T  Ethernet24
#
#- name: Configure switch port of interfaces
#  sonic_l2_interfaces:
#    config:
#      - name: Ethernet12
#        access:
#          vlan: 10
#    state: merged
#
# After state:
# ------------
#
#do show Vlan
#Q: A - Access (Untagged), T - Tagged
#NUM        Status      Q Ports
#10         Inactive    A  Ethernet12
#11         Inactive    T  Ethernet24
#12         Inactive    T  Ethernet24
#
#
# Using merged
#
# Before state:
# -------------
#
#do show Vlan
#Q: A - Access (Untagged), T - Tagged
#NUM        Status      Q Ports
#10         Inactive    A  Ethernet12
#
#- name: Configure switch port of interfaces
#  sonic_l2_interfaces:
#    config:
#      - name: Ethernet12
#        trunk:
#          allowed_vlans:
#             - vlan: 11
#             - vlan: 12
#    state: merged
#
# After state:
# ------------
#
#do show Vlan
#Q: A - Access (Untagged), T - Tagged
#NUM        Status      Q Ports
#10         Inactive    A  Ethernet12
#11         Inactive    T  Ethernet24
#12         Inactive    T  Ethernet24
#
#
# Using merged
#
# Before state:
# -------------
#
#do show Vlan
#Q: A - Access (Untagged), T - Tagged
#NUM        Status      Q Ports
#10         Inactive
#11         Inactive
#12         Inactive    A  Ethernet13
#13         Inactive    T  Ethernet13
#14         Inactive    A  Ethernet14
#15         Inactive    T  Ethernet14
#
#- name: Configure switch port of interfaces
#  sonic_l2_interfaces:
#    config:
#      - name: Ethernet12
#        access:
#          vlan: 12
#        trunk:
#          allowed_vlans:
#             - vlan: 13
#             - vlan: 14
#    state: merged
#
# After state:
# ------------
#
#do show Vlan
#Q: A - Access (Untagged), T - Tagged
#NUM        Status      Q Ports
#10         Inactive
#11         Inactive
#12         Inactive    A  Ethernet12
#                       A  Ethernet13
#13         Inactive    T  Ethernet12
#                       T  Ethernet13
#14         Inactive    A  Ethernet12
#                       A  Ethernet14
#15         Inactive    T  Ethernet14
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
from ansible_collections.dellemc.sonic.plugins.module_utils.network.sonic.argspec.l2_interfaces.l2_interfaces import L2_interfacesArgs
from ansible_collections.dellemc.sonic.plugins.module_utils.network.sonic.config.l2_interfaces.l2_interfaces import L2_interfaces


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(argument_spec=L2_interfacesArgs.argument_spec,
                           supports_check_mode=True)

    result = L2_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == '__main__':
    main()
