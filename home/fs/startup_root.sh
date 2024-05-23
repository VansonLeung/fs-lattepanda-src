#!/bin/bash

sleep 5
sudo chmod 777 /dev/i2c-0
sudo chmod 777 /dev/i2c-1
sudo chmod 777 /dev/i2c-2
sudo chmod 777 /dev/i2c-3
sudo chmod 777 /dev/i2c-4
sudo chmod 777 /dev/i2c-5
sudo chmod 777 /dev/i2c-6
sudo chmod 777 /dev/i2c-7

sleep 5
cd /home/fs/fs-lattepanda-src/home/fs/simcom-cm/ && sudo ./simcom-cm 


