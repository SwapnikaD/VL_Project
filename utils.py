import json
import re

def save_entry_to_json(entry,file_name): 

    try: 
        with open(file_name, 'r') as file: 
                data = json.load(file) 
         
        # Append the new entry 
        data.append(entry) 
         
        # Save back to the file 
        with open(file_name, 'w') as file: 
            json.dump(data, file, indent=4) 
        print(f"Successfully saved entry: {entry}") 
     
    except Exception as e: 
        print(f"Error saving entry to JSON: {e}") 


def cleanstring(input_string: str, key: str) -> str:

    # Replace ',', '-', and '' with a space
    cleaned = re.sub(r"[,_-]", " ", input_string)
    cleaned = re.sub(re.escape(key), "", cleaned, count=1,flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned

def process_json_file(from_file,to_file) -> dict:
    # Load the JSON data
    ret_list = []
    with open(from_file, 'r') as file:
    # with open('data_sample_for_process_test.json', 'r') as file:
        data_json = json.load(file)

    # Process each string in the arrays
    for data in data_json:
        for outer_key, inner_dict in data.items():
            for inner_key, string_list in inner_dict.items():
                data[outer_key][inner_key] = list(set(cleanstring(s, inner_key) for s in string_list))
            ret_list.append(data)
    print(ret_list)
 
    # with open("test.json", 'w') as file:
    with open(to_file, 'w') as file:
        json.dump(ret_list,file, indent=4)
    # json.dumps(processed_data, "processed_triples_data_dicts_triplets_llama3-new-237.json",indent=4)        



def process_llama_result(entry): 
    category_pattern = r"Category\d+: \[(.*?)\]" 
    categories = re.findall(category_pattern, entry) 
    response = entry.replace("\n"," ")
    data = { 
        "groups": categories, 
        "response": response 
    } 
    return data

def clean_data():
    file_path = "data/gold_data.json"

    # Read data from file.
    with open(file_path,'r') as file:
        data = json.load(file)
        print(data)
        i=0
        for record in data:
            # if i<2:
                result = [", ".join(value) for value in record["categories"].values()]
                print(result)
                key="set"+str(i)
                save_entry_to_json({key:result},"data/gold_data_polished.json")
                i+=1




def filling_empty_sets_in_answers_sent_by_llama():
        try: 
            with open('data/my_llama_answers_all.json', 'r') as file: 
                all_data = json.load(file)  # Assuming the file is in JSON format 
            # print(len(all_data))
            # print(all_data[1])
            for record in all_data:
                # print(record)
                # print("........")
                for idx, data in record.items():
                    
                    # Check if 'groups' is an empty list 
                    if len(data.get('groups'))==0: 
                        response_text = data.get('response', '') 
                        if response_text: 
                            grouped_strings=[]
                            print(idx)
                            capital_words = re.findall(r'\b[A-Z]+\b', response_text) 
                            if "I" in capital_words:
                                capital_words.remove("I")
                            if "NYT" in capital_words:
                                capital_words.remove("NYT")
                            print(capital_words)
                            if len(capital_words) % 4 == 0:
                                grouped_strings = [", ".join(capital_words[i:i + 4]) for i in range(0, len(capital_words), 4)]
                                print(grouped_strings)
                        
        except json.JSONDecodeError: 
            return "Invalid JSON format." 

def convert_json_structure(): 
    # with open('llama_answers_all.json', 'r') as file: 
    with open('data/test.json', 'r') as file: 
        all_data = json.load(file)
    output_json = {} 
    for record in all_data:
        # print(record)
        # print("........")
        for idx, data in record.items():
            
            # Check if 'groups' is an empty list 
            if len(data.get('groups'))!=0: 
                group_str = data.get('groups') # Convert to lowercase to match the left-side format 
                output_json[idx]=group_str
            
    print(output_json)
    save_entry_to_json(output_json,"data/processed_llama_answers.json")


filling_empty_sets_in_answers_sent_by_llama()
