#!/bin/bash

set -e
set -x

echo "netq show agents"
netq show agents

echo "netq check bgp"
netq show bgp
netq check bgp include 0
netq check bgp include 1
netq check bgp include 2

echo "netq check vxlan"
netq show vxlan
netq check vxlan include 0
netq check vxlan include 1

echo "netq check evpn"
netq show evpn
netq check evpn include 0
netq check evpn include 1
#netq check evpn include 2
netq check evpn include 3
netq check evpn include 4
netq check evpn include 5
netq check evpn include 6
netq check evpn include 7 

echo "netq check clag"
netq show clag
netq check clag include 0
netq check clag include 1
netq check clag include 2
netq check clag include 3
netq check clag include 4
#netq check clag include 5
netq check clag include 6
netq check clag include 7
netq check clag include 8
netq check clag include 9
netq check clag include 10

echo "netq check cl-version"
netq check cl-version include 0

echo "netq check mtu"
#netq check mtu 0
netq check mtu include 1
netq check mtu include 2

echo "netq check ntp"
netq show ntp
netq check ntp include 0 || echo "we love you ntp"

echo "netq check vlan"
netq show vlan
netq check vlan include 0
netq check vlan include 1
