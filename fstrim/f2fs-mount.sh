umount ./mnt

sleep 120

mkfs.f2fs -f /dev/sda

mount /dev/sda ./mnt
echo "mount success\n"

echo "\n"
echo "directory mount,,,\n"
df -h ./mnt

echo "\n"
echo "file system is,,,\n"
lsblk -d -f /dev/sda

echo "\n"
