# EVPN Symmetric Inventory

This repository holds all the configurations for a standardized deployment using the following technologies:

* BGP underlay
* VXLAN encapsulation server connectivity
* EVPN symmetric mode control plane
* Distributed gateway routing, with SVI as gateways living on border leafs


## Demo architecture

### IPAM

Servers are configured for access vlan. The servers use a route for 10.0.0.0/8 pointing to the firewall (10.1.<VLAN#>.1).

```
server01 - vlan 10 - 10.1.10.101
server02 - vlan 20 - 10.1.20.102
server03 - vlan 30 - 10.1.30.103
server04 - vlan 10 - 10.1.10.104
server05 - vlan 20 - 10.1.20.105
server06 - vlan 30 - 10.1.30.106
leaf01   - vlan 10 - 10.1.10.1/10.1.10.2 - vrf RED
         - vlan 20 - 10.1.20.1/10.1.20.2 - vrf RED
         - vlan 30 - 10.1.30.1/10.1.30.2 - vrf BLUE
leaf02   - vlan 10 - 10.1.10.1/10.1.10.3 - vrf RED
         - vlan 20 - 10.1.20.1/10.1.20.3 - vrf RED
         - vlan 30 - 10.1.30.1/10.1.30.3 - vrf BLUE
leaf03   - vlan 10 - 10.1.10.1/10.1.10.4 - vrf RED
         - vlan 20 - 10.1.20.1/10.1.20.4 - vrf RED
         - vlan 30 - 10.1.30.1/10.1.30.4 - vrf BLUE
leaf04   - vlan 10 - 10.1.10.1/10.1.10.5 - vrf RED
         - vlan 20 - 10.1.20.1/10.1.20.5 - vrf RED
         - vlan 30 - 10.1.30.1/10.1.30.5 - vrf BLUE
border01 - vlan 10 - 10.1.10.1/10.1.10.2
         - vlan 20 - 10.1.20.1/10.1.20.2
border02 - vlan 10 - 10.1.10.1/10.1.10.3
         - vlan 20 - 10.1.20.1/10.1.20.3
```

### Features

This automation repo is used to demonstrate the following features:
 * BGP unnumbered underlay fabric
 * VXLAN overlay encapsulation data plane
 * EVPN overlay control plane

### PTM

```
cumulus@leaf01:mgmt-vrf:~$ sudo ptmctl -dl
------------------------------------------------------------------------------------------
port   cbl     exp            act            sysname   portID  portDescr    match   last
       status  nbr            nbr                                           on      upd
------------------------------------------------------------------------------------------
swp1   pass    server01:eth1  server01:eth1  server01  eth1    eth1         IfName   2s
swp2   pass    server02:eth1  server02:eth1  server02  eth1    eth1         IfName   2s
swp49  pass    leaf02:swp49   leaf02:swp49   leaf02    swp49   peerlink     IfName   2s
swp50  pass    leaf02:swp50   leaf02:swp50   leaf02    swp50   peerlink     IfName   2s
swp51  pass    spine01:swp1   spine01:swp1   spine01   swp1    fabric link  IfName   2s
swp52  pass    spine02:swp1   spine02:swp1   spine02   swp1    fabric link  IfName   2s
swp53  pass    spine03:swp1   spine03:swp1   spine03   swp1    fabric link  IfName   2s
swp54  pass    spine04:swp1   spine04:swp1   spine04   swp1    fabric link  IfName   2s
```

## Automation

### Ansible

Prerequisites:
- Cumulus Linux Reference Topology (cldemo2) has already been started and is running
- From a shell session on the oob-mgmt-server inside of the simulation

**Note: If you used the start-script.sh to start the simulation, the directory is already present on the oob-mgmt-server**

1) Clone the repo
```
git clone https://gitlab.com/cumulus-consulting/goldenturtle/cumulus_ansible_modules.git && cd cumulus_ansible_modules
```

2) Test ansible
```
ansible pod1 -i inventories/evpn_symmetric/hosts -m ping
```

3) Run the ansible playbook to deploy the demo to the fabric
```
ansible-playbook playbooks/deploy.yml -i inventories/evpn_symmetric/hosts --diff
```

### Playbook Structure

The playbooks have the following important structure:
* Variables and inventories are stored in the same directory `inventories/`
* Backup configurations are stored in `configs/`
<!-- AIR:tour -->
## Validate

### Server to Server connectivity

Log into `server01`:
```
cumulus@oob-mgmt-server:~$ ssh server01
Warning: Permanently added 'server01' (ECDSA) to the list of known hosts.
Welcome to Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-70-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon Nov 25 15:27:42 PST 2019

  System load:  0.0               Processes:             83
  Usage of /:   18.7% of 9.29GB   Users logged in:       0
  Memory usage: 12%               IP address for eth0:   192.168.200.14
  Swap usage:   0%                IP address for uplink: 10.1.10.101

 * Overheard at KubeCon: "microk8s.status just blew my mind".

     https://microk8s.io/docs/commands#microk8s.status

23 packages can be updated.
0 updates are security updates.


Last login: Mon Nov 25 15:00:38 2019 from 192.168.200.1
cumulus@server01:~$
```

Ping `server04` from `server01` to validate L2 intra-VLAN connectivity:
```
cumulus@server01:~$ ping 10.1.10.104
PING 10.1.10.104 (10.1.10.104) 56(84) bytes of data.
64 bytes from 10.1.10.104: icmp_seq=1 ttl=64 time=7.68 ms
64 bytes from 10.1.10.104: icmp_seq=2 ttl=64 time=4.32 ms
^C
--- 10.1.10.104 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 4.324/6.002/7.680/1.678 ms
```

Ping `server02` from `server01` to validate L3 inter-VLAN connectivity:
```
cumulus@server01:~$ ping 10.1.20.102
PING 10.1.20.102 (10.1.20.102) 56(84) bytes of data.
64 bytes from 10.1.20.102: icmp_seq=1 ttl=63 time=8.20 ms
64 bytes from 10.1.20.102: icmp_seq=2 ttl=63 time=5.61 ms
^C
--- 10.1.20.102 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 5.614/6.910/8.206/1.296 ms
```

Ping `server03` from `server01` to validate L3 inter-VLAN connectivity is not allowed between VRF:
```
cumulus@server01:~$ ping 10.1.30.103
PING 10.1.30.103 (10.1.30.103) 56(84) bytes of data.
From 10.1.10.3 icmp_seq=1 Destination Host Unreachable
From 10.1.10.3 icmp_seq=2 Destination Host Unreachable
^C
--- 10.1.30.103 ping statistics ---
2 packets transmitted, 0 received, +2 errors, 100% packet loss, time 1032ms
```

Verify EVPN VNI entries on leaf01/leaf02:
```
cumulus@leaf01:mgmt-vrf:~$ net show evpn vni
VNI        Type VxLAN IF              # MACs   # ARPs   # Remote VTEPs  Tenant VRF
30020      L2   vni30020              13       8        2               RED
30010      L2   vni30010              11       8        2               RED
30030      L2   vni30030              10       5        2               BLUE
3004002    L3   L3VNI_BLUE            0        0        n/a             BLUE
3004001    L3   L3VNI_RED             2        1        n/a             RED
```
```
cumulus@leaf01:mgmt-vrf:~$ net show bgp evpn vni
Advertise Gateway Macip: Disabled
Advertise SVI Macip: Disabled
Advertise All VNI flag: Enabled
BUM flooding: Head-end replication
Number of L2 VNIs: 3
Number of L3 VNIs: 2
Flags: * - Kernel
  VNI        Type RD                    Import RT                 Export RT                 Tenant VRF
* 30020      L2   10.10.10.1:4          65101:30020               65101:30020              RED
* 30010      L2   10.10.10.1:6          65101:30010               65101:30010              RED
* 30030      L2   10.10.10.1:5          65101:30030               65101:30030              BLUE
* 3004001    L3   10.10.10.1:2          65101:3004001             65101:3004001            RED
* 3004002    L3   10.10.10.1:3          65101:3004002             65101:3004002            BLUE
```

Verify MAC entries are being learned on bridge of leaf01/leaf02:
```
cumulus@leaf01:mgmt-vrf:~$ net show bridge macs dynamic

VLAN      Master  Interface  MAC                TunnelDest  State   Flags          LastSeen
--------  ------  ---------  -----------------  ----------  ------  -------------  --------
10        bridge  peerlink   00:60:08:69:97:ef                                     00:00:23
10        bridge  peerlink   56:01:03:11:47:22              static                 00:05:04
10        bridge  peerlink   c2:18:4f:c6:b7:58                                     00:00:37
10        bridge  vni30010   0c:69:e0:a2:b1:9d              static                 00:05:01
10        bridge  vni30010   4e:98:e0:81:97:d5              static                 00:05:01
10        bridge  vni30010   7a:e6:4b:f5:63:c3                      offload        00:04:35
10        bridge  vni30010   9e:41:ad:5e:f5:4b              static                 00:05:01
10        bridge  vni30010   44:12:c5:47:81:78              static                 00:05:01
10        bridge  vni30010   e6:1f:a3:8a:ee:59                      offload        00:05:01
20        bridge  bond2      24:b9:ce:e5:de:f0                                     00:02:06
20        bridge  bond2      26:b9:ce:e5:de:f0                                     00:00:25
20        bridge  peerlink   6a:08:e9:37:a4:4c                                     00:00:37
20        bridge  peerlink   56:01:03:11:47:22              static                 00:05:04
20        bridge  vni30020   00:60:08:69:97:ef                      offload        00:05:01
20        bridge  vni30020   0c:69:e0:a2:b1:9d              static                 00:05:01
20        bridge  vni30020   4e:98:e0:81:97:d5              static                 00:05:01
20        bridge  vni30020   9e:41:ad:5e:f5:4b              static                 00:05:01
20        bridge  vni30020   14:18:d3:43:ea:7f                      offload        00:05:01
20        bridge  vni30020   16:18:d3:43:ea:7f                      offload        00:05:01
20        bridge  vni30020   44:12:c5:47:81:78              static                 00:05:01
30        bridge  bond3      00:60:08:69:97:ef                                     00:00:25
30        bridge  peerlink   56:01:03:11:47:22              static                 00:05:04
30        bridge  peerlink   ea:63:fb:86:a8:d3                                     00:00:37
30        bridge  vni30030   4e:98:e0:81:97:d5              static                 00:05:01
30        bridge  vni30030   8a:1a:c0:10:68:94                      offload        00:05:01
30        bridge  vni30030   9e:41:ad:5e:f5:4b              static                 00:05:01
30        bridge  vni30030   f0:bb:f8:c9:f9:70                      offload        00:05:01
30        bridge  vni30030   f2:bb:f8:c9:f9:70                      offload        00:05:01
4001      bridge  L3VNI_RED  4e:98:e0:81:97:d5                      offload        00:04:30
4001      bridge  L3VNI_RED  9e:41:ad:5e:f5:4b                      offload        00:05:01
4001      bridge  peerlink   56:01:03:11:47:22              static                 00:05:04
4002      bridge  peerlink   56:01:03:11:47:22              static                 00:05:04
untagged          L3VNI_RED  4e:98:e0:81:97:d5  10.0.1.2            self, offload  00:04:30
untagged          L3VNI_RED  9e:41:ad:5e:f5:4b  10.0.1.2            self, offload  00:05:01
untagged          vni30010   0c:69:e0:a2:b1:9d  10.0.1.254  static  self           00:05:01
untagged          vni30010   4e:98:e0:81:97:d5  10.0.1.2    static  self           00:05:01
untagged          vni30010   7a:e6:4b:f5:63:c3  10.0.1.2            self, offload  00:04:35
untagged          vni30010   9e:41:ad:5e:f5:4b  10.0.1.2    static  self           00:05:01
untagged          vni30010   44:12:c5:47:81:78  10.0.1.254  static  self           00:05:01
untagged          vni30010   e6:1f:a3:8a:ee:59  10.0.1.2            self, offload  00:05:01
untagged          vni30020   00:60:08:69:97:ef  10.0.1.2            self, offload  00:05:01
untagged          vni30020   0c:69:e0:a2:b1:9d  10.0.1.254  static  self           00:05:01
untagged          vni30020   4e:98:e0:81:97:d5  10.0.1.2    static  self           00:05:01
untagged          vni30020   9e:41:ad:5e:f5:4b  10.0.1.2    static  self           00:05:01
untagged          vni30020   14:18:d3:43:ea:7f  10.0.1.2            self, offload  00:05:01
untagged          vni30020   16:18:d3:43:ea:7f  10.0.1.2            self, offload  00:05:01
untagged          vni30020   44:12:c5:47:81:78  10.0.1.254  static  self           00:05:01
untagged          vni30030   4e:98:e0:81:97:d5  10.0.1.2    static  self           00:05:01
untagged          vni30030   8a:1a:c0:10:68:94  10.0.1.2            self, offload  00:05:01
untagged          vni30030   9e:41:ad:5e:f5:4b  10.0.1.2    static  self           00:05:01
untagged          vni30030   f0:bb:f8:c9:f9:70  10.0.1.2            self, offload  00:05:01
untagged          vni30030   f2:bb:f8:c9:f9:70  10.0.1.2            self, offload  00:05:01
```

Verify neighbor entries are being learned on leaf01/leaf02:
```
cumulus@leaf01:mgmt-vrf:~$ ip neighbor show
10.1.10.101 dev vlan10 lladdr c2:18:4f:c6:b7:58 REACHABLE
169.254.0.1 dev swp52 lladdr 6e:4b:8a:4a:70:07 PERMANENT
10.1.20.102 dev vlan20 lladdr 24:b9:ce:e5:de:f0 REACHABLE
10.1.10.101 dev vlan10-v0 lladdr c2:18:4f:c6:b7:58 STALE
10.1.20.3 dev vlan20 lladdr 56:01:03:11:47:22 PERMANENT
10.1.10.104 dev vlan10 lladdr 7a:e6:4b:f5:63:c3 offload NOARP
10.0.1.2 dev vlan4001 lladdr 9e:41:ad:5e:f5:4b offload NOARP
10.1.20.105 dev vlan20 lladdr 14:18:d3:43:ea:7f offload NOARP
169.254.0.1 dev peerlink.4094 lladdr 56:01:03:11:47:22 PERMANENT
10.1.20.102 dev vlan20-v0 lladdr 24:b9:ce:e5:de:f0 STALE
10.1.30.3 dev vlan30 lladdr 56:01:03:11:47:22 PERMANENT
10.1.10.3 dev vlan10 lladdr 56:01:03:11:47:22 PERMANENT
169.254.0.1 dev swp53 lladdr 36:8e:7e:3b:50:da PERMANENT
192.168.200.1 dev eth0 lladdr 8c:2d:5d:3e:18:d7 REACHABLE
169.254.0.1 dev swp51 lladdr 08:39:f8:e1:75:6d PERMANENT
169.254.0.1 dev swp54 lladdr 44:86:d1:fa:df:24 PERMANENT
```

