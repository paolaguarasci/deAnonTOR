#!/bin/sh
 
sudo tunctl -t tap0

sudo ifconfig tap0 192.168.122.1
sudo ifconfig tap0 netmask 255.255.255.252
sudo ifconfig tap0 broadcast 192.168.122.3
sudo ifconfig tap0 up
 
sudo iptables -t nat -A POSTROUTING -o enp4s0 -j MASQUERADE
sudo iptables -A FORWARD -i tap0 -j ACCEPT

sudo sysctl -w net.ipv4.ip_forward=1
sudo route add -net 10.0.0.0/8 gw 192.168.122.2 dev tap0