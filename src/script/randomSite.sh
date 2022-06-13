#!/usr/bin/bash
ursl=("http://10.0.0.11/unical.it/" "http://10.0.0.11:81/facebook.it/" "http://10.0.0.11:82/ansa.it/" "http://10.0.0.11:83/youtube.it/" "http://10.0.0.11:84/archlinux.org/")
r=$(($RANDOM % 4 + 0))
sudo proxychains wget -p ${ursl[$r]}
