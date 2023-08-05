fio --name=iops_8k_RW --filename=$1 --numjobs=4 --bs=8k --runtime=6300 --ioengine=libaio --direct=1 --rw=randwrite --group_reporting --iodepth=32 --time_based --randrepeat=0 --norandommap  --refill_buffers > iops_8k_RW.log &
iostat -mcdxt 1 > iostat_8k_RW.log &
sleep 6300
pkill iostat
