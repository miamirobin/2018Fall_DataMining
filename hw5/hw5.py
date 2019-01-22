#################
##  hw5         #
##  r06921048   #
##  Yo-Chi Lee  #
#################


import numpy as np
import pandas as pd
import sys
import os
import timeit
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder


def printf(format, *args):
    sys.stdout.write(format % args)

def Parse(trainCSV,testCSV,hwNumber) :  
    data_train=np.genfromtxt(trainCSV,delimiter=',',dtype=str)
    data_test=np.genfromtxt(testCSV,delimiter=',',dtype=str) 

 
    x_train=[]
    y_train=[]
    x_test=[]
    y_test=[]
    
    if hwNumber=='3':
        for i in range(len(data_train)):
            data_list=list(data_train[i])
            target=data_list.pop()
            y_train.append(float(target))
            for j in range(len(data_list)):
                if j==0:
                    data_list[j]=ord(data_list[j])
                else:
                    data_list[j]=float(data_list[j])
            x_train.append(data_list)

        for i in range(len(data_test)):
            data_list=list(data_test[i])
            target=data_list.pop()
            y_test.append(float(target))
            for j in range(len(data_list)):
                if j==0:
                    data_list[j]=ord(data_list[j])
                else:
                    data_list[j]=float(data_list[j])

            x_test.append(data_list)
          
    elif hwNumber=='4':
        for i in range(len(data_train)):
            data_list=list(data_train[i])
            target=data_list.pop()
            y_train.append(float(target))
            for j in range(len(data_list)):
                number=0
                for k in data_list[j]:
                    number=number+ord(k)
                   
                data_list[j]=number
            x_train.append(data_list)
        boundary=len(x_train)
        for i in range(len(data_test)):
            data_list=list(data_test[i])
            #target=data_list.pop()
            y_test.append(float(0))
            for j in range(len(data_list)):
                number=0
                for k in data_list[j]:
                    number=number+ord(k)

                data_list[j]=number
            x_test.append(data_list)
            x_train.append(data_list)
 
        imp = SimpleImputer(missing_values=95, strategy='mean')
        imp = imp.fit(x_train)
        x_train = imp.transform(x_train)

        imp = SimpleImputer(missing_values=95, strategy='mean')
        imp = imp.fit(x_test)
        x_test = imp.transform(x_test)
        df = pd.DataFrame(np.array(x_train))
        for i in range(0,len(x_train[0])):

            one_hot=pd.get_dummies(df[i] , prefix='c'+str(i) )
            df=df.join(one_hot)
        for i in range (0,len(x_train[0])):
            df=df.drop(df.columns[0],axis=1)

        x_total=np.array(df)
        x_train=[]
        x_test=[]
        for i in range (0,len(x_total)):
            if i<boundary:
                x_train.append(x_total[i])
            else:
                x_test.append(x_total[i])




    return x_train, y_train, x_test, y_test


def Output( outFile, result):
    f = open(outFile,"w" )
    for i in range (len(result) ):
        print (int(result[i]),file=f)    
    f.close()

def OutputTrain( outFile,x_train,y_train):
    f = open(outFile,"w" )
    for i in range(len(x_train)):
        print (int(y_train[i]),end=' ',file=f)
        for j in range(len(x_train[i])):
            if x_train[i][j]!=0:
                print (j+1,end='',file=f)
                print (':',end='',file=f)
                print (x_train[i][j],end=' ',file=f)
        print ('',file=f)
    f.close()
def OutputTest (outFile,x_test,y_test):
    f = open(outFile,"w" )
    for i in range(len(x_test)):
        
        print (int(y_test[i]),end=' ',file=f)
        for j in range(len(x_test[i])):
            if x_test[i][j]!=0:
                print (j+1,end='',file=f)
                print (':',end='',file=f)
                print (x_test[i][j],end=' ',file=f)

        print ('',file=f)
        
    f.close()

if __name__ == '__main__':
    start = timeit.default_timer()
    x_train, y_train, x_test, y_test=Parse(sys.argv[1], sys.argv[2], sys.argv[3])
    OutputTrain(sys.argv[4], x_train,y_train)
    OutputTest(sys.argv[5],x_test,y_test) 
     
    stop = timeit.default_timer()
    #printf("run time: %.2f s\n",stop-start)
