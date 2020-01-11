###########################################################################################################
Wifi Setup
###################################################################################################################

---
- hosts: all
  remote_user: pi
  become: yes
  gather_facts: false
  vars:
    create_user: midnite
    copy_local_key: "{{ lookup('file', lookup('env','HOME') + '/.ssh/id_rsa.pub') }}"
    sys_packages: ['python-gps','gpsd','hostapd','isc-dhcp-server'] 

  tasks:
  
    - name: Install required system packages
      apt: name={{ sys_packages }} state=latest

    - name: Copy dhcp.conf
      copy:
        src: ./files/dhcp.conf
        dest: /etc/dhcp/
        owner: root
        group: dialout
        mode: 0644
        backup: yes

    - name: Copy isc-dhcp-server
      copy:
        src: ./files/isc-dhcp-server
        dest: /etc/defaults
        owner: root
        group: dialout
        mode: 0644
        backup: yes

    - name: Copy hostapd.conf
      copy:
        src: ./files/hostapd.conf
        dest: /etc/hostapd/
        owner: root
        group: dialout
        mode: 0644
        backup: yes

    - name: Copy hostapd
      copy:
        src: ./files/hostapd
        dest: /etc/default/
        owner: root
        group: dialout
        mode: 0644
        backup: yes
