import groq_test as gr
import utils as utils
i = 0
with open('parsedCleanedLLM.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # if i<2:
            puzz = line.strip()
            print(puzz)
            ans = gr.getAnswersForGame(puzz)
            print(ans)
            data= utils.process_llama_result(ans)
            print(data)
            key="set"+str(i)
            utils.save_entry_to_json({key:data},"my_llama_answers_all.json")
            i+=1

print(i)