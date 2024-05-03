discard=$1

umount ./mnt

sleep 120

mkfs.f2fs -f /dev/sda

sleep 120

mount -o $discard /dev/sda ./mnt
echo "mount success\n"

echo "\n"
echo "directory mount,,,\n"
df -h ./mnt

echo "\n"
echo "file system is,,,\n"
lsblk -d -f /dev/sda

echo "\n"
