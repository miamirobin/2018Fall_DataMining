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
#./$scale -l 0 -u 1 -s range3 $2 > news.tr.scale
#./$scale -r range3 $3 > news.te.scale
./$train -c 2.0 -g 1.0 $2 model2
./$predict $3 model2 $4
