#!/bin/bash
#
# This will run in the test phase of CI if there are no site specific tests configured.
# This will not produce errors that halt/fail CI processing.

set -x

echo "netq show agents"
netq show agents

echo "netq check bgp"
netq check bgp

echo "netq check vxlan"
netq check vxlan

echo "netq check evpn"
netq check evpn

echo "netq check clag"
netq check clag

echo "netq check cl-version"
netq check cl-version

echo "netq check mtu"
netq check mtu 

echo "netq check ntp"
netq check ntp

echo "netq check vlan"
netq check vlan

exit 0

