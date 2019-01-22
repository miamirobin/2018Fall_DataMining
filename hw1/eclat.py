#######################
# hw1 eclat          ##
# Yo-Chi Lee         ##
# r06921048          ##
#######################

import sys
import os
import timeit
import functools

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
def eclat(dict,x,key0,set0,MinSupport,dict_new):
    
    list0=sorted(dict.keys())
    
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
           eclat(dict,i+1,key1,set2, MinSupport,dict_new)
  

 
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
    for i in range(len(list0)):
        key=list0[i]
        eclat(dict,i+1,key,dict[key],MinSupport,dict2)

    outputFile(dict2,f)   
    f.close()
    del dict
    del dict2
    stop = timeit.default_timer()
    printf("run time: %.2f s\n",stop-start) 
     
     


