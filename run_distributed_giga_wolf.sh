export PYTHONPATH=$(pwd)

process_number=12
count=`expr $process_number - 1`

for i in `seq 0 $count`
do
  python Trainer/Deep/Test/Distributed/TestDistributedDeepGIGAWoLF.py "$i" "$process_number" &
  echo python TestDistributedDeepGIGAWoLF.py "$i" "$process_number"
  sleep 1
done
wait
echo Done!
