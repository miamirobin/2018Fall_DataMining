import pandas as pd
# https://github.com/SohierDane/BigQuery_Helper
from bq_helper import BigQueryHelper

bq_assistant = BigQueryHelper("bigquery-public-data", "github_repos")

QUERY = """
        SELECT *
        FROM `bigquery-public-data.github_repos.languages`
        """
df = bq_assistant.query_to_pandas_safe(QUERY)

def proc_language(row):
    return list(map(lambda x: x['name'], row['language']))

df['language'] = df.apply(proc_language,axis=1)

df.to_csv('language_proccessed.csv')

from ast import literal_eval

count = {}
byte_count = {}
def stats(row):
    global count
    global byte_count
    for lang in literal_eval(row['language']):
        name = lang['name']
        if name not in count:
            count[name] = 0
            byte_count[name] = 0
        count[name] += 1
        byte_count[name] += lang['bytes']

df.apply(stats, axis=1)

print(count)

# print
for x, y in sorted(list(byte_count.items()), key=lambda x:x[1], reverse=True):
    print(y)
