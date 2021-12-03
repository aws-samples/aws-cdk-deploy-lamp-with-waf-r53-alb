#!/bin/bash
sudo yum update -y
sudo yum -y install httpd php
sudo chkconfig httpd on
sudo service httpd start

## TO-DO
# EC2 hardening
# create website files and upload as part of the deployment
