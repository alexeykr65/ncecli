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
import click
from luklibs.huawei.nce import NCE
from rich.console import Console
from rich.table import Table
from rich import box
from pathlib import Path

main = click.Group(help="Query Information from Huawei NCE Fabric")


@main.command("devices", help="Query Devices")
@click.option("-t", "--type_dev", default="", help="Type of device(ex.: switch,host,firewall,edge ...)")
def devices(type_dev):
    nc.dev_print_by_type(tp=type_dev)


@main.command("dev_groups", help="Query Device Groups")
def dev_groups():
    nc.dev_group_print()


@main.command("ends", help="Query End Ports on VMs")
@click.option("-f", "--filter", default="", help="Filter by name VM")
def ends(filter):
    nc.end_ports_print(flt=filter.split(','))


@main.command("dev_links", help="Query Device Links")
@click.option("-f", "--filter", default="", help="Name of device")
@click.option("-m", "--mode", default="", help="Mode (ex.: common, int_ext) of links")
@click.option("-s", "--status", default="", help="Status of links (ex.: up, down, unknown)")
# @click.option("-se", "--statusexclude", default="", help="Status of links (up, down, unknown)")
def dev_links(filter, mode, status):
    nc.links_print(flt=filter.split(','), mode=mode, stat=status)


@main.command("host_links", help="Query Host Links")
@click.option("-f", "--filter", default="", help="Name of Host Links")
def host_links(filter):
    nc.hostLinks_print(flt=filter.split(','))


@main.command("lports", help="Query Logical Ports by Switch Name")
@click.option("-n", "--name", required=True, help="Filter by Logical Switch Name")
@click.option("-s", "--status", default="", help="Filter by Status Ports(up, down)")
def lports(name, status):
    nc.ports_print(sw=name, status=status)


@main.command("lports_all", help="Query All Logical Ports (slow)")
@click.option("-n", "--net", default="", help="Filter by Network Name")
@click.option("-f", "--filter", default="", help="Filter by Network Name")
def lports_all(filter, net):
    nc.ports_print_total(flt=filter.strip(','), net=net)


@main.command("lsw", help="Query Logical Switches")
@click.option("-f", "--filter", default="", help="Name of Switch")
@click.option("-n", "--net", default="", help="Name of Network")
def lsw(filter, net):
    nc.logic_sw_print(filter.split(','), net=net)


@main.command("lnets", help="Query All Logical Networks")
@click.option("-f", "--filter", default="", help="Name of Net")
def lnets(filter):
    nc.networks_print(filter.split(','))


@main.command("epg", help="Query EPGs")
@click.option("-r", "--router", default="", help="Filter by Name of Router")
def epg(router):
    nc.epg_print(router.split(','))


@main.command("routers", help="Query All Logical Routers")
@click.option("-f", "--filter", default="", help="Name of Router")
def routers(filter):
    nc.routers_print(filter.split(','))


@main.command("nqa", help="Query All NQA Names")
@click.option("-f", "--filter", default="", help="Filter by Name")
def nqa(filter):
    nc.nqa_print(filter.split(','))


@main.command("dhcp", help="Query DHCP Groups")
@click.option("-f", "--filter", default="", help="Filter by Name")
def dhcp(filter):
    nc.dhcp_group_print(filter.split(','))


@main.command("scapp", help="Query VPC Communication Policy App")
@click.option("-n", "--net", default="", help="Name of Network")
def scapp(net):
    nc.scapp_print(net.split(','))


@main.command("vm", help="Query route policy for VM from switches")
@click.option("-f", "--filter", required=True, help="Name of VM")
def vm(filter):
    nc.get_host_tp(hst=filter, user=username, pwd=pwd)

@main.command("mac", help="Query mac or ip address from switches")
@click.option("-m", "--mac", required=True, help="MAC address or ip address")
@click.option("-f", "--fabric", required=False, default="nce", help="Name of Fabric(srt or krv)")
@click.option("-v", "--verbose", is_flag=True, help="Show verbose with pevlan and cevlan")
def mac(fabric, mac, verbose):
    nc.get_mac_addresses(fabric=fabric, mac=mac, user=username, pwd=pwd, flag_verbose=verbose)

@main.command("cmd", help="Run command on Huawei switches ")
@click.option("-c", "--cmd", required=True, help="Command to run")
@click.option("-s", "--switch", default="", help="Name of Switches(comma separated)")
@click.option("-g", "--group", default="all", help="Group of Switches")
@click.option("-f", "--filter", default="", help="Filter output")
def cmd(cmd, switch, group, filter):
    nc.run_cmd(sw=switch, gr=group, cmd=cmd, user=username, pwd=pwd, filter=filter)

@main.command("tpol_global", help="Query Traffic Policy of Global")
@click.option("-s", "--switch", help="Name of Switche")
def tpol_global(switch):
    nc.tpol_global(hst=switch, user=username, pwd=pwd)

def get_cfg(fl):
    cfg_file = Path(Path.home(), f'inventory/{fl}')
    load_cfg = ""
    if cfg_file.exists():
        with open(cfg_file, 'r') as file:
            load_cfg = yaml.safe_load(file)
    return load_cfg


if __name__ == "__main__":
    dt = get_cfg('nce.yaml')
    assert len(dt) > 0, "Problem with loading config file "
    username = dt['username']
    URL = dt['url']
    VMM = dt['vmm']
    if 'PASSW' in os.environ:
        pwd = os.environ['PASSW']
    else:
        pwd = maskpass.askpass(prompt="Password:", mask="#")
    print_raw = False
    nc = NCE(URL=URL, login=username, password=pwd, raw=print_raw)
    exit(main())
    # flt = args.filter.split(',')
