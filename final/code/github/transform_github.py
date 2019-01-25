from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer
import sys
import csv
import numpy as np
#a = "c++"
#print(a.replace("+","plus"))
'''
def stem_input(target):
  stemmer = SnowballStemmer("english")
  a=set()
  for i in range(len(target)):
    line = target[i]
    if i<5:
        print (line)
    line = line.replace("+","plus")
    line = line.replace("#","sharp")
    
    tokens = line.split()
    new_line = ""
    for token in tokens:
     
      token = (token.strip(',()/'))
      new_line += (" " + stemmer.stem(token))
    target[i] = new_line.strip()
   return target
'''
def find_keyword(keyword,target):
    word=[]
    for i in range(1,len(target)):
        word_row=set()
        for j in range(2,len(target[i])):
            #print (target[109][5])
            column = target[i][j]        
            #column = column.replace('C','CCC')
            #column = column.replace('R','RRR')
            #column = column.replace('#','sharp')
            column = column.lower()
                        
            for k in keyword:
                if column.find(k.lower())!=-1:
                    word_row.add(k.lower())     
        if len(word_row)>0:
            word.append(sorted(word_row))
    return word            
'''
if len(sys.argv) < 3:
  print ("Usage: python3 %s <input_file> <output_file>" % sys.argv[0])
  exit(0)
'''

input_path = sys.argv[1]
input_path2= sys.argv[2]
output_path = sys.argv[3]



keyword=np.genfromtxt(input_path2,delimiter='\n',dtype=str,comments=None)

with open (input_path, 'r') as csvfile:
    iterator = csv.reader(csvfile, delimiter = ',')
    data = [data for data in iterator]
#input_data = np.asarray(data)

# content  stemming
#job_title = stem_input(input_data[:,1])
#job_categ = stem_input(input_data[:,2])
#job_locat,a = stem_input(input_data[:,3])
#job_descr = stem_input(input_data[:,4])
#job_miniq = stem_input(input_data[:,5])
#job_prefq = stem_input(input_data[:,6])

#word=find_keyword(keyword,input_data)
word=find_keyword(keyword,data)

f = open(output_path,"w" )
for i in range (len(word) ):
    for j in range(len(word[i])):
        if j<len(word[i])-1:
            print (word[i][j],file=f,end=',')
        else:
            print (word[i][j],file=f,end='\n')
f.close()
