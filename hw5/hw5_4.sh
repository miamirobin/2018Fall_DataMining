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
python3 hw5.py $2 $3 4 income.tr income.te
#./$scale -l -1 -u 1 -s range3 income.tr > income.tr.scale
#./$scale -r range3 income.te > income.te.scale
./$train -c 4 -g 0.0625 income.tr model4
./$predict income.te model4 $4
echo "Above accuracy is not the actual accuracy, test label not provided"
