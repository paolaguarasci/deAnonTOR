#!/usr/bin/bash
ip route add 192.168.1.0/24 via 192.168.2.1 dev ens4
ip route add 192.168.3.0/24 via 192.168.4.6 dev ens5
