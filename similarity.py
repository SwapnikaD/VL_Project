import sentence_transformers
from sklearn.metrics.pairwise import cosine_similarity

model_name = 'all-mpnet-base-v2'
# model_name = 'all-MiniLM-L6-v2'

# Instantiate a SentenceTransformer model
model = sentence_transformers.SentenceTransformer(model_name)

sample_dict = {
       "fruits": ["apple", "banana", "cherry", "date", "fig", "grape", "honeydew", "kiwi", "lemon", "mango"], 
        "stone_fruits": ["peach", "plum", "pear", "apricot", "nectarine", "cherry", "date", "fig", "grape", "honeydew"], 
        "vehicles": ["car", "bike", "bus", "train", "plane", "boat", "helicopter", "ship", "ferry", "subway"], 
        "ai_technologies": ["neural network", "machine learning", "deep learning", "supervised", "unsupervised", "reinforcement", "classification", "regression", "clustering", "optimization"], 
        "statistics": ["mean", "median", "mode", "variance", "standard deviation", "distribution", "analysis", "hypothesis", "probability", "statistics"], 
        "programming_languages": ["python", "java", "c++", "javascript", "ruby", "php", "swift", "go", "kotlin", "typescript"], 
        "databases": ["sql", "database", "table", "row", "column", "query", "join", "index", "schema", "primary key"], 
        "big_data_tools": ["spark", "hadoop", "big data", "etl", "data lake", "data warehouse", "pipeline", "batch processing", "stream processing", "distributed systems"], 
        "machine_learning": ["classification", "prediction", "regression", "clustering", "dimensionality reduction", "anomaly detection", "time series", "forecasting", "natural language", "vision"], 
        "data_visualization": ["plot", "chart", "graph", "visualization", "dashboard", "report", "insight", "analysis", "trend", "metric"], 
        "cybersecurity": ["encryption", "decryption", "authentication", "authorization", "hashing", "ssl", "tls", "certificate", "secure", "firewall"], 
        "operating_systems": ["linux", "windows", "macos", "ubuntu", "redhat", "debian", "centos", "fedora", "arch", "manjaro"], 
        "web_development": ["web development", "frontend", "backend", "html", "css", "javascript", "react", "angular", "vue", "node.js"], 
        "mobile_development": ["mobile development", "android", "ios", "flutter", "react native", "swift", "kotlin", "objective-c", "xamarin", "cordova"], 
        "cloud_computing": ["cloud computing", "aws", "azure", "google cloud", "virtualization", "containers", "docker", "kubernetes", "serverless", "cloud storage"], 
        "project_management": ["project management", "scrum", "agile", "kanban", "gantt", "milestone", "task", "resource", "stakeholder", "deliverable"] 
    }




# Encode the input texts to obtain their embeddings
embeddings1 = model.encode('keyboard')
embeddings2 = model.encode('piano')
# embeddings3 = model.encode('apple')
# print(embeddings1)

# Calculate the cosine similarity between the embeddings
similarity_score = cosine_similarity([embeddings1, embeddings2])[0][1]
print(similarity_score)