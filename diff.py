from diffusers import StableDiffusionPipeline 

import torch 
import os
 

def generate_image_from_word(array,foldername): 
    model_id = "CompVis/stable-diffusion-v1-4" 
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16) 
    pipe = pipe.to("cuda")  # Use GPU for faster generation 
    os.mkdir("images_sd/"+foldername)
    for word in array:
        # Define the prompt 
        prompt = f"An image representing {word}, highly detailed" 
        # Generate the image 
        image = pipe(prompt).images[0] 
        # Save the image 
        output_file="images_sd/"+foldername+"/"+word+".png"
        image.save(output_file) 
        print(f"Image saved as {output_file}") 

 
