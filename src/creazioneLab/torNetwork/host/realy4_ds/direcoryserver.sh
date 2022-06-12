#!/usr/bin/bash
sudo /etc/init.d/tor stop
sudo -u debian-tor mkdir /var/lib/tor/keys
sudo -u debian-tor tor-gencert --create-identity-key -m 12 -a 10.0.0.103:7000 \
            -i /var/lib/tor/keys/authority_identity_key \
            -s /var/lib/tor/keys/authority_signing_key \
            -c /var/lib/tor/keys/authority_certificate

sudo -u debian-tor tor --list-fingerprint --orport 1 \
    --dirserver "x 127.0.0.1:1 ffffffffffffffffffffffffffffffffffffffff" \
    --datadirectory /var/lib/tor


finger1=$(sudo cat /var/lib/tor/keys/authority_certificate  | grep fingerprint | cut -f 2 -d ' ')
finger2=$(sudo cat /var/lib/tor/fingerprint | cut -f 2 -d ' ')
HOSTNAME=$(hostname -s)

echo $finger1   # C7DD529E00152E92B42EE3CD8B9FADF5F2839313
echo $finger2   # A0DE68BAFAAE46E1B69D29C6C72578C5007B7008
echo $HOSTNAME  # dirserver

sudo mv /etc/tor/torrc /etc/tor/torrc.bak
sudo -u debian-tor nano /etc/tor/torrc
# incollare il contenuto di torrc

sudo nano /var/www/html/router.conf
# incollare il contenuto di router.conf

sudo nano /var/www/html/client.conf
# incollare il contenuto di client.conf

sudo chown -R www-data:www-data /var/www/html
sudo /etc/init.d/tor start
sudo cat /var/log/tor/debug.log | grep "Trusted"


# 10.0.0.101
# 7FB28B3B8FBFAE5756167DB4395A15CB541FFAC8
# 52F9C69D33E6E304396339F013B5F01160AF34FF
# 
# 10.0.0.102
# B864C54C75CBA2AD8DF0DFD1BCD3A1BAF1FD68A1
# 45CB1F23B946B77875BC47AD84746B40A5129BC3
# 
# 10.0.0.103
# 3DBBD860684C84FE6B76BBFDFAF161E2A621998C
# 161562507D119F13A3D9F65257A547B69D59AB10