import json
import time
import wikidata as api
file_path = "data/gold_data.json"

with open(file_path,'r') as file:
    data = json.load(file)

for i,puzz in enumerate(data):
    if i >303:
        puzzle = data[i]['allwords']
        print(data[i]['allwords'])
        # Read the puzzlw string having 16 words.
        # trying only for first record
        conn_16 = data[i]['allwords'].split(", ")
        print(conn_16)

        word_conns = {}
        for word in conn_16:    
            tupl = api.getData(word.capitalize())
            word_conns[word] = tupl

        print(word_conns)
        key="set"+str(i)
        api.save_entry_to_json({key:word_conns})


