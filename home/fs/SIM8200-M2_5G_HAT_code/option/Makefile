ifneq ($(KERNELRELEASE),)
obj-m := option.o
else  
KDIR := /usr/src/linux-headers-5.4.51-v7l+/  
PWD := $(shell pwd)
all:
	make -C $(KDIR)-I ./usb_wwan M=$(PWD) modules
clean:
	rm *.o *.ko *.mod.c modules.order Module.symvers
.PHONY:clean
endif