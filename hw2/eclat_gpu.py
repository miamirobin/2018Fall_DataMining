#######################
# hw2 eclat          ##
# Yo-Chi Lee         ##
# r06921048          ##
#######################

import sys
import os
import timeit
import functools
import numpy as np
import pycuda.autoinit
import pycuda.driver as drv
import numpy as np
from pycuda.compiler import SourceModule

ThreadNum = 256
BlockNum= 256

mod= SourceModule("""
 #include <stdio.h>
 
__global__ void intersection(int *dest, int*a, int*b, int* index2, int*index0, int* index1)
{
  const int tid = threadIdx.x;
  const int bid = blockIdx.x;
  
  
  for (int i=bid*blockDim.x+tid;i<index0[1];i+=gridDim.x*blockDim.x){
      
    
      //dest[i] = a[i] & b[i];
     int j=0;
     int k=0;
     int count=i*index0[0];
     const int len0=index0[0];
     const int len1=index1[i];
     if (i>0){ k=index1[i-1] ;}

     while( (j<len0) and (k<len1) ){
           
            if (a[j]==b[k]){
                dest[count]=a[j];
                count++;
                j=j+1;
                k=k+1;
            }
            else if( a[j]>b[k]){
                k=k+1;
            }
            else{
                j=j+1; 
            }
     }
     index2[i]=count;       
 }
 

}  

""")


# parse the input
def parse(dict):
    f = open(sys.argv[1],"r" )
    lines = f.readlines()
    for i in range(0,len(lines)): 

        for word in lines[i].split():
            word=int(word)  
            #word=tuple([word])

            if dict.get(word)==None: 
                dict[word]=set([i])
            else:
                dict[word].add(i)              
            
           
    f.close()
    return len(lines)*float(sys.argv[2])



# compare function for sorting
def cmp_1(x, y):
    if len(x)<len(y):
        return -1 
    elif len(x) > len(y):
        return 1
    else:
        i=0
        while True:
            if x[i]<y[i]:
                return -1
            elif x[i]>y[i]:
                return 1
            else:
                i=i+1
                if i>=len(x) or i>=len(y):
                    return 0 




# eclat algorithm
def eclat(dict,x,key0,set0,MinSupport,dict_new,list0,Arr1,Index1):
    if x<0.95*len(list0):
        for i in range(x,len(list0)):
            set1=dict[list0[i]]
        
            set2=set0 & set1
        
            if len(set2)>=MinSupport:
                #print(key0,',',list0[i],end='')
                if type(key0)==int:
                    key1=[key0]
                else:
                    key1=list(key0)
                key1.append(list0[i])
                key1=tuple(key1)
                dict_new[key1]=len(set2)
                #print (key1,': ',set0 & set1)
                eclat(dict,i+1,key1,set2, MinSupport,dict_new,list0,Arr1,Index1)
        return  
      
    
    if x>=len(list0):
        return
    arr0=sorted(set0)    
    arr1=Arr1[Index1[x-1]:]
    arr2=arr0*(len(list0)-x)
    index1=Index1[x:]-Index1[x-1]    
    
    arr0=np.array(arr0,dtype=np.int32)
    arr1=np.array(arr1,dtype=np.int32)
    arr2=np.array(arr2,dtype=np.int32)  
    index0=np.array([len(arr0),len(list0)-x],dtype=np.int32)
    index1=np.array(index1,dtype=np.int32)
    index2=np.zeros_like(index1) 
    
    #print (key0,arr0,index0) 
    intersection = mod.get_function("intersection")
    intersection( drv.Out(arr2), drv.In(arr0), drv.In(arr1),
                  drv.Out(index2), drv.In(index0), drv.In(index1),
                    block=(ThreadNum,1,1), grid=(BlockNum,1)  
    )
    
        
   
    del arr1
    del index1
    del arr0
    for i in range(x,len(list0)):
        #print (list0[i])
        set2=list (arr2[((i-x)*index0[0]):(index2[i-x])])
        
        if len(set2)>=MinSupport:
           #print(key0,',',list0[i],end='')
           if type(key0)==int: 
               key1=[key0]
           else:
               key1=list(key0)
           key1.append(list0[i])
           #if len(key1)>1:
           #    continue
           key1=tuple(key1)
           dict_new[key1]=len(set2)
           #print (key1,': ',set0 & set1)
           eclat(dict,i+1,key1,set2, MinSupport,dict_new,list0,Arr1,Index1)
  

 
# output L1 item
def output1(dict,f):
    list0=sorted(dict.keys())
    for i in range(len(list0)):
        key=list0[i]
        if len(dict[key])<MinSupport:
            dict.pop(key)
        else:
            print (key ,end=' ',file=f)
            print ("(",end='',file=f)
            print (len(dict[key]),end='',file=f)
            print (")",file=f)
    return sorted(dict.keys())


#output Lk itemset
def outputFile(dict2,f):
    for i in sorted(dict2.keys(),key=functools.cmp_to_key(cmp_1)):
    #for i in dict2.keys():
        for j in i:
            print (j,end=' ',file=f)
        print ("(",end='',file=f) 
        print (dict2[i],end='',file=f)
        print (")",file=f)
   


def printf(format, *args):
    sys.stdout.write(format % args)

if  __name__=='__main__':
    start = timeit.default_timer()
    dict={}
    f = open(sys.argv[3],"w" )
    MinSupport=parse(dict)  
    list0=output1(dict,f)
    dict2={}
    
    arr1=[]
    index1=[]
    ind1=0
    
    for i in range(0,len(list0)):

        ind1=ind1+ len(dict[list0[i]])
        index1.append(ind1 )
        arr1=arr1+sorted(dict[list0[i]])
    arr1=np.array(arr1,dtype=np.int32)
    index1=np.array(index1,dtype=np.int32)
    
    #print (arr1,index1)
    #stop = timeit.default_timer()
    #printf("run time: %.2f s\n",stop-start)
  

    for i in range(len(list0)):
        key=list0[i]
        
        eclat(dict,i+1,key,dict[key],MinSupport,dict2,list0,arr1,index1)

    outputFile(dict2,f)   
    f.close()
    del dict
    del dict2
    stop = timeit.default_timer()
    printf("run time: %.2f s\n",stop-start) 
     
     


