# EVPN Centralized Inventory

This repository holds all the configurations for a standardized deployment using the following technologies:

* BGP underlay
* VXLAN encapsulation server connectivity
* EVPN control plane
* Centralized routing, with SVI as gateways living on border leafs

## Demo architecture

### IPAM

Servers are configured for access vlan. The servers use a route for 10.0.0.0/8 pointing to the firewall (10.1.<VLAN#>.1).

```
server01 - vlan 10 - 10.1.10.101
server02 - vlan 20 - 10.1.20.102
server04 - vlan 10 - 10.1.10.104
server05 - vlan 20 - 10.1.20.105
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

The configurations deployed by the automation in this demo will create a network infrastructure that creates L2 extension between racks. Any inter-VXLAN routed traffic will have to route between VXLANs on the border leafs.

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
ansible pod1 -i inventories/evpn_centralized/hosts -m ping
```

3) Run the ansible playbook to deploy the demo to the fabric
```
ansible-playbook playbooks/deploy.yml -i inventories/evpn_centralized/hosts --diff
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

Verify EVPN VNI entries on leaf01/leaf02:
```
cumulus@leaf01:mgmt-vrf:~$ net show evpn vni
VNI        Type VxLAN IF              # MACs   # ARPs   # Remote VTEPs  Tenant VRF
30020      L2   vni30020              13       10       2               default
30010      L2   vni30010              11       11       2               default
cumulus@leaf01:mgmt-vrf:~$
```
```
cumulus@leaf01:mgmt-vrf:~$ net show bgp evpn vni
Advertise Gateway Macip: Disabled
Advertise SVI Macip: Disabled
Advertise All VNI flag: Enabled
BUM flooding: Head-end replication
Number of L2 VNIs: 2
Number of L3 VNIs: 0
Flags: * - Kernel
  VNI        Type RD                    Import RT                 Export RT                 Tenant VRF
* 30020      L2   10.10.10.1:2          65101:30020               65101:30020              default
* 30010      L2   10.10.10.1:3          65101:30010               65101:30010              default
cumulus@leaf01:mgmt-vrf:~$
```

Verify MAC entries are being learned on bridge of leaf01/leaf02:
```
cumulus@leaf01:mgmt-vrf:~$ net show bridge macs dynamic

