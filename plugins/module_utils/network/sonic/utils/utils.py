#
# -*- coding: utf-8 -*-
# Copyright 2020 Dell Inc. or its subsidiaries. All Rights Reserved
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# utils

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import socket
import re
from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    is_masklen,
    to_netmask,
    remove_empties
)


def get_diff(base_data, compare_with_data, test_keys=None):
    if isinstance(base_data, list) and isinstance(compare_with_data, list):
        dict_diff = get_diff_dict({"config": base_data}, {"config": compare_with_data}, test_keys)
        return dict_diff.get("config", [])
    else:
        return get_diff_dict(base_data, compare_with_data, test_keys)


def get_diff_dict(base_data, compare_with_data, test_keys=None):

    if test_keys is None:
        test_keys = []

    if not base_data:
        return base_data

    planned_set = set(base_data.keys())
    discovered_set = set(compare_with_data.keys())
    intersect_set = planned_set.intersection(discovered_set)
    changed_dict = {}
    has_dict_item = None
    added_set = planned_set - intersect_set
    # Keys part of added are new and put into changed_dict
    if added_set:
        for key in added_set:
            changed_dict[key] = base_data[key]
    for key in intersect_set:
        has_dict_item = False
        value = base_data[key]
        if isinstance(value, list):
            p_list = base_data[key] if key in base_data else []
            d_list = compare_with_data[key] if key in compare_with_data else []
            changed_list = []
            if p_list and d_list:
                for p_list_item in p_list:
                    matched = False
                    has_diff = False
                    for d_list_item in d_list:
                        if test_keys:
                            if (isinstance(p_list_item, dict) and isinstance(d_list_item, dict)):
                                test_keys_present = False
                                for test_key_item in test_keys:
                                    if isinstance(test_key_item, set):
                                        test_key_item = list(test_key_item)
                                    else:
                                        test_key_item = [test_key_item]

                                    key_matched = False
                                    for test_key in list(test_key_item):
                                        if test_key in set(p_list_item).intersection(d_list_item):
                                            test_keys_present = True
                                            if p_list_item[test_key] == d_list_item[test_key]:
                                                key_matched = True
                                                break
                                    if key_matched:
                                        dict_diff = get_diff_dict(p_list_item, d_list_item, test_keys)
                                        matched = True
                                        if dict_diff:
                                            has_diff = True
                                            for test_key in list(test_key_item):
                                                dict_diff.update({test_key: p_list_item[test_key]})
                                        break
                                if not matched and test_keys_present:
                                    if (isinstance(p_list_item, dict) and isinstance(d_list_item, dict)):
                                        dict_diff = get_diff_dict(p_list_item, d_list_item)
                                        if not dict_diff:
                                            matched = True
                                            break
                            else:
                                if p_list_item == d_list_item:
                                    matched = True
                                    break
                        else:
                            if (isinstance(p_list_item, dict) and isinstance(d_list_item, dict)):
                                dict_diff = get_diff_dict(p_list_item, d_list_item)
                                if not dict_diff:
                                    matched = True
                                    break
                    if test_keys:
                        if not matched:
                            changed_list.append(p_list_item)
                        elif has_diff and dict_diff:
                            changed_list.append(dict_diff)
                    else:
                        if not matched:
                            changed_list.append(p_list_item)
                if changed_list:
                    changed_dict.update({key: changed_list})
            elif p_list and (not d_list):
                changed_dict[key] = p_list
        elif (isinstance(value, dict) and isinstance(compare_with_data[key], dict)):
            dict_diff = get_diff_dict(base_data[key], compare_with_data[key], test_keys)
            if dict_diff:
                changed_dict[key] = dict_diff
        elif value is not None:
            if compare_with_data[key] != base_data[key]:
                changed_dict[key] = base_data[key]
    return changed_dict


def update_states(commands, state):
    ret_list = list()
    if commands:
        if isinstance(commands, list):
            for command in commands:
                ret = command.copy()
                ret.update({"state": state})
                ret_list.append(ret)
        elif isinstance(commands, dict):
            ret_list.append(commands.copy())
            ret_list[0].update({"state": state})
    return ret_list


def dict_to_set(sample_dict):
    # Generate a set with passed dictionary for comparison
    test_dict = dict()
    if isinstance(sample_dict, dict):
        for k, v in iteritems(sample_dict):
            if v is not None:
                if isinstance(v, list):
                    if isinstance(v[0], dict):
                        li = []
                        for each in v:
                            for key, value in iteritems(each):
                                if isinstance(value, list):
                                    each[key] = tuple(value)
                            li.append(tuple(iteritems(each)))
                        v = tuple(li)
                    else:
                        v = tuple(v)
                elif isinstance(v, dict):
                    li = []
                    for key, value in iteritems(v):
                        if isinstance(value, list):
                            v[key] = tuple(value)
                    li.extend(tuple(iteritems(v)))
                    v = tuple(li)
                test_dict.update({k: v})
        return_set = set(tuple(iteritems(test_dict)))
    else:
        return_set = set(sample_dict)
    return return_set


def validate_ipv4(value, module):
    if value:
        address = value.split("/")
        if len(address) != 2:
            module.fail_json(
                msg="address format is <ipv4 address>/<mask>, got invalid format {0}".format(
                    value
                )
            )

        if not is_masklen(address[1]):
            module.fail_json(
                msg="invalid value for mask: {0}, mask should be in range 0-32".format(
                    address[1]
                )
            )


def validate_ipv6(value, module):
    if value:
        address = value.split("/")
        if len(address) != 2:
            module.fail_json(
                msg="address format is <ipv6 address>/<mask>, got invalid format {0}".format(
                    value
                )
            )
        else:
            if not 0 <= int(address[1]) <= 128:
                module.fail_json(
                    msg="invalid value for mask: {0}, mask should be in range 0-128".format(
                        address[1]
                    )
                )


def validate_n_expand_ipv4(module, want):
    # Check if input IPV4 is valid IP and expand IPV4 with its subnet mask
    ip_addr_want = want.get("address")
    if len(ip_addr_want.split(" ")) > 1:
        return ip_addr_want
    validate_ipv4(ip_addr_want, module)
    ip = ip_addr_want.split("/")
    if len(ip) == 2:
        ip_addr_want = "{0} {1}".format(ip[0], to_netmask(ip[1]))

    return ip_addr_want


def netmask_to_cidr(netmask):
    bit_range = [128, 64, 32, 16, 8, 4, 2, 1]
    count = 0
    cidr = 0
    netmask_list = netmask.split(".")
    netmask_calc = [i for i in netmask_list if int(i) != 255 and int(i) != 0]
    if netmask_calc:
        netmask_calc_index = netmask_list.index(netmask_calc[0])
    elif sum(list(map(int, netmask_list))) == 0:
        return "32"
    else:
        return "24"
    for each in bit_range:
        if cidr == int(netmask.split(".")[2]):
            if netmask_calc_index == 1:
                return str(8 + count)
            elif netmask_calc_index == 2:
                return str(8 * 2 + count)
            elif netmask_calc_index == 3:
                return str(8 * 3 + count)
            break
        cidr += each
        count += 1


def remove_empties_from_list(config_list):
    ret_config = []
    if not config_list:
        return ret_config
    for config in config_list:
        ret_config.append(remove_empties(config))
    return ret_config


def normalize_interface_name(configs, namekey=None):
    if not namekey:
        namekey = 'name'

    if configs:
        for conf in configs:
            conf[namekey] = get_normalize_interface_name(conf[namekey])


def get_normalize_interface_name(intf_name):
    ret_intf_name = re.sub(r"\s+", "", intf_name, flags=re.UNICODE)
    ret_intf_name = ret_intf_name.capitalize()

    match = re.search(r"\d", ret_intf_name)
    if match:
        start_pos = match.start()
        name = ret_intf_name[0:start_pos]
        intf_id = ret_intf_name[start_pos:]

        if ret_intf_name.startswith("Management") or ret_intf_name.startswith("Mgmt"):
            name = "eth"
            intf_id = "0"
        elif name.startswith("Eth"):
            name = "Ethernet"
        elif name.startswith("Po"):
            name = "PortChannel"
        elif name.startswith("Vlan"):
            name = "Vlan"
        elif name.startswith("Loop"):
            name = "Loopback"

        ret_intf_name = name + intf_id

    return ret_intf_name
