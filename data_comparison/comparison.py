import json 
import re 
from collections import defaultdict 
def normalize_string(value): 
    words = value.split(",") 
    sorted_words = sorted(word.strip().lower() for word in words) 
    return ",".join(sorted_words) 
    

def compare_keys(base_file, comparison_file): 
    try: 
        with open(base_file, 'r') as f: 
            base_data = json.load(f) 
        with open(comparison_file, 'r') as f: 
            comparison_data = json.load(f) 
        key_matches = {} 
        for key, base_values in base_data.items(): 
            base_set = set( 
                normalize_string(value) for value in base_values 
            ) 
            comparison_values = comparison_data.get(key, []) 
            comparison_set = set( 
                normalize_string(value) for value in comparison_values 
            ) 
            matches = base_set.intersection(comparison_set) 
            key_matches[key] = len(matches) 
        return key_matches 
    except Exception as e: 
        print(f"Error: {e}") 
        return {} 
# Example usage 
base_file_path = 'gold_data_polished.json' 
comparison_file_path = 'processed_llama_answers.json' 
# Calculate matches key by key 
result = compare_keys(base_file_path, comparison_file_path) 
print(json.dumps(result, indent=4)) 

 