fio --name=iops_8k_RR --filename=$1 --numjobs=4 --bs=8k --runtime=4500 --ioengine=libaio --direct=1 --rw=randread --group_reporting --iodepth=32 --time_based --randrepeat=0 --norandommap --refill_buffers > iops_8k_RR.log &
iostat -mcdxt 1 > iostat_8k_RR.log &
sleep 4500
pkill iostat
