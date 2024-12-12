import json
# import api as api
# import groq_test as api
# import google_search_image as gsi
# import time
import diff as diff
file_path = "data/gold_data.json"

# Read data from file.
with open(file_path,'r') as file:
    data = json.load(file)


for i,puzz in enumerate(data):
    puzzle = data[i]['allwords']
    print(data[i]['allwords'])
    # Read the puzzlw string having 16 words.
    # trying only for first record
    conn_16 = data[i]['allwords'].split(", ")
    print(conn_16)

    # from llama model's API via getting triplets for each word
    # word_conns = {}
    # for word in conn_16:    
    #     tupl = api.getData(word)
    #     word_conns[word] = tupl

    # word_conns = api.extract_valid_data(word_conns)
    # print(word_conns)

    # getting images for each word using google images API
    # gsi.fetch_images(conn_16,"set"+str(i)+"/")
    # time.sleep(5)
    diff.generate_image_from_word(conn_16,"set"+str(i)+"/")
# 