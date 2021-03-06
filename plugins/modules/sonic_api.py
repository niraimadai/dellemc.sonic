#!/usr/bin/python
#
# (c) 2015 Peter Sprygada, <psprygada@ansible.com>
# Copyright (c) 2020 Dell Inc.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for sonic_vlans
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
    'license': 'Apache 2.0'
}

DOCUMENTATION = """
---
module: sonic_api
version_added: 1.0.0
author: "Abirami N (@abirami-n)"
short_description: Manages REST operations on networking device running SONiC"
description:
  - Manages REST operations on networking device running SONiC. This module provides
    an implementation for working with SONiC REST operations in a deterministic way.
options:
  url:
    description:
      - The HTTP path of the request after 'restconf/'.
    type: path
    required: true
  body:
    description:
      - The body of the http request/response to the web service which contains the payload.
    type: raw
  method:
    description:
      - The HTTP method of the request or response.
        but it still must be a valid method accepted by the service handling the request.
    type: str
    required: true
    choices: ['GET', 'PUT', 'POST', 'PATCH', 'DELETE']
  status_code:
    description:
      - A list of valid, numeric, HTTP status code that signifies success of the request.
    type: list
    elements: int
    required: true
"""
EXAMPLES = """
- name: Check that you can connect (GET) to a page and it returns a status 200
  sonic_api:
    url: data/openconfig-interfaces:interfaces/interface=Ethernet60
    method: "GET"
    status_code: 200

- name: Append data to an existing interface using PATCH and verify if it returns status 204
  sonic_api:
    url: data/openconfig-interfaces:interfaces/interface=Ethernet60/config/description
    method: "PATCH"
    body: {"openconfig-interfaces:description": "Eth-60"}
    status_code: 204

- name: Delete associated ip-address using DELETE and verify if it returns status 204
  sonic_api:
    url: >
      data/openconfig-interfaces:interfaces/interface=Ethernet64/subinterfaces/subinterface=0/
      openconfig-if-ip:ipv4/addresses/address=1.1.1.1/config/prefix-length
    method: "DELETE"
    status_code: 204

- name: Add a vlan network-instance using PUT and verify if it returns status 204
  sonic_api:
    url: data/openconfig-network-instance:network-instances/network-instance=Vlan100/
    method: "PUT"
    body: {"openconfig-network-instance:network-instance": [{"name": "Vlan100","config": {"name": "Vlan100"}}]}
    status_code: 204

- name: Add a prefix-set to routing policy using POST and verify if it returns 201
  sonic_api:
        url: data/openconfig-routing-policy:routing-policy/defined-sets/prefix-sets/prefix-set=p1
        method: "POST"
        body: {"openconfig-routing-policy:config": {"name": "p1","mode": "IPV4" }}
        status_code: 201

"""
RETURN = """
response:
  description: The response at the network device end for the REST call which contains the status code.
  returned: always
  type: list
  sample: {"response": [ 204,{""}]}
msg:
  description: The HTTP error message from the request
  returned: HTTP Error
  type: str
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.sonic.plugins.module_utils.network.sonic.sonic import edit_config, to_request


def initiate_request(module):
    """Get all the data available in chassis"""
    url = module.params['url']
    body = module.params['body']
    method = module.params['method']
    if method == "GET" or method == "DELETE":
        request = to_request(module, [{"path": url, "method": method}])
        response = edit_config(module, request)
    elif method == "PATCH" or method == "PUT" or method == "POST":
        request = to_request(module, [{"path": url, "method": method, "data": body}])
        response = edit_config(module, request)
    return response


def main():

    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    argument_spec = dict(
        url=dict(type='path', required=True),
        body=dict(type='raw', required=False),
        method=dict(type='str', choices=['GET', 'PUT', 'PATCH', 'DELETE', 'POST'], required=True),
        status_code=dict(type='list', elements='int', required=True),
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    result = dict(
        changed=False,
    )
    response = initiate_request(module)
    response_code = response[0][0]
    status_code = module.params['status_code']
    if response_code == int(status_code[0]) and response_code in (201, 204):
        result.update({'changed': True})

    result.update({
        'response': response,
    })
    module.exit_json(**result)


if __name__ == '__main__':
    main()