VLAN      Master  Interface  MAC                TunnelDest  State   Flags          LastSeen
--------  ------  ---------  -----------------  ----------  ------  -------------  --------
10        bridge  peerlink   56:01:03:11:47:22              static                 00:39:44
10        bridge  peerlink   c2:18:4f:c6:b7:58                                     00:01:19
10        bridge  vni30010   00:00:00:00:00:1a              static                 00:39:39
10        bridge  vni30010   00:60:08:69:97:ef                      offload        00:00:06
10        bridge  vni30010   0c:69:e0:a2:b1:9d              static                 00:39:38
10        bridge  vni30010   4e:98:e0:81:97:d5              static                 00:39:39
10        bridge  vni30010   9e:41:ad:5e:f5:4b              static                 00:39:39
10        bridge  vni30010   44:12:c5:47:81:78              static                 00:39:38
10        bridge  vni30010   e4:1f:a3:8a:ee:59                      offload        00:37:17
10        bridge  vni30010   e6:1f:a3:8a:ee:59                      offload        00:37:07
20        bridge  bond2      24:b9:ce:e5:de:f0                                     <1 sec
20        bridge  bond2      26:b9:ce:e5:de:f0                                     00:00:07
20        bridge  peerlink   6a:08:e9:37:a4:4c                                     00:01:19
20        bridge  peerlink   56:01:03:11:47:22              static                 00:39:44
20        bridge  vni30020   00:00:00:00:00:1a              static                 00:39:39
20        bridge  vni30020   00:60:08:69:97:ef                      offload        00:37:28
20        bridge  vni30020   0c:69:e0:a2:b1:9d              static                 00:39:38
20        bridge  vni30020   4e:98:e0:81:97:d5              static                 00:39:39
20        bridge  vni30020   9e:41:ad:5e:f5:4b              static                 00:39:39
20        bridge  vni30020   14:18:d3:43:ea:7f                      offload        00:37:30
20        bridge  vni30020   16:18:d3:43:ea:7f                      offload        00:37:28
20        bridge  vni30020   44:12:c5:47:81:78              static                 00:39:38
untagged          vni30010   00:00:00:00:00:1a  10.0.1.254  static  self           00:39:39
untagged          vni30010   00:60:08:69:97:ef  10.0.1.2            self, offload  00:00:06
untagged          vni30010   0c:69:e0:a2:b1:9d  10.0.1.254  static  self           00:39:39
untagged          vni30010   4e:98:e0:81:97:d5  10.0.1.2    static  self           00:39:39
untagged          vni30010   9e:41:ad:5e:f5:4b  10.0.1.2    static  self           00:39:39
untagged          vni30010   44:12:c5:47:81:78  10.0.1.254  static  self           00:39:39
untagged          vni30010   e4:1f:a3:8a:ee:59  10.0.1.2            self, offload  00:37:17
untagged          vni30010   e6:1f:a3:8a:ee:59  10.0.1.2            self, offload  00:37:07
untagged          vni30020   00:00:00:00:00:1a  10.0.1.254  static  self           00:39:39
untagged          vni30020   00:60:08:69:97:ef  10.0.1.2            self, offload  00:37:28
untagged          vni30020   0c:69:e0:a2:b1:9d  10.0.1.254  static  self           00:39:39
untagged          vni30020   4e:98:e0:81:97:d5  10.0.1.2    static  self           00:39:39
untagged          vni30020   9e:41:ad:5e:f5:4b  10.0.1.2    static  self           00:39:39
untagged          vni30020   14:18:d3:43:ea:7f  10.0.1.2            self, offload  00:37:30
untagged          vni30020   16:18:d3:43:ea:7f  10.0.1.2            self, offload  00:37:28
untagged          vni30020   44:12:c5:47:81:78  10.0.1.254  static  self           00:39:39
```

Verify ARP entry for gateways of `10.1.10.1` on `server01` and `10.1.20.1` on `server02`:
```
cumulus@server01:~$ ip neigh show
10.1.10.104 dev uplink lladdr e4:1f:a3:8a:ee:59 STALE
10.1.10.1 dev uplink lladdr 00:00:00:00:00:1a STALE
192.168.200.1 dev eth0 lladdr 8c:2d:5d:3e:18:d7 REACHABLE
fe80::5401:3ff:fe11:4722 dev uplink lladdr 56:01:03:11:47:22 STALE
fe80::e69:e0ff:fea2:b19d dev uplink lladdr 0c:69:e0:a2:b1:9d router STALE
fe80::9cd2:5ff:fe93:a5cf dev uplink lladdr 9e:d2:05:93:a5:cf STALE
```

```
cumulus@server02:~$ ip neigh show
10.1.20.1 dev uplink lladdr 00:00:00:00:00:1a STALE
192.168.200.1 dev eth0 lladdr 8c:2d:5d:3e:18:d7 REACHABLE
fe80::9cd2:5ff:fe93:a5cf dev uplink lladdr 9e:d2:05:93:a5:cf STALE
fe80::5401:3ff:fe11:4722 dev uplink lladdr 56:01:03:11:47:22 STALE
fe80::e69:e0ff:fea2:b19d dev uplink lladdr 0c:69:e0:a2:b1:9d router STALE
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
Route Distinguisher: 10.10.10.63:2
*  [2]:[0]:[0]:[48]:[00:00:00:00:00:1a]:[32]:[10.1.20.1]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30020 ET:8 Default Gateway
*> [2]:[0]:[0]:[48]:[00:00:00:00:00:1a]:[32]:[10.1.20.1]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30020 ET:8 Default Gateway
*  [2]:[0]:[0]:[48]:[00:00:00:00:00:1a]:[128]:[fe80::200:ff:fe00:1a]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30020 ET:8 Default Gateway ND:Router Flag
*> [2]:[0]:[0]:[48]:[00:00:00:00:00:1a]:[128]:[fe80::200:ff:fe00:1a]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30020 ET:8 Default Gateway ND:Router Flag
*  [2]:[0]:[0]:[48]:[0c:69:e0:a2:b1:9d]:[32]:[10.1.20.2]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30020 ET:8 Default Gateway
*> [2]:[0]:[0]:[48]:[0c:69:e0:a2:b1:9d]:[32]:[10.1.20.2]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30020 ET:8 Default Gateway
*  [2]:[0]:[0]:[48]:[0c:69:e0:a2:b1:9d]:[128]:[fe80::e69:e0ff:fea2:b19d]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30020 ET:8 Default Gateway ND:Router Flag
*> [2]:[0]:[0]:[48]:[0c:69:e0:a2:b1:9d]:[128]:[fe80::e69:e0ff:fea2:b19d]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30020 ET:8 Default Gateway ND:Router Flag
*  [2]:[0]:[0]:[48]:[44:12:c5:47:81:78]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30020 ET:8 MM:0, sticky MAC
*> [2]:[0]:[0]:[48]:[44:12:c5:47:81:78]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30020 ET:8 MM:0, sticky MAC
*  [3]:[0]:[32]:[10.0.1.254]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30020 ET:8
*> [3]:[0]:[32]:[10.0.1.254]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30020 ET:8
Route Distinguisher: 10.10.10.63:3
*  [2]:[0]:[0]:[48]:[00:00:00:00:00:1a]:[32]:[10.1.10.1]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30010 ET:8 Default Gateway
*> [2]:[0]:[0]:[48]:[00:00:00:00:00:1a]:[32]:[10.1.10.1]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30010 ET:8 Default Gateway
*  [2]:[0]:[0]:[48]:[00:00:00:00:00:1a]:[128]:[fe80::200:ff:fe00:1a]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30010 ET:8 Default Gateway ND:Router Flag
*> [2]:[0]:[0]:[48]:[00:00:00:00:00:1a]:[128]:[fe80::200:ff:fe00:1a]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30010 ET:8 Default Gateway ND:Router Flag
*  [2]:[0]:[0]:[48]:[0c:69:e0:a2:b1:9d]:[32]:[10.1.10.2]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30010 ET:8 Default Gateway
*> [2]:[0]:[0]:[48]:[0c:69:e0:a2:b1:9d]:[32]:[10.1.10.2]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30010 ET:8 Default Gateway
*  [2]:[0]:[0]:[48]:[0c:69:e0:a2:b1:9d]:[128]:[fe80::e69:e0ff:fea2:b19d]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30010 ET:8 Default Gateway ND:Router Flag
*> [2]:[0]:[0]:[48]:[0c:69:e0:a2:b1:9d]:[128]:[fe80::e69:e0ff:fea2:b19d]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30010 ET:8 Default Gateway ND:Router Flag
*  [2]:[0]:[0]:[48]:[44:12:c5:47:81:78]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30010 ET:8 MM:0, sticky MAC
*> [2]:[0]:[0]:[48]:[44:12:c5:47:81:78]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30010 ET:8 MM:0, sticky MAC
*  [3]:[0]:[32]:[10.0.1.254]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30010 ET:8
*> [3]:[0]:[32]:[10.0.1.254]
                    10.0.1.254                             0 65199 65254 i
                    RT:65254:30010 ET:8
```
<!-- AIR:tour -->
