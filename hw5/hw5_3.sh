train="$1/svm-train"
predict="$1/svm-predict"
scale="$1/svm-scale"

if [ ! -f "$train" ]
then
	echo "$train not found."

fi
if [ ! -f "$predict" ]
then
        echo "$predict not found."

fi
if [ ! -f "$scale" ]
then
        echo "$scale not found."

fi
python3 hw5.py $2 $3 3 abalone.tr abalone.te
./$scale -l -1 -u 1 -s range3 abalone.tr > abalone.tr.scale
./$scale -r range3 abalone.te > abalone.te.scale
./$train -c 256 -g 0.25 abalone.tr.scale model3
./$predict abalone.te.scale model3 $4
