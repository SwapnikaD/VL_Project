from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
import torch
import re

def getData(keyword):
    # Define the model name and the authentication token required to access the LLaMA-2 model from Hugging Face.
    name = "meta-llama/Llama-2-7b-chat-hf"
    auth_token = "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"

    # Load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(name, cache_dir='./model/', token=auth_token, use_fast=True)

    # Check if a GPU is available and set the device accordingly
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    # Load the LLaMA-2 model using the previously defined name and authentication token. We'll also set some model parameters.
    model = AutoModelForCausalLM.from_pretrained(
        name, 
        cache_dir='./model/', 
        token=auth_token, 
        torch_dtype=torch_dtype,
    )

    # Setup a Prompt: We'll create a prompt that we want to query the model with. Testing preprompted model for NPL.

    user_input = f"Generate a list of triplets where each triplet consists of three words in the following format [Given word, relation, related word]. Here are some examples for African-American:[African-American, isa, race], [African-American, is subset of, Americans], [African-American, culturally, rich ],   Please generate 50 such triplets for the given word {keyword}"
    prompt = f"### User:{user_input} ### Assistant:"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # Generate Text: Now we'll run the model to generate text based on the input prompt.
    with torch.no_grad(): 
        streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
        output = model.generate(**inputs, streamer=streamer, use_cache=True, max_new_tokens=500, early_stopping=False)

    output_text = tokenizer.decode(output[0], skip_special_tokens=True)
    print(output_text)
    response = output_text.split("### Assistant:")[1]
    items = re.findall(r'\d+\.\s*([^\d]+)', response)
    triples = []
    i=1
    # list_of_all_triples=[]
    for item in items:
        triple = item.split(",")
        if len(triple)>1:
            triples.append([triple[0].strip()+str(i),triple[1].strip(), triple[2].strip()])
            i+=1
        
        # list_of_all_triples.extend(triples)



    # Now 'triples' contains the full result 
    print(triples)
    return tuple(triples)

# getData("Barack Obama")