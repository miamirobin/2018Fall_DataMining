from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer
import sys
import csv
import numpy as np
a = "c++"
print(a.replace("+","plus"))

def stem_input(target):
  stemmer = SnowballStemmer("english")

  for i in range(len(target)):
    line = target[i]
    line = line.replace("+","plus")
    line = line.replace("#","sharp")
    tokens = line.split()
    new_line = ""
    for token in tokens:
      token = (token.strip(',()/'))
      new_line += (" " + stemmer.stem(token))
    target[i] = new_line.strip()
    #if i<5:
    #    print (target[i])
  return target

if len(sys.argv) < 3:
  print ("Usage: python3 %s <input_file> <output_file>" % sys.argv[0])
  exit(0)

input_path = sys.argv[1]
output_path = sys.argv[2]

with open (input_path, 'r') as csvfile:
  iterator = csv.reader(csvfile, delimiter = ',')
  data = [data for data in iterator]
input_data = np.asarray(data)



# content  stemming
job_title = stem_input(input_data[:,1])
job_categ = stem_input(input_data[:,2])
job_locat = stem_input(input_data[:,3])
job_descr = stem_input(input_data[:,4])
job_miniq = stem_input(input_data[:,5])
job_prefq = stem_input(input_data[:,6])


"""
with open('GGGG.csv', 'w') as f:
  for line in job_title:
    try:
      f.write(line + '\n')
    except UnicodeEncodeError:
      continue
"""


vec = TfidfVectorizer()
X = vec.fit_transform(job_prefq)

attri = vec.get_feature_names()

print ("Num of tfidf vec %d" % len(attri))


"""
encode_error_time = 0

for i in range(len(attri)):
  try:
    attri[i] = str(attri[i])
    #attri[i] = attri[i].encode("ascii")
  except UnicodeEncodeError:
    encode_error_time +=1
    continue
"""


i = 0

if True:
  with open(output_path, 'w') as f:
    for line in attri:
      try:
        f.write(line + '\n')
      except UnicodeEncodeError:
        continue
#print (input_data[:,4]).shape
