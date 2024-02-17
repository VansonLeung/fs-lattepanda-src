#Update KO
uname_r=$(uname -r)
echo $(uname -a)
mv /lib/modules/$(uname -r)/kernel/drivers/usb/serial/option.ko /lib/modules/$(uname -r)/kernel/drivers/usb/serial/option_bk.ko
cp option/option.ko /lib/modules/$(uname -r)/kernel/drivers/usb/serial/
cp qmi_wwan_simcom/qmi_wwan_simcom.ko /lib/modules/$(uname -r)/kernel/drivers/net/usb
depmod
modprobe option
modprobe qmi_wwan_simcom
dmesg | grep "ttyUSB"
dmesg | grep "qmi_wwan_simcom"

#add DNS file
mkdir -p /usr/share/udhcpc
sudo chmod 777 default.script
sudo cp default.script /usr/share/udhcpc

