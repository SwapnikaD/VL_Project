from groq import Groq
import os
import re
import json 


def extract_valid_data(input_dict): 
    with open('data_dump_llama3.txt', 'a',encoding='utf-8') as file:
        # Write the text to the file
        file.write(str(input_dict))
        file.write("\n")
    # print(input_dict)
    result = {} 
    # Regular expression to match square brackets with clean content 
    pattern = r'\[([a-zA-Z0-9_\s,-]+)\]' 
    for key, value in input_dict.items(): 
        matches = re.findall(pattern, value) 
        clean_matches = [match.strip() for match in matches if match] 
        result[key] = clean_matches  
        if len(clean_matches)==0:
            result[key] = ["|added|"+value]

    return result 

# input_dict= {'CHIME': ':\n\n1. [Chime, syno- nym, clang]\n2. [Chime, has suffix, e]\n3. [Chime, related _ to, bell]\n4. [Chime, has, sound]\n5. [Chime, indicates, attention]\n6. [Chime, has, musical]\n7. [Chime, used_in, clock]\n8. [Chime, has, harmonious]\n9. [Chime, is a type of, sound effect]\n10. [Chime, antonym, silence]\n\nNote that these triplets are not exhaustive, and there may be other valid relationships and related words for the word CHIME.'}

# rex = extract_valid_data(input_dict)
# print(".........")
# print(rex)
def save_entry_to_json(entry): 

    try: 
        with open("data_dicts_triplets_llama3.json", 'r') as file: 
                data = json.load(file) 
         
        # Append the new entry 
        data.append(entry) 
         
        # Save back to the file 
        with open("data_dicts_triplets_llama3.json", 'w') as file: 
            json.dump(data, file, indent=4) 
        print(f"Successfully saved entry: {entry}") 
     
    except Exception as e: 
        print(f"Error saving entry to JSON: {e}") 


