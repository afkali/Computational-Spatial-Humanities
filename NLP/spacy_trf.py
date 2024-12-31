import os
import spacy
import json

nlp = spacy.load("en_core_web_trf")

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        doc = nlp(text)
        
        loc_entities = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ == "LOC"]
        print(f"Entities found in {file_path}: {loc_entities}")  # debug statement
        return loc_entities

# create dictionary to store results
results = {}

# keep track of processed file paths
processed_files = set()

root_folder = "web scraping"
for folder_name, subfolders, filenames in os.walk(root_folder):
    for filename in filenames:
        if filename.lower().endswith('.txt'):
            file_path = os.path.join(folder_name, filename)
            if file_path not in processed_files:  # check if file is already processed
                rel_path = os.path.relpath(file_path, root_folder) 
                entities_found = process_file(file_path)  # extract entities
                if entities_found: 
                    results[rel_path] = entities_found 
                processed_files.add(file_path) 

# print results (cuz console goes brrrrrrr :D)
for file_path, entities in results.items():
    print(f"entities found in {file_path}:")
    for entity, label in entities:
        print(f"{entity} - {label}")

output_file = "NLP/location_entities.json"
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)
