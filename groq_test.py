from groq import Groq
import os
import re


def extract_valid_data(input_dict): 
    result = {} 
    # Regular expression to match square brackets with clean content 
    pattern = r'\[([a-zA-Z0-9\s,]+)\]' 
    for key, value in input_dict.items(): 
        matches = re.findall(pattern, value) 
        clean_matches = [match.strip() for match in matches if match] 
        result[key] = clean_matches  
    return result 

def getData(keyword):
    client = Groq()

    # user_input = f"You are a knowledge engine, Generate a list of triplets where each triplet consists of three words in the following format [Given word, relation, related word]. Here are some examples for Barack Obama:[Barack Obama, was, President], [Barack Obama, isa, political leader], [Barack Obama, had, many accomplishments ],   Please generate 10 such triplets for the given word {keyword}"
    # prompt = f"### User:{user_input} ### Knowledge engine:"

    

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": f"You are a knowledge engine, Generate a list of triplets where each triplet consists of three words in the following format [Given word, relation, related word]. Here are some examples for Barack Obama:[Barack Obama, was, President], [Barack Obama, isa, political leader], [Barack Obama, had, many accomplishments ]. Please generate 10 such triplets for the given word {keyword}"
            },
            {
                "role": "assistant",
                "content": f"Here are 10 triplets for the given word {keyword}"
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    # print("...........")
    # print(completion)
    # print("...........")
    return_val = ""

    for chunk in completion:
        if chunk.choices[0].delta.content:
            if chunk.choices[0].delta.content != '\n':
                return_val+= chunk.choices[0].delta.content
        else:
            return_val+= ""

    # return_val = extract_valid_text(return_val)
    print(return_val)
    return return_val

