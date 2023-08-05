fio --name=bandwidth_128k_SR --filename=$1 --numjobs=4 --bs=128k --ioengine=libaio --direct=1 --randrepeat=0 --norandommap --rw=read --group_reporting --iodepth=32 --iodepth_batch=128 --iodepth_batch_complete=128 --gtod_reduce=1 --runtime=4500 --time_based > bandwidth_128k_SR.log &
iostat -mcdxt 1 > iostat_128k_SR.log &
sleep 4500
pkill iostat