Verify routes are learned over L3VNI for inter-VLAN routed peers:
```
cumulus@leaf01:mgmt-vrf:~$ net show route vrf RED
show ip route vrf RED
======================
Codes: K - kernel route, C - connected, S - static, R - RIP,
       O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, D - SHARP,
       F - PBR,
       > - selected route, * - FIB route


VRF RED:
K * 0.0.0.0/0 [255/8192] unreachable (ICMP unreachable), 00:06:16
C * 10.1.10.0/24 is directly connected, vlan10-v0, 00:06:08
C>* 10.1.10.0/24 is directly connected, vlan10, 00:06:08
B>* 10.1.10.104/32 [20/0] via 10.0.1.2, vlan4001 onlink, 00:05:35
C * 10.1.20.0/24 is directly connected, vlan20-v0, 00:06:08
C>* 10.1.20.0/24 is directly connected, vlan20, 00:06:08
B>* 10.1.20.105/32 [20/0] via 10.0.1.2, vlan4001 onlink, 00:06:07
```

Verify that MAC address of gateway is being populated into EVPN:
```
cumulus@leaf01:mgmt-vrf:~$ net show bgp l2vpn evpn route
BGP table version is 7, local router ID is 10.10.10.1
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal
Origin codes: i - IGP, e - EGP, ? - incomplete
EVPN type-2 prefix: [2]:[ESI]:[EthTag]:[MAClen]:[MAC]:[IPlen]:[IP]
EVPN type-3 prefix: [3]:[EthTag]:[IPlen]:[OrigIP]
EVPN type-5 prefix: [5]:[ESI]:[EthTag]:[IPlen]:[IP]

   Network          Next Hop            Metric LocPrf Weight Path
                    Extended Community
...
Route Distinguisher: 10.10.10.4:4
...
*  [2]:[0]:[0]:[48]:[14:18:d3:43:ea:7f]:[32]:[10.1.20.105]
                    10.0.1.2                               0 65199 65102 i
                    RT:65102:30020 RT:65102:3004001 ET:8 Rmac:4e:98:e0:81:97:d5
*  [2]:[0]:[0]:[48]:[14:18:d3:43:ea:7f]:[32]:[10.1.20.105]
                    10.0.1.2                               0 65199 65102 i
                    RT:65102:30020 RT:65102:3004001 ET:8 Rmac:4e:98:e0:81:97:d5
*  [2]:[0]:[0]:[48]:[14:18:d3:43:ea:7f]:[32]:[10.1.20.105]
                    10.0.1.2                               0 65199 65102 i
                    RT:65102:30020 RT:65102:3004001 ET:8 Rmac:4e:98:e0:81:97:d5
*> [2]:[0]:[0]:[48]:[14:18:d3:43:ea:7f]:[32]:[10.1.20.105]
                    10.0.1.2                               0 65199 65102 i
                    RT:65102:30020 RT:65102:3004001 ET:8 Rmac:4e:98:e0:81:97:d5
...
Route Distinguisher: 10.10.10.4:6
...
*  [2]:[0]:[0]:[48]:[7a:e6:4b:f5:63:c3]:[32]:[10.1.10.104]
                    10.0.1.2                               0 65199 65102 i
                    RT:65102:30010 RT:65102:3004001 ET:8 Rmac:4e:98:e0:81:97:d5
*  [2]:[0]:[0]:[48]:[7a:e6:4b:f5:63:c3]:[32]:[10.1.10.104]
                    10.0.1.2                               0 65199 65102 i
                    RT:65102:30010 RT:65102:3004001 ET:8 Rmac:4e:98:e0:81:97:d5
*  [2]:[0]:[0]:[48]:[7a:e6:4b:f5:63:c3]:[32]:[10.1.10.104]
                    10.0.1.2                               0 65199 65102 i
                    RT:65102:30010 RT:65102:3004001 ET:8 Rmac:4e:98:e0:81:97:d5
*> [2]:[0]:[0]:[48]:[7a:e6:4b:f5:63:c3]:[32]:[10.1.10.104]
                    10.0.1.2                               0 65199 65102 i
                    RT:65102:30010 RT:65102:3004001 ET:8 Rmac:4e:98:e0:81:97:d5
```
<!-- AIR:tour -->
