# Mount the USB key port to mnt (could be different than sda1... could be sdb/ sda/ etc...)
sudo mount /dev/sda1 /mnt

# Use the data
cd /mnt

#unmount when finished using it
umount /mnt
