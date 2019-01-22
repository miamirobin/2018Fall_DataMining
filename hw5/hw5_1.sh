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
#./$scale -l -1 -u 1 -s range3 $2 > iris.tr.scale
#./$scale -r range3 $3 > iris.te.scale
./$train -t 0 $2 model1
./$predict $3 model1 $4
