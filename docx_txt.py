import os
import json
import docx2txt


FOLDER_PATH = "docs"
OUTPUT_PATH = "docs_txt"

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

hashmap = {}

for filename in os.listdir(FOLDER_PATH):
        if filename.endswith(".docx"):
            docx_file_path = os.path.join(FOLDER_PATH, filename)
            text = docx2txt.process(docx_file_path)
            filename = filename[:-4] + "txt"
            output_txt_path = os.path.join(OUTPUT_PATH, filename)
            if text is not None:
                with open(output_txt_path, "w", encoding="utf-8") as output_file:
                    output_file.write(text)
                print(f"Successfully saved extracted text to: {output_txt_path}")
            

