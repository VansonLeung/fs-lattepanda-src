cmd_/home/pi/kernel/option/option.ko := ld -r  -EL  --build-id  -T ./scripts/module-common.lds -T ./arch/arm/kernel/module.lds -o /home/pi/kernel/option/option.ko /home/pi/kernel/option/option.o /home/pi/kernel/option/option.mod.o;  true