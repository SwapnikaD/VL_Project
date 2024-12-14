import json
import wikidata as wiki
file_path = "data/gold_data.json"

# Parse the JSON content
with open(file_path,'r') as file:
    data = json.load(file)


print(data[0]['allwords'])
# trying only for first record
conn_16 = data[0]['allwords'].split(", ")
print(conn_16)

word_conns = {}
for word in conn_16:    
    tupl = wiki.getData(word.capitalize())
    word_conns[word] = tupl


print(word_conns)
