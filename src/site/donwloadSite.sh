#!/usr/bin/bash

LINK=("facebook.it" "ansa.it" "unical.it" "google.it" "wikipedia.it")

for i in "${LINK[@]}"
do
  echo "Downloading $i"
  sudo wget -e robots=off --wait 1 -H -p -k http://$i
done