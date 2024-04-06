umount ./mnt

sleep 120

mkfs.ext4 -F -E lazy_itable_init=0,lazy_journal_init=0 /dev/sda

mount /dev/sda ./mnt
echo "mount success\n"

echo "\n"
echo "directory mount,,,\n"
df -h ./mnt

echo "\n"
echo "file system is,,,\n"
lsblk -d -f /dev/sda

echo "\n"
