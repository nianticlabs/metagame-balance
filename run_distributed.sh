export PYTHONPATH=$(pwd)

thread_number=12
count=`expr $thread_number - 1`

for i in `seq 0 $count`
do
    python Trainer/Deep/Test/Distributed/TestDistributedDeepGIGAWoLF.py "$i" "$thread_number" &
    echo python Trainer/Deep/Test/Distributed/TestDistributedDeepGIGAWoLF.py "$i" "$thread_number"
    sleep 1
done
wait
echo Dcd Mode