import torch 
from PIL import Image 
from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize 
from transformers import CLIPProcessor, CLIPModel 
import numpy as np 
from scipy.spatial.distance import cdist 
import os 
import utils as utils

device = torch.device("cuda" if torch.cuda.is_available() else "cpu") 
print(f"Using device: {device}") 
 
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device) 
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32") 

def preprocess_image(image_paths): 
    transform = Compose([ 
        Resize((224, 224)), 
        CenterCrop(224), 
        ToTensor(), 
        Normalize(mean=(0.48145466, 0.4578275, 0.40821073), std=(0.26862954, 0.26130258, 0.27577711)) 
    ]) 
    images = [transform(Image.open(path).convert("RGB")) for path in image_paths] 
    return torch.stack(images) 

def get_image_embeddings(image_paths): 
    images = preprocess_image(image_paths).to(device)  # Move images to GPU 
    with torch.no_grad(): 
        image_features = model.get_image_features(images) 
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)  # Normalize embeddings 
    return image_features 

def enforce_equal_clusters(image_embeddings, image_paths, num_clusters=4): 
    from sklearn.cluster import KMeans 
    kmeans = KMeans(n_clusters=num_clusters, random_state=42) 
    cluster_centers = kmeans.fit(image_embeddings.cpu().numpy()).cluster_centers_ 
    distances = cdist(image_embeddings.cpu().numpy(), cluster_centers, metric='euclidean') 

    clusters = [[] for _ in range(num_clusters)] 
    used_indices = set() 

    for _ in range(len(image_paths)): 
        for cluster_id in range(num_clusters): 
            for idx in np.argsort(distances[:, cluster_id]): 
                if idx not in used_indices: 
                    clusters[cluster_id].append(idx) 
                    used_indices.add(idx) 
                    break 

    for cluster_id in range(num_clusters): 
        while len(clusters[cluster_id]) > len(image_paths) // num_clusters: 
            extra_idx = clusters[cluster_id].pop() 
            used_indices.remove(extra_idx) 

    grouped_images = {i: [image_paths[idx] for idx in clusters[i]] for i in range(num_clusters)} 
    return grouped_images 

all_data_dict = {}
image_dir = "images_sd"
# i=0
for i,folder in enumerate(os.listdir(image_dir)):
    # if i <2:
        print(f"fodler: {folder}")
        
        folder_path = os.path.join(image_dir, folder)
        image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".png")] 
        image_embeddings = get_image_embeddings(image_paths) 
        grouped_images = enforce_equal_clusters(image_embeddings, image_paths, num_clusters=4) 

        groups=[]
        for group_id, images in grouped_images.items(): 
            print(f"Group {group_id + 1}: {images}") 
            image_names = [os.path.splitext(os.path.basename(path))[0].lower() for path in images]
            output = ", ".join(image_names)
            print(image_names)
            print(output)
            groups.append(output)
        all_data_dict[folder]=groups
print(all_data_dict)
utils.save_entry_to_json(all_data_dict,"clip_similarities.json")

 