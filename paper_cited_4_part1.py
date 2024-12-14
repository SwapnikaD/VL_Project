from itertools import combinations 
from sentence_transformers import SentenceTransformer 
from sklearn.metrics.pairwise import cosine_similarity 
import numpy as np 
import utils
def solve_puzzle_with_mpnet(words): 
    model = SentenceTransformer('all-mpnet-base-v2') 
    word_embeddings = model.encode(words) 
    all_groups = list(combinations(words, 4)) 
    group_scores = [] 
    for group in all_groups: 
        group_indices = [words.index(word) for word in group] 
        group_embeddings = [word_embeddings[idx] for idx in group_indices] 
        similarity_matrix = cosine_similarity(group_embeddings) 
        pairwise_similarities = similarity_matrix[np.triu_indices(4, k=1)]  # Upper triangle excluding diagonal 
        avg_similarity = np.mean(pairwise_similarities) 
        group_scores.append((group, avg_similarity)) 
    sorted_groups = sorted(group_scores, key=lambda x: x[1], reverse=True) 
    remaining_words = set(words) 
    guessed_groups = [] 
    for group, _ in sorted_groups: 
        if set(group).issubset(remaining_words): 
            guessed_groups.append(group) 
            remaining_words -= set(group)  # Remove guessed words 
            if len(remaining_words) < 4: 
                break 
    return guessed_groups 
words = [ 
    "apple", "orange", "banana", "grape", 
    "cat", "dog", "rabbit", "horse", 
    "red", "blue", "green", "yellow", 
    "car", "train", "plane", "boat" 
] 
groups_semantic_data={}
i=0
with open('txt files\parsedCleanedLLM.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # if i<2:
            puzz = line.strip()
            # print(puzz)
            words = puzz.split(", ")
            result = solve_puzzle_with_mpnet(words)
            # print("Guessed Groups:") 
            groups=[]
            for group in result: 
                # print(group) 
                output = ", ".join(group)
                # print(output)
                groups.append(output)
            key="set"+str(i)
            groups_semantic_data[key]=groups
            i+=1
    print(i)
utils.save_entry_to_json(groups_semantic_data,"data/paper1.json")