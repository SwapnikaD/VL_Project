import json
# import api as api
# import groq_test as api
# import google_search_image as gsi
import time
import wikidata as api
# import diff as diff
file_path = "data/gold_data.json"

# Read data from file.
with open(file_path,'r') as file:
    data = json.load(file)
# # .............
# puzzle = data[0]['allwords']
# print(data[0]['allwords'])
# # Read the puzzlw string having 16 words.
# # trying only for first record
# conn_16 = data[0]['allwords'].split(", ")
# print(conn_16)

# # from llama model's API via getting triplets for each word
# word_conns = {}
# for word in conn_16:    
#     tupl = api.getData(word)
#     word_conns[word] = tupl

# word_conns = api.extract_valid_data(word_conns)
# print(word_conns)
# key="set"+str(0)
# api.save_entry_to_json({key:word_conns})


# puzzle = data[1]['allwords']
# print(data[1]['allwords'])
# # Read the puzzlw string having 16 words.
# # trying only for first record
# conn_16 = data[1]['allwords'].split(", ")
# print(conn_16)

# # from llama model's API via getting triplets for each word
# word_conns = {}
# for word in conn_16:    
#     tupl = api.getData(word)
#     word_conns[word] = tupl

# word_conns = api.extract_valid_data(word_conns)
# print(word_conns)
# key="set"+str(1)
# api.save_entry_to_json({key:word_conns})




# ...............
for i,puzz in enumerate(data):
    if i >303:
        puzzle = data[i]['allwords']
        print(data[i]['allwords'])
        # Read the puzzlw string having 16 words.
        # trying only for first record
        conn_16 = data[i]['allwords'].split(", ")
        print(conn_16)

        # from llama model's API via getting triplets for each word
        word_conns = {}
        for word in conn_16:    
            tupl = api.getData(word.capitalize())
            word_conns[word] = tupl

        print(word_conns)
        key="set"+str(i)
        api.save_entry_to_json({key:word_conns})