def getData(keyword):
    client = Groq()

    # user_input = f"You are a knowledge engine, Generate a list of triplets where each triplet consists of three words in the following format [Given word, relation, related word]. Here are some examples for Like:[like, synonym, similar], [like, antonym, dislike], [like, isa, verb], [like, used_in, social media], [like, has, positive connotation], [like, indicates, preference], [like, related_to, emotion], [like, has suffix, ly], [like, has prefix, un], [like, has, no color]. Please generate 10 such triplets for the given word {keyword}"
    # prompt = f"### User:{user_input} ### Knowledge engine:"

    

    completion = client.chat.completions.create(
        model="llama-3.2-3b-preview",
        messages=[
            {
                "role": "user",
                "content": f"You are a knowledge engine, Generate a list of triplets where each triplet consists of three words in the following format [Given word, relation, related word]. Here are some examples for Like:[like, synonym, similar], [like, antonym, dislike], [like, isa, verb], [like, used_in, social media], [like, has, positive connotation], [like, indicates, preference], [like, related_to, emotion], [like, has suffix, ly], [like, has prefix, un], [like, has, no color]. Please generate 10 such triplets for the given word {keyword}"
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


def getAnswersForGame(Game):
    client = Groq()

    # user_input = f"You are a knowledge engine, Generate a list of triplets where each triplet consists of three words in the following format [Given word, relation, related word]. Here are some examples for Like:[like, synonym, similar], [like, antonym, dislike], [like, isa, verb], [like, used_in, social media], [like, has, positive connotation], [like, indicates, preference], [like, related_to, emotion], [like, has suffix, ly], [like, has prefix, un], [like, has, no color]. Please generate 10 such triplets for the given word {keyword}"
    # prompt = f"### User:{user_input} ### Knowledge engine:"

    

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": ("You are an expert knowledge engine. Solve today's NYT Connections game."
                            "Here are the instructions for how to play this game:"
                            "Find groups of four items that share something in common."
                            "Category Examples:"
                            "FISH: Bass, Flounder, Salmon, Trout"
                            "FIRE ___: Ant, Drill, Island, Opal"
                            "Categories will always be more specific than '5-LETTER-WORDS', 'NAMES' or 'VERBS.'"
                            "Example 1:"
                            "Words: ['DART', 'HEM', 'PLEAT', 'SEAM', 'CAN', 'CURE', 'DRY', 'FREEZE', 'BITE', 'EDGE', 'PUNCH', 'SPICE', 'CONDO', 'HAW', 'HERO', 'LOO']"
                            "Groupings:"
                            "Things to sew: ['DART', 'HEM', 'PLEAT', 'SEAM']"
                            "Ways to preserve food: [CAN', 'CURE', 'DRY', 'FREEZE']"
                            "Sharp quality: ['BITE', 'EDGE', 'PUNCH', 'SPICE']"
                            "Birds minus last letter: ['CONDO', 'HAW', 'HERO', 'LOO']"
                            "Example 2:"
                            "Words: ['COLLECTIVE', 'COMMON', 'JOINT', 'MUTUAL', 'CLEAR', 'DRAIN', 'EMPTY', 'FLUSH', 'CIGARETTE', 'PENCIL', 'TICKET', 'TOE', 'AMERICAN', 'FEVER', 'LUCID', 'PIPE']"
                            "Groupings:"
                            "Shared: ['COLLECTIVE', 'COMMON', 'JOINT', 'MUTUAL']"
                            "Rid of contents: ['CLEAR', 'DRAIN', 'EMPTY', 'FLUSH']"
                            "Associated with “stub”: ['CIGARETTE', 'PENCIL', 'TICKET', 'TOE']"
                            "____ Dream: [ 'AMERICAN', 'FEVER', 'LUCID', 'PIPE']"
                            "Example 3:"
                            "Words: ['HANGAR', 'RUNWAY', 'TARMAC', 'TERMINAL', 'ACTION', 'CLAIM', 'COMPLAINT', 'LAWSUIT', 'BEANBAG', 'CLUB', 'RING', 'TORCH', 'FOXGLOVE', 'GUMSHOE', 'TURNCOAT', 'WINDSOCK']"
                            "Groupings:"
                            "Parts of an airport: ['HANGAR', 'RUNWAY', 'TARMAC', 'TERMINAL']"
                            "Legal terms: ['ACTION', 'CLAIM', 'COMPLAINT', 'LAWSUIT']"
                            "Things a juggler juggles: ['BEANBAG', 'CLUB', 'RING', 'TORCH']"
                            "Words ending in clothing: ['FOXGLOVE', 'GUMSHOE', 'TURNCOAT', 'WINDSOCK']"
                            "Categories share commonalities:"
                            "- There are 4 categories of 4 words each"
                            "- Every word will be in only 1 category"
                            "- One word will never be in two categories"
                            "- There will never be a miscellaneous category"
                            "- As the category number increases, the connections between the words and their category become more obscure. Category 1 is the most easy and intuitive and Category 4 is the hardest"
                            "- There may be a red herrings (words that seems to belong together but actually are in separate categories)"
                            "- Category 4 often contains compound words with a common prefix or suffix word"
                            "- A few other common categories include word and letter patterns, pop culture clues (such as music and movie titles) and fill-in-the-blank phrases"
                            "To better play this game, think in form of triplets from a knowledge engine which generates its relation to the given word in terms of synonym, antonym, color, common suffix, prefix. This knowledge will help you better group these words"
                            "You will be given a new example(Example 4) with today's list of words.First explain your reason for each category and then give your final answer following the structure below (Replace Category1,2,3,4 with their names instead):"
                            "Groupings:"
                            "Category1: [word1, word2, word3, word4]"
                            "Category2: [word5, word6, word7, word8]"
                            "Category3: [word9, word10, word11, word12]"
                            "Category4: [word13, word14, word15, word16]"
                            "Remember that the same word cannot be repeated across multiple categories, and you need to output 4 categories with 4 distinct words each. Do not make up words not in the list. This is the most important rule. Please obey"
                            "Example 4:"
                           f"Words : [{Game}]"
                            "Groupings:")
            },
            {
                "role": "assistant",
                "content": "Here are the possible answers"
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

