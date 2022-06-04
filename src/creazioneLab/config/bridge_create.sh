#!/usr/bin/bash
# https://kashyapc.fedorapeople.org/virt/create-a-new-libvirt-bridge.txt
# 1. Create a new libvirt network (other than your default 198.162.x.x) file:
cat openstackvms.xml 
#   <network>
#     <name>openstackvms</name>
#     <uuid>d0e9964a-f91a-40c0-b769-a609aee41bf2</uuid>
#     <forward mode='nat'>
#       <nat>
#         <port start='1024' end='65535'/>
#       </nat>
#     </forward>
#     <bridge name='virbr2' stp='on' delay='0' />
#     <mac address='52:54:00:60:f8:6e'/>
#     <ip address='192.169.122.1' netmask='255.255.255.0'>
#       <dhcp>
#         <range start='192.169.122.2' end='192.169.122.254' />
#       </dhcp>
#     </ip>
#   </network>

# 2. Define the above network:
virsh net-define openstackvms.xml

# 3. Start the network and enable it for "autostart"
virsh net-start openstackvms
# virsh net-autostart openstackvms

# 4. List your libvirt networks to see if it reflects:
# virsh net-list

# 5. Optionally, list your bridge devices:
# brctl show

# Delete the network:
# virsh net-destroy openstackvms     