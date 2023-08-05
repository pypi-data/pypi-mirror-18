fio --name=latency_4k_RW --filename=$1 --numjobs=1 --bs=4k --runtime=30 --ioengine=libaio --direct=1 --rw=randread --group_reporting --iodepth=1 --time_based --randrepeat=0 --norandommap --refill_buffers > "latency_4k_RR_"$2".log" &
sleep 31
