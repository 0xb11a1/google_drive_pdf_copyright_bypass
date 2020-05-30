#!/bin/bash
sudo apt-get install gscan2pdf python3-pip default-jdk
pip3 install browsermob-proxy
pip3 install selenium
sudo cp geckodriver /usr/bin/geckodriver 
# sudo sed -E 's/<policy domain="coder" rights="none" pattern="PDF" \/>/<policy domain="coder" rights="read | write" pattern="PDF" \/>/g' /etc/ImageMagick-*/policy.xml