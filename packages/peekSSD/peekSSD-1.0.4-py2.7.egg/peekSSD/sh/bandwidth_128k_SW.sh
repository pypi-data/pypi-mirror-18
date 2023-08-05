fio --name=bandwidth_128k_SW --filename=$1 --numjobs=4 --bs=128k --ioengine=libaio --direct=1 --randrepeat=0 --norandommap --rw=write --group_reporting --iodepth=32 --iodepth_batch=128 --iodepth_batch_complete=128 --gtod_reduce=1 --runtime=6300 --time_based > bandwidth_128k_SW.log &
iostat -mcdxt 1 > iostat_128k_SW.log &
sleep 6300
pkill iostat
