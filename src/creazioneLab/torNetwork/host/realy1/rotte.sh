#!/usr/bin/bash
ip route add 192.168.4.0/24 via 192.168.2.3 dev ens5
ip route add 192.168.3.0/24 via 192.168.2.5 dev ens5
