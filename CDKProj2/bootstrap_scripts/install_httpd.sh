#!/bin/bash
sudo yum update
sudo yum install -y httpd
sudo chkconfig httpd on
sudo service httpd start