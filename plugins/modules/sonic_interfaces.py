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
The module file for sonic_interfaces
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
module: sonic_interfaces
version_added: 1.0.0
short_description: 'Manages interface attributes of SONiC interfaces.'
description: 'Manages interface attributes of SONiC interfaces.'
author: 'Niraimadaiselvam M(@niraimadaiselvamm)'
notes:
  - 'Tested against SONiC-OS-3.0.1'
options:
  config:
    description: A list of interfaces configurations.
    type: list
    elements: dict
    suboptions:
      name:
        type: str
        description: The name of the interfaces
        required: true
      description:
        type: str
        description:
        - Description about the interface
      enabled:
        description:
        - It is state of shutdown state of interface.
        type: bool
      mtu:
        description:
        - MTU.
        type: int
  state:
    description:
    - The state of the configuration after module completion.
    type: str
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
# show interface status | no-more
#------------------------------------------------------------------------------------------
#Name                Description         Admin          Oper           Speed          MTU
#------------------------------------------------------------------------------------------
#Ethernet0           -                   up                            100000         9100
#Ethernet4           -                   up                            100000         9100
#Ethernet8           -                   down                          100000         9100
#Ethernet12          Ethernet-12         down                          1000           5000
#Ethernet16          -                   down                          100000         9100
#
#- name: Configure interfaces
#  sonic_interfaces:
#    config:
#      name: Ethernet12
#    state: deleted
#
# After state:
# -------------
#
# show interface status | no-more
#------------------------------------------------------------------------------------------
#Name                Description         Admin          Oper           Speed          MTU
#------------------------------------------------------------------------------------------
#Ethernet0           -                   up                            100000         9100
#Ethernet4           -                   up                            100000         9100
#Ethernet8           -                   down                          100000         9100
#Ethernet12          -                   up                            100000         9100
#Ethernet16          -                   down                          100000         9100
#
#
# Using deleted
#
# Before state:
# -------------
#
# show interface status | no-more
#------------------------------------------------------------------------------------------
#Name                Description         Admin          Oper           Speed          MTU
#------------------------------------------------------------------------------------------
#Ethernet0           -                   up                            100000         9100
#Ethernet4           -                   up                            100000         9100
#Ethernet8           -                   down                          100000         9100
#Ethernet12          -                   down                          1000           9100
#Ethernet16          -                   down                          100000         9100
#
#- name: Configure interfaces
#  sonic_interfaces:
#    config:
#
#    state: deleted
#
# After state:
# -------------
#
# show interface status | no-more
#------------------------------------------------------------------------------------------
#Name                Description         Admin          Oper           Speed          MTU
#------------------------------------------------------------------------------------------
#Ethernet0           -                   up                            100000         9100
#Ethernet4           -                   up                            100000         9100
#Ethernet8           -                   up                            100000         9100
#Ethernet12          -                   up                            100000         9100
#Ethernet16          -                   up                            100000         9100
#
#
# Using merged
#
# Before state:
# -------------
#
# show interface status | no-more
#------------------------------------------------------------------------------------------
#Name                Description         Admin          Oper           Speed          MTU
#------------------------------------------------------------------------------------------
#Ethernet0           -                   up                            100000         9100
#Ethernet4           -                   up                            100000         9100
#Ethernet8           -                   down                          100000         9100
#Ethernet12          -                   down                          1000           9100
#
#- name: Configure interfaces
#  sonic_interfaces:
#    config:
#      - name: Ethernet12
#        description: 'Ethernet Twelve'
#      - name: Ethernet16
#        description: 'Ethernet Sixteen'
#        enable: True
#        mtu: 3500
#    state: merged
#
#
# After state:
# ------------
#
# show interface status | no-more
#------------------------------------------------------------------------------------------
#Name                Description         Admin          Oper           Speed          MTU
#------------------------------------------------------------------------------------------
#Ethernet0           -                   up                            100000         9100
#Ethernet4           -                   up                            100000         9100
#Ethernet8           -                   down                          100000         9100
#Ethernet12          Ethernet Twelve     down                          1000           9100
#Ethernet16          Ethernet Sixteen    down                          100000         3500
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
from ansible_collections.dellemc.sonic.plugins.module_utils.network.sonic.argspec.interfaces.interfaces import InterfacesArgs
from ansible_collections.dellemc.sonic.plugins.module_utils.network.sonic.config.interfaces.interfaces import Interfaces


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(argument_spec=InterfacesArgs.argument_spec,
                           supports_check_mode=True)

    result = Interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == '__main__':
    main()
