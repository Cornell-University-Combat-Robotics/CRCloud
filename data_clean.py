# {"title": "content": str}
import os
import json

FOLDER_PATH = "docs_txt"

hashmap = {}

for filename in os.listdir(FOLDER_PATH):
        if filename.endswith(".txt"):
            file_path = os.path.join(FOLDER_PATH, filename)
            
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r') as f:
                        hashmap[filename] = f.read()
                except IOError as e:
                    print(f"Error reading file {filename}")
                except UnicodeDecodeError as e:
                    print(f"Error decoding file {filename}")

folder_name = "json_data"
file_name = "janfab_data.json"

save_path = os.path.join(os.getcwd(), folder_name)
os.makedirs(save_path, exist_ok=True)
complete_name = os.path.join(save_path, file_name)

try:
    with open(complete_name, 'w') as json_file:
        json.dump(hashmap, json_file, indent=4)
    print(f"Successfully saved JSON file to: {complete_name}")
except IOError as e:
    print(f"Error saving file: {e}")
