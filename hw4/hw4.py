#################
##  hw4         #
##  r06921048   #
##  Yo-Chi Lee  #
#################


import numpy as np
import pandas as pd
import sys
import os
import timeit
from sklearn import tree
from sklearn import naive_bayes
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
    
    if hwNumber=='1':
        for i in range(len(data_train)):
            data_list=list(data_train[i])
            target=data_list.pop()
            y_train.append(float(target))
            for j in range(len(data_list)):
                data_list[j]=float(data_list[j])
            x_train.append(data_list)

        for i in range(len(data_test)):
            data_list=list(data_test[i])
            target=data_list.pop()
            y_test.append(float(target))
            for j in range(len(data_list)):
                data_list[j]=float(data_list[j])
            x_test.append(data_list)

    elif hwNumber=='2' :
 
        for i in range(len(data_train)):
            data_list=list(data_train[i])
            target=data_list.pop()
            y_train.append(float(target))
            for j in range(len(data_list)):
                
                data_list[j]=ord(data_list[j])
 
            x_train.append(data_list)
        boundary=len(x_train)
        for i in range(len(data_test)):
            data_list=list(data_test[i])
            target=data_list.pop()
            y_test.append(float(target))
            for j in range(len(data_list)):
                
                data_list[j]=ord(data_list[j])
 
            x_test.append(data_list)
            x_train.append(data_list)

        
        df = pd.DataFrame(np.array(x_train))
        for i in range(0,len(x_train[0])):
            
            one_hot=pd.get_dummies(df[i] , prefix='c'+str(i) )
           
            if i!=10 :
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
        
        

    elif hwNumber=='3':
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

        for i in range(len(data_test)):
            data_list=list(data_test[i])
            #target=data_list.pop()
            #y_test.append(float(target))
            for j in range(len(data_list)):
                number=0
                for k in data_list[j]:
                    number=number+ord(k)

                data_list[j]=number
            x_test.append(data_list)
        
        imp = SimpleImputer(missing_values=95, strategy='mean')
        imp = imp.fit(x_train)
        x_train = imp.transform(x_train)

        imp = SimpleImputer(missing_values=95, strategy='mean')
        imp = imp.fit(x_test)
        x_test = imp.transform(x_test)



    return x_train, y_train, x_test, y_test

def Train_Predict (x_train, y_train, x_test, y_test, hwNumber, model):
    baseline=100.0
    accuracy=0.0
    clf=None
    if model=='D':
        if hwNumber=='2':
            baseline=99.1
            clf = tree.DecisionTreeClassifier(
                    criterion='gini',
                    splitter='best',
                    random_state=2,
                    max_depth=None,
                    min_samples_split=10,
                    max_features=None,
                    max_leaf_nodes=None,
                    min_impurity_decrease=0.0)

        elif hwNumber=='1':
            baseline=61.1
            clf = tree.DecisionTreeClassifier(
                    criterion='gini',
                    splitter='random',
                    random_state=47,
                    max_depth=None,
                    min_samples_split=10,
                    max_features=None,
                    max_leaf_nodes=None,
                    min_impurity_decrease=0.0)
        elif hwNumber=='3':
            baseline=85.1
            clf = tree.DecisionTreeClassifier(
                    criterion='gini',
                    splitter='best',
                    random_state=1,
                    max_depth=None,
                    min_samples_split=600,
                    max_features=None,
                    max_leaf_nodes=None,
                    min_impurity_decrease=0.0)

        else :
            print ("Error!")     
            return
    elif model=='N':
        if hwNumber=='2':
            baseline=98.1
            clf = naive_bayes.GaussianNB(priors=[0.5, 0.5],var_smoothing=3e-3 )
            
        elif  hwNumber=='1':
            baseline=85.1
            clf = naive_bayes.MultinomialNB(alpha=0.05,fit_prior=True, class_prior=None)
            
        elif hwNumber=='3':
            baseline=85.1
            clf = naive_bayes.GaussianNB(var_smoothing=1e-04)
        else :
            print ("Error!")
            return
       
    
    
    if accuracy<baseline :   
            
        clf.fit(x_train, y_train)
        test_y_predicted = clf.predict(x_test)
        point=0
        if (len(y_test)==0):
            print ('No test label')
        else :
            for i in range (len(y_test) ):
                if int(test_y_predicted[i])==y_test[i] :
                    point=point+1
        if point>0:
            accuracy=point*100.0/(len(y_test))
           
             

        else :
            return test_y_predicted, None
        

        #tree.export_graphviz(clf, out_file='tree.dot')
        #os.system("dot -Tpng tree.dot -o tree.png")
        #print (accuracy,' ',baseline)

    return test_y_predicted, accuracy

def Output( outFile, result):
    f = open(outFile,"w" )
    for i in range (len(result) ):
        print (int(result[i]),file=f)    
    f.close()

if __name__ == '__main__':
    start = timeit.default_timer()
    x_train, y_train, x_test, y_test=Parse(sys.argv[1], sys.argv[2], sys.argv[3])
    result, accuracy=Train_Predict(x_train, y_train, x_test, y_test, sys.argv[3], sys.argv[4] )
    Output(sys.argv[5], result) 
       
    if accuracy!=None:
        printf ( "accuracy: %.2f %2s\n", accuracy,'%')
    stop = timeit.default_timer()
    printf("run time: %.2f s\n",stop-start)
