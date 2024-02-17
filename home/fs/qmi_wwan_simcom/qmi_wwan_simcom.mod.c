#include <linux/build-salt.h>
#include <linux/module.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(.gnu.linkonce.this_module) = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif

static const struct modversion_info ____versions[]
__used __section(__versions) = {
	{ 0xdad1276d, "module_layout" },
	{ 0x5832ebe2, "usbnet_disconnect" },
	{ 0xd14d0aba, "usbnet_tx_timeout" },
	{ 0xd4bce030, "usbnet_change_mtu" },
	{ 0x50d08c52, "eth_validate_addr" },
	{ 0x8914efc6, "usbnet_start_xmit" },
	{ 0xd2d3ff05, "usbnet_stop" },
	{ 0x9d610290, "usbnet_open" },
	{ 0xc7c609f9, "usb_deregister" },
	{ 0x8aaf61fc, "usb_register_driver" },
	{ 0x3ac4dce5, "skb_push" },
	{ 0xf190a1d9, "__dev_kfree_skb_any" },
	{ 0xb8ffcbb, "skb_pull" },
	{ 0x5dfde3e2, "usbnet_probe" },
	{ 0x15be6fc4, "usbnet_suspend" },
	{ 0xa2045210, "usbnet_resume" },
	{ 0xecf07ae4, "usbnet_get_ethernet_addr" },
	{ 0x79aa04a2, "get_random_bytes" },
	{ 0xad7707bd, "_dev_err" },
	{ 0x825873ad, "usb_control_msg" },
	{ 0xfc7a3fdb, "_dev_info" },
	{ 0x533cac44, "usb_cdc_wdm_register" },
	{ 0x5511e06, "usbnet_get_endpoints" },
	{ 0x508dea70, "usb_driver_claim_interface" },
	{ 0xad19ad5a, "usb_ifnum_to_if" },
	{ 0xf6344221, "eth_commit_mac_addr_change" },
	{ 0x71b63299, "eth_prepare_mac_addr_change" },
	{ 0x9b40c293, "usb_driver_release_interface" },
	{ 0x62ec45c5, "usb_autopm_put_interface" },
	{ 0x19768388, "usb_autopm_get_interface" },
	{ 0xb1ad28e0, "__gnu_mcount_nc" },
};

MODULE_INFO(depends, "cdc-wdm");

MODULE_ALIAS("usb:v1E0Ep9001d*dc*dsc*dp*ic*isc*ip*in05*");

MODULE_INFO(srcversion, "29480A58515EB2DB048A6C6");
