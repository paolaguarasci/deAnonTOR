#!/usr/bin/bash
sudo /etc/init.d/tor stop
sudo -u debian-tor mkdir /var/lib/tor/keys
sudo -u debian-tor tor-gencert --create-identity-key -m 12 -a 192.168.1.4:7000 \
            -i /var/lib/tor/keys/authority_identity_key \
            -s /var/lib/tor/keys/authority_signing_key \
            -c /var/lib/tor/keys/authority_certificate

sudo -u debian-tor tor --list-fingerprint --orport 1 \
    --dirserver "x 127.0.0.1:1 ffffffffffffffffffffffffffffffffffffffff" \
    --datadirectory /var/lib/tor


finger1=$(sudo cat /var/lib/tor/keys/authority_certificate  | grep fingerprint | cut -f 2 -d ' ')
finger2=$(sudo cat /var/lib/tor/fingerprint | cut -f 2 -d ' ')
HOSTNAME=$(hostname -s)

echo $finger1   # 7D727F6C262E254CB501B05EFC4DE981C3C76AB9
echo $finger2   # E52F69BE42EA667C7D259B8AE211308E12F60EB9
echo $HOSTNAME  # debian

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
