#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Get Information from Huawei NCE Fabric
#
# alexeykr@gmail.com
# coding=utf-8

import json
import maskpass
import argparse
import yaml
import os
from luklibs.huawei.nce import NCE
from rich.console import Console
from rich.table import Table
from rich import box
from pathlib import Path

description = "Get information from Huawei NCE Fabric"

def get_cfg(fl):
    cfg_file = Path(Path.home(), f'inventory/{fl}')
    load_cfg = ""
    if cfg_file.exists():
        with open(cfg_file, 'r') as file:
            load_cfg = yaml.safe_load(file)
    return load_cfg


def cmdArgsParser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=description, usage=argparse.SUPPRESS)
    parser.add_argument("-d", "--dev", help="Get All Devices by Type", dest="dev", action="store_true")
    parser.add_argument("-g", "--groups", help="Get All Groups of Devices", dest="grp", action="store_true")
    parser.add_argument("-e", "--ends", help="Get all End Ports", dest="ends", action="store_true")
    parser.add_argument("-epg", "--epg", help="Get all EPG", dest="epg", action="store_true")
    parser.add_argument("-pass", "--passw", help="Get Password from keyboard", dest="passw", action="store_true")
    parser.add_argument("-s", "--switch", help="Get All Logical Switches(Brief)", dest="switch", action="store_true")
    parser.add_argument("-pm", "--pmaps", help="Get All Ports of Switches", dest="pmaps", action="store")
    parser.add_argument("-pl", "--plogic", help="Get All Ports of Switches", dest="plogic", action="store")
    parser.add_argument("-l", "--links", help="Get All Links", dest="links", action="store_true")
    parser.add_argument("-hl", "--hostlinks", help="Get All Host Links", dest="hostlinks", action="store_true")
    parser.add_argument("-hs", "--hostswitch", help="Get All Host Links in switch", dest="hostswitch", action="store_true")
    parser.add_argument("-n", "--net", help="Get All Logical Networks", dest="net", action="store_true")
    parser.add_argument("-f", "--filter", help="Filter query(comma separated)", dest="filter", action="store", default="")
    parser.add_argument("-r", "--raw", help="Print raw JSON format", dest="raw", action="store_true")
    parser.add_argument("-v", "--vmname", help="Print route policy for VM", dest="vmname", action="store")

    return parser.parse_args()


if __name__ == "__main__":
    args = cmdArgsParser()
    dt = get_cfg('nce.yaml')
    assert len(dt) > 0, "Problem with loading config file "
    username = dt['username']
    URL = dt['url']
    if args.passw:
        pwd = maskpass.askpass(prompt="Password:", mask="#")
    else:
        if 'PASSW' in os.environ:
            pwd = os.environ['PASSW']
        else:
            pwd = maskpass.askpass(prompt="Password:", mask="#")

    print_raw = False
    if args.raw:
        print_raw = True
    nc = NCE(URL=URL, login=username, password=pwd, raw=print_raw)
    flt = args.filter.split(',')
    if args.dev:
        nc.get_devices()
        nc.dev_print_by_type()

    if args.ends:
        nc.end_ports_print(flt)

    if args.grp:
        nc.get_dev_group()
        nc.dev_group_print()

    if args.links:
        nc.links_print()

    if args.hostlinks:
        nc.hostLinks_print()

    if args.hostswitch:
        nc.hostLinks_switches_print()

    if args.pmaps:
        lnet = args.pmaps
        nc.ports_print(flt, lnet)

    if args.switch:
        nc.logic_sw_print(flt)

    if args.net:
        nc.networks_print(flt)

    if args.epg:
        nc.epg_print(flt)

    if args.vmname:
        nc.get_host_tp(hst=args.vmname, user=username, pwd=pwd)

