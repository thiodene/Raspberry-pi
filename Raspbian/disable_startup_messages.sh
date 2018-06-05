# Splash screen / Logo etc...
# Edit and update /boot/config.txt
dwc_otg.lpm_enable=0 console=serial0,115200 console=tty3 root=/dev/mmcblk0p7 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait logo.nologo vt.global_cursor_default=0 quiet 

dwc_otg.lpm_enable=0 console=serial0,115200 console=tty3 loglevel=3 logo.nologo root=/dev/mmcblk0p7 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait
