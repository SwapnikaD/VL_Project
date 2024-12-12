from sklearn.metrics.pairwise import cosine_similarity 
from sklearn.cluster import KMeans 
from sentence_transformers import SentenceTransformer 
import numpy as np 
from collections import defaultdict 
import json
import utils

data = {'APPROVAL': ['synonym acceptance', 'antonym disapproval', 'has positive connotation', 'indicates agreement', 'related to emotion', 'has suffix able', 'has suffix ment', 'is a type of consent', 'shows approval rating', 'is a kind of agreement'],  
                  'BLESSING': ['isa noun', 'has no color', 'indicates favor', 'related to god', 'has prefix bi', 'used in Christian', 'has suffix ing', 'has positive connotation', 'has no sound', 'derived from bless'],  
                  'CONSENT': ['synonym agreement', 'antonym refusal', 'isa verb', 'used in law', 'has positive connotation', 'indicates willingness', 'related to permission', 'has suffix ment', 'involves personal choice', 'considered ethical'], 
                  'SUPPORT': ['synonym assistance', 'antonym disapproval', 'isa verb', 'used in social sciences', 'has positive connotation', 'indicates backing', 'related to encouragement', 'has suffix ing', 'has prefix re', 'has concrete substance'], 
                  'BAGEL': ['related to food', 'isa pastry', 'has circular shape', 'has chewy texture', 'indicates hungover', 'has prefix bag', 'baked bread', 'related to breakfast', 'associated with Judaism', 'stuffed with cream cheese'],  
                  'LIFESAVER': ['has prefix', 'is a noun', 'has suffix er', 'related to aid', 'has life', 'used in emergency', 'indicates bravery', 'is title', 'has positive connotation', 'is a savior'],  
                  'TIRE': ['is a vehicle part', 'has round shape', 'is used in car', 'has durable material', 'has prefix tri', 'has suffix less', 'related to road', 'has rubber composition', 'indicates fatigue', 'has antonym energy'],  
                  'WREATH': ['is a decoration', 'used in Christmas', 'related to flower', 'indicates festivities', 'has no plurality', 'is a arrangement', 'related to garland', 'used in wedding', 'is a accessory', 'has three dimensions'],  
                  'HOOK': ['synonym lasso', 'isa fishing tool', 'related to fish', 'has three dimensional', 'used in karaoke', 'indicates catch', 'related to music', 'is type of fastener', 'has sounds like crook', 'makes secure'],  
                  'SHANK': ['synonym shorn', 'antonym intact', 'isa body part', 'used in golf', 'has sharp edge', 'indicates wood grain orientation', 'related to leg', 'has suffix ed', 'has meaty part of leg'],  
                  'SLICE': ['synonym cut', 'antonym whole', 'isa verb', 'used in food', 'has sharp edge', 'indicates precision', 'related to knife', 'has prefix sharp', 'has specific portion', 'used by chef'],  
                  'WHIFF': ['synonym scent', 'antonym full', 'isa noun', 'used in perfume', 'indicates detection', 'related to smell', 'has prefix whil', 'has suffix ed', 'has small amount', 'part of breath'],  
                  'LOAF': ['synonym bread', 'has slice', 'made from wheat', 'shaped like rectangle', 'has leavening agents', 'taste like savory', 'baked in oven', 'related to kitchen', 'has prefix un', 'related to rising', 'has carbohydrates'],  
                  'SLIP': ['synonym slide', 'antonym grip', 'isa verb', 'used in sports', 'indicates accident', 'has no color', 'related to fall', 'has suffix ly', 'has noun', 'is often associated with danger'],  
                  'SNEAK': ['isa verb', 'has suffix ly', 'means secretly enter or leave', 'related to secretive behavior', 'has negative connotation', 'indicates covert action', 'has prefix sne', 'used in idioms', 'related to stealth', 'used in sentences with a sense of concealment'],  
                  'WADE': ['has suffix ly', 'used in swimming', 'has prefix re']} 

# with open('test.json', 'r') as file: 
# with open('processed_triples_data_dicts_triplets_llama3-new-237.json', 'r') as file: 
# with open('triples_input_sim.json', 'r') as file: 
with open('cleaned_wiki.json', 'r') as file: 
    groups_semantic_data={}
    data_all = json.load(file) 
    # o=0
    for o,puzzle in enumerate(data_all):
        # print(puzzle)
        # print("..............")
        # if (o<238):
            for setn,data in puzzle.items():
                # print(setn,data)

            

                keys = list(data.keys()) 
                flat_data = [] 
                key_value_map = defaultdict(list) 

                for key, values in data.items(): 
                    for value in values: 
                        flat_data.append(value) 
                        key_value_map[key].append(len(flat_data) - 1) 
                # Generate embeddings 
                model = SentenceTransformer('all-MiniLM-L6-v2') 
                embeddings = model.encode(flat_data) 

                #Compute average pairwise similarity matrix 
                n_keys = len(keys) 
                # print(n_keys)
                key_similarity_matrix = np.zeros((n_keys, n_keys)) 

                for i, key1 in enumerate(keys): 
                    for j, key2 in enumerate(keys): 
                        if i != j: 
                            indices1 = key_value_map[key1] 
                            indices2 = key_value_map[key2] 
                            embeddings1 = embeddings[indices1] 
                            embeddings2 = embeddings[indices2] 
                            similarity = cosine_similarity(embeddings1, embeddings2).mean() 
                            key_similarity_matrix[i, j] = similarity 


                #KMeans clustering into 4 groups 
                kmeans = KMeans(n_clusters=4, random_state=42) 
                clusters = kmeans.fit_predict(key_similarity_matrix) 
                #Enforce unique, balanced groups 
                grouped_keys = defaultdict(list) 
                for key_index, cluster_id in enumerate(clusters): 
                    grouped_keys[cluster_id].append(keys[key_index]) 
                #Adjust to ensure exactly 4 unique keys per group 
                # Flatten all groups into a single list 
                all_keys = [key for group in grouped_keys.values() for key in group] 
                #Ensure no repetition and balance the groups 
                final_groups = [all_keys[i:i + 4] for i in range(0, len(all_keys), 4)] 
                groups=[]
                # Output the groups 
                for i, group in enumerate(final_groups, 1): 
                    # print(f"Group {i}: {', '.join(group)}") 
                    output = ", ".join(group)
                    # print(output)
                    groups.append(output)
                groups_semantic_data[setn]=groups
        # print(groups_semantic_data)
                
                print(o)
utils.save_entry_to_json(groups_semantic_data,"sem_sim_wiki.json")