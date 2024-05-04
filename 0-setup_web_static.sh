#!/usr/bin/env bash
# sets up my web servers for web_static deployment

echo -e "\e[1;32m START\e[0m"

#packages
sudo apt-get -y update
sudo apt-get -y install nginx

echo -e "\e[1;32m Packages done\e[0m"
echo

#firewall
sudo ufw allow 'Nginx HTTP'
echo -e "\e[1;32m Allow incoming NGINX HTTP Connections\e[0m"
echo

#create directories
sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared
echo -e "\e[1;32m created directories"
echo

#my text string
echo "<h3>Welcome to reginah.tech, We do amazing things</h3>" > /data/web_static/releases/test/index.html
echo -e "\e[1;32m Added text string\e[0m"
echo

# No overwrite
if [ -d "/data/web_static/current" ];
then
    echo "path /data/web_static/current exists"
    sudo rm -rf /data/web_static/current;
fi
echo -e "\e[1;32m prevent overwrite\e[0m"
echo

#symblic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -hR ubuntu:ubuntu /data
sudo sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

sudo ln -sf '/etc/nginx/sites-available/default' '/etc/nginx/sites-enabled/default'
echo -e "\e[1;32m Created symbolic link\e[0m"
echo

 
sudo service nginx restart
echo -e "\e[1;32m restarted nginx\e[0m"
