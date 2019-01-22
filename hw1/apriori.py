#######################
# hw1 apriori        ##
# Yo-Chi Lee         ##
# r06921048          ##
#######################

import sys
import os
import timeit

# parse the input
def parse(dict,arr):
    f = open(sys.argv[1],"r" )
    lines = f.readlines()
    for i in range(0,len(lines)): 

        numberset = set()  
        for word in lines[i].split():
            word=int(word)           
            if dict.get(word)==None: 
    	        dict[word]=1
            else:
                dict[word]=dict[word]+1		 	
            numberset.add(word);
        arr.append(numberset)    
    f.close()
    return len(lines)*float(sys.argv[2])
# select the frequent itemset for L1
def chooseWord(dict,MinSupport ):
    list=[]
    list1=[]
    for i in sorted(dict.keys()):
        set0=set()
        value=dict[i]
        if value>=MinSupport:
            set0.add(i)
            list.append(set0)
            list1.append(value)
    return (list,list1) 
# select the frequent itemset for L2~Lk
def chooseArrWord( itemlist,arr,MinSupport ):
    list=[]
    list1=[]
    for i in sorted(itemlist):
        count=0
        for j in arr:
            if i<=j:
                count=count+1
        
        if count>=MinSupport:
            #print (i,'\n')           
            list.append(i)
            list1.append(count)
    return (list,list1)
# find Lk itemset by Lk-1 itemset
def newItemset(newlist,list,number,x=0,set0=set(),counter=0,newset=set()):
    for i in range(x,len(list)):
        if len(set0)==0:
            set0=list[i]
            for j in range (i+1,len(list)):
                if len(set0 & list[j])>=(number-2):
                    set1=set()                   
                    if (number>2):
                        set1.add(tuple(sorted(set0|list[j])))
                        if newset>=set1:
                            continue            
                        newItemset(newlist,list,number,j+1,(set0|list[j]),2,newset)
                    else :
                        newlist.append( set0|list[j])
                        newset.add(tuple(sorted(set0|list[j]))) 
        elif (set0>list[i])==False:
            continue 
        elif counter+1<number:
            newItemset(newlist,list,number,i+1,(set0|list[i]),counter+1,newset)
            return
        else :
            newlist.append( set0|list[i])
            newset.add(tuple(sorted(set0|list[i]))) 
            return
        set0=set() 
# output itemset to file
def outputFile(finallist,countlist,f):
    for it in range (0,len(finallist)):
        sortlist=sorted(finallist[it])
        for i in range(len(sortlist)):
            print (sortlist[i],end=' ',file=f)
        print ("(",end='',file=f)
        print (countlist[it],end='',file=f)
        print (")",file=f)

def printf(format, *args):
    sys.stdout.write(format % args)

if __name__ =='__main__':
    start = timeit.default_timer()
    dict={}
    arr=[]    
    MinSupport=parse(dict,arr)
    f = open(sys.argv[3],"w" )   
    #print (MinSupport,"\n")
    (itemset,countlist)=chooseWord(dict,MinSupport)
    outputFile(itemset,countlist,f)
    finallist=[]
    countlist=[]
    it=2
    while True: 
        newlist=[]  
        newItemset(newlist,itemset,it) 
        (newlist,countlist0)=chooseArrWord( newlist,arr,MinSupport )
        #print (newlist)
        if len(newlist)>0:
            finallist=newlist 
            countlist=countlist0
            outputFile(finallist,countlist,f)
            it=it+1
        else:
            break
        itemset=newlist   
    #print (finallist,'\n',countlist,'\n')
    f.close()
    stop = timeit.default_timer()
    printf("run time: %.2f s\n",stop-start)  
