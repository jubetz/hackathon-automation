# EVPN L2 Only Inventory

This repository holds all the configurations for a standardized deployment using the following technologies:

* BGP underlay
* VXLAN encapsulation server connectivity
* EVPN control plane
* All server gateways live outside the VXLAN fabric

## Demo architecture

### IPAM

Servers are configured for access vlan. The servers use a route for 10.0.0.0/8 pointing to the firewall (10.1.<VLAN#>.1).

```
server01 - vlan 10 - 10.1.10.101
server02 - vlan 20 - 10.1.20.102
server04 - vlan 10 - 10.1.10.104
server05 - vlan 20 - 10.1.20.105
fw1 - vlan 10 - 10.1.10.1
fw1 - vlan 10 - 10.1.20.1
```

### Features

This automation repo is used to demonstrate the following features:
 * BGP unnumbered underlay fabric
 * VXLAN overlay encapsulation data plane
 * EVPN overlay control plane

The configurations deployed by the automation in this demo will create a network infrastructure that creates L2 extension between racks. Any inter-VXLAN routed traffic will have to route between VXLANs on an external device. In this demo, it is the `fw`.

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
ansible pod1 -i inventories/evpn_l2only/hosts -m ping
```

3) Run the ansible playbook to deploy the demo to the fabric
```
ansible-playbook playbooks/deploy.yml -i inventories/evpn_l2only/hosts --diff
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
Welcome to Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-70-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Thu Nov 21 12:39:40 PST 2019

  System load:  0.0               Processes:             83
  Usage of /:   18.5% of 9.29GB   Users logged in:       0
  Memory usage: 11%               IP address for eth0:   192.168.200.14
  Swap usage:   0%                IP address for uplink: 10.1.10.101

 * Overheard at KubeCon: "microk8s.status just blew my mind".

     https://microk8s.io/docs/commands#microk8s.status

15 packages can be updated.
0 updates are security updates.


Last login: Thu Nov 21 12:32:33 2019 from 192.168.200.1
cumulus@server01:~$
```

Ping `server04` from `server01` to validate connectivity:
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

Verify EVPN VNI entries on leaf01/leaf02:
```
cumulus@leaf01:mgmt-vrf:~$ net show evpn vni
VNI        Type VxLAN IF              # MACs   # ARPs   # Remote VTEPs  Tenant VRF
30020      L2   vni30020              10       1        2               default
30010      L2   vni30010              11       3        2               default
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
```

Verify MAC entries are being learned on bridge of leaf01/leaf02:
```
cumulus@leaf01:mgmt-vrf:~$ net show bridge macs dynamic

VLAN      Master  Interface  MAC                TunnelDest  State   Flags          LastSeen
--------  ------  ---------  -----------------  ----------  ------  -------------  --------
10        bridge  bond1      56:c0:00:62:f0:2d                                     00:00:02
10        bridge  peerlink   9a:33:a4:19:3e:6d              static                 00:14:06
10        bridge  peerlink   be:fd:71:b0:6d:59                                     00:00:44
10        bridge  vni30010   00:53:ed:56:5b:c4                      offload        00:10:59
10        bridge  vni30010   00:60:08:69:97:ef                      offload        <1 sec
10        bridge  vni30010   02:53:ed:56:5b:c4                      offload        00:10:58
10        bridge  vni30010   9c:2d:fd:34:2b:54              static                 00:14:06
10        bridge  vni30010   90:a5:81:ec:c5:8d              static                 00:14:04
10        bridge  vni30010   c2:c1:5e:bc:3b:dc              static                 00:14:06
10        bridge  vni30010   f0:a5:ce:c2:3f:8e              static                 00:14:04
20        bridge  bond2      8a:72:cc:3d:6f:e8                                     00:01:57
20        bridge  peerlink   9a:33:a4:19:3e:6d              static                 00:14:06
20        bridge  peerlink   ca:72:7f:5a:46:ce                                     00:00:44
20        bridge  vni30020   00:60:08:69:97:ef                      offload        <1 sec
20        bridge  vni30020   9c:2d:fd:34:2b:54              static                 00:14:06
20        bridge  vni30020   90:a5:81:ec:c5:8d              static                 00:14:04
20        bridge  vni30020   ae:fb:1c:98:55:81                      offload        00:10:31
20        bridge  vni30020   c2:c1:5e:bc:3b:dc              static                 00:14:06
20        bridge  vni30020   f0:a5:ce:c2:3f:8e              static                 00:14:04
untagged          vni30010   00:53:ed:56:5b:c4  10.0.1.2            self, offload  00:10:59
untagged          vni30010   00:60:08:69:97:ef  10.0.1.2            self, offload  <1 sec
untagged          vni30010   02:53:ed:56:5b:c4  10.0.1.2            self, offload  00:10:58
untagged          vni30010   9c:2d:fd:34:2b:54  10.0.1.254  static  self           00:14:06
untagged          vni30010   90:a5:81:ec:c5:8d  10.0.1.2    static  self           00:14:04
untagged          vni30010   c2:c1:5e:bc:3b:dc  10.0.1.254  static  self           00:14:06
untagged          vni30010   f0:a5:ce:c2:3f:8e  10.0.1.2    static  self           00:14:04
untagged          vni30020   00:60:08:69:97:ef  10.0.1.2            self, offload  <1 sec
untagged          vni30020   9c:2d:fd:34:2b:54  10.0.1.254  static  self           00:14:06
untagged          vni30020   90:a5:81:ec:c5:8d  10.0.1.2    static  self           00:14:04
untagged          vni30020   ae:fb:1c:98:55:81  10.0.1.2            self, offload  00:10:31
untagged          vni30020   c2:c1:5e:bc:3b:dc  10.0.1.254  static  self           00:14:06
untagged          vni30020   f0:a5:ce:c2:3f:8e  10.0.1.2    static  self           00:14:04
```

Verify that MAC address of server is being populated into EVPN
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
Route Distinguisher: 10.10.10.1:3
*> [2]:[0]:[0]:[48]:[56:c0:00:62:f0:2d]
                    10.0.1.1                           32768 i
                    ET:8 RT:65101:30010
*> [2]:[0]:[0]:[48]:[9a:33:a4:19:3e:6d]
                    10.0.1.1                           32768 i
                    ET:8 RT:65101:30010 MM:0, sticky MAC
*> [2]:[0]:[0]:[48]:[be:fd:71:b0:6d:59]
                    10.0.1.1                           32768 i
                    ET:8 RT:65101:30010
*> [2]:[0]:[0]:[48]:[be:fd:71:b0:6d:59]:[32]:[10.1.10.101]
                    10.0.1.1                           32768 i
                    ET:8 RT:65101:30010
*> [3]:[0]:[32]:[10.0.1.1]
                    10.0.1.1                           32768 i
                    ET:8 RT:65101:30010
Route Distinguisher: 10.10.10.3:2
```
<!-- AIR:tour -->
