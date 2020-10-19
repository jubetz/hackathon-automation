# NVIDIA Cumulus Linux Roles

[![Pipeline](https://gitlab.com/cumulus-consulting/goldenturtle/cumulus_evpn/badges/master/pipeline.svg)](https://gitlab.com/cumulus-consulting/goldenturtle/cumulus_evpn/pipelines)
[![License](https://img.shields.io/badge/License-Apache%202.0-83389B.svg)](https://opensource.org/licenses/Apache-2.0)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Slack Status](https://img.shields.io/badge/Slack-2800+-F1446F)](https://slack.cumulusnetworks.com)
[![Code of Conduct](https://img.shields.io/badge/Contributing-Code%20of%20Conduct-1EB5BD)](https://docs.cumulusnetworks.com/contributor-guide/#contributor-covenant-code-of-conduct)

<img src="https://www.ansible.com/hubfs/2016_Images/Assets/Ansible-Mark-Large-RGB-BlackOutline.png" height="150" title="Ansible" align="right" /> 
<img src="https://gitlab.com/cumulus-consulting/goldenturtle/cldemo2/-/raw/master/documentation/images/cumulus-logo.svg" height="150" title="Cumulus Networks" align="right" /> 

Modules to configure a Cumulus Linux Switch

- [NVIDIA Cumulus Linux Roles](#NVIDIA-cumulus-linux-roles)
  * [Roles](#roles)
    + [backup](roles/backup/README.md)
    + [dns](roles/dns/README.md)
    + [frr](roles/frr/README.md)
    + [hostname](roles/hostname/README.md)
    + [interfaces](roles/interfaces/README.md)
    + [motd](roles/motd/README.md)
    + [ntp](roles/ntp/README.md)
    + [ptm](roles/ptm/README.md)
    + [snmp](roles/snmp/README.md)
    + [ssh](roles/ssh/README.md)
    + [syslog](roles/syslog/README.md)
    + [tacacs_client](roles/tacacs_client/README.md)
    + [tacacs_server](roles/tacacs_server/README.md)


## How to Use

Included in this repo are 3 different demos each with their own inventories:
* [EVPN Centralized](inventories/evpn_centralized)
* [EVPN L2Only](inventories/evpn_l2only)
* [EVPN Symmetric](inventories/evpn_symmetric)

Push your configs with the correct inventory using the -i flag with ansible-playbook.
```bash
cumulus@oob-mgmt-server:~/cumulus_ansible_modules$ ansible-playbook -i inventories/evpn_centralized/hosts playbooks/deploy.yml
```


## Requirements

* NVIDIA Cumulus Linux Version
  ```bash
  cumulus@leaf01:mgmt-vrf:~$ net sh ver
  NCLU_VERSION=1.0-cl3u32
  DISTRIB_ID="Cumulus Linux"
  DISTRIB_RELEASE=3.7.12
  DISTRIB_DESCRIPTION="Cumulus Linux 3.7.12"
  ```
* Ansible Version
  ```bash
  cumulus@oob-mgmt-server:~/cumulus_ansible_modules$ ansible --version
  ansible 2.9.11
    config file = /home/cumulus/cumulus_ansible_modules/ansible.cfg
    configured module search path = ['/home/cumulus/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
    ansible python module location = /home/cumulus/.local/lib/python3.6/site-packages/ansible
    executable location = /usr/local/bin/ansible
    python version = 3.6.9 (default, Apr 18 2020, 01:56:04) [GCC 8.4.0]
  ```
* Ubuntu Version
  ```bash
  cumulus@oob-mgmt-server:~/cumulus_ansible_modules$ cat /etc/lsb-release
  DISTRIB_ID=Ubuntu
  DISTRIB_RELEASE=18.04
  DISTRIB_CODENAME=bionic
  DISTRIB_DESCRIPTION="Ubuntu 18.04.4 LTS"
  ```
