
import os
import replicate
os.environ["REPLICATE_API_TOKEN"] = "r8_ERNFr0nbIkR1BT9D8HqRy4uMsDoULi31mx11p"


def getData(keyword):

    user_input = f"You are a knowledge engine, Generate a list of triplets where each triplet consists of three words in the following format [Given word, relation, related word]. Here are some examples for Barack Obama:[Barack Obama, was, President], [Barack Obama, isa, political leader], [Barack Obama, had, many accomplishments ],   Please generate 10 such triplets for the given word {keyword}"
    prompt = f"### User:{user_input} ### Knowledge engine:"

    # Generate LLM response
    output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', # LLM model
                            input={"prompt": f"{prompt}", # Prompts
                            "temperature":0.1, "top_p":0.9, "max_length":500, "repetition_penalty":1})  # Model parameters

    full_response = ""

    for item in output:
        full_response += item

    print(full_response)
    return full_response