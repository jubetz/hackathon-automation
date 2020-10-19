#!/bin/bash

set -x
set -e

check_state(){
if [ "$?" != "0" ]; then
    echo "ERROR Previous command failed test!"
    exit 1
fi
}

echo "netq show agents"
netq show agents

echo "netq show inv br"
netq show inventory br

echo "netq check cl-version"
netq check cl-version include 0

echo "netq check agents include 0"
netq check agents include 0

echo "netq show interfaces"
netq check interfaces || echo "hey this failed"
netq show interfaces

echo "netq check mtu"
netq check mtu hostnames server01,server02,server03,server04,server05,server06,leaf01,leaf02,leaf03,leaf04,spine01,spine02,spine03,spine04 include 0
netq check mtu include 1
netq check mtu include 2

echo "netq check vlan"
netq show vlan
#leaving out border01, border02, fw1, fw2
netq check vlan hostnames server01,server02,server03,server04,server05,server06,leaf01,leaf02,leaf03,leaf04,spine01,spine02,spine03,spine04 include 0
netq check vlan include 1

echo "netq check clag"
netq show clag
netq check clag include 0
netq check clag include 1
netq check clag include 2
netq check clag include 3
netq check clag include 4
netq check clag include 5
#see issue 7 in gitlab
#netq check clag include 6
netq check clag include 7
netq check clag include 8
netq check clag include 9
netq check clag include 10

echo "netq check bgp"
netq show bgp
netq check bgp include 0
netq check bgp include 1
netq check bgp include 2

echo "netq check vxlan"
netq show vxlan
netq check vxlan include 0
#see issue 8 in gitlab
#netq check vxlan include 1

echo "netq check evpn"
netq show evpn
netq check evpn include 0
netq check evpn include 1
#netq check evpn include 2
#see issue 9 in gitlab
#netq check evpn include 3
netq check evpn include 4
netq check evpn include 5
netq check evpn include 6
netq check evpn include 7 

echo "netq check ntp"
netq show ntp
netq check ntp include 0 || echo "we love you ntp"
