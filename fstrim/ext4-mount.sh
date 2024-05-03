discard=$1

umount ./mnt

sleep 120

mkfs.ext4 -F -E lazy_itable_init=0,lazy_journal_init=0 /dev/sda

sleep 120

#mount -o nodiscard /dev/sda ./mnt
mount -o $discard /dev/sda ./mnt
echo "mount success\n"



echo "\n"
echo "directory mount,,,\n"
df -h ./mnt

echo "\n"
echo "file system is,,,\n"
lsblk -d -f /dev/sda

echo "\n"
