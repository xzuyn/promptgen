import os
import json
import re

new_data = []

for book_filename in os.listdir("books"):
    if os.path.isfile(os.path.join(os.path.curdir, "prompts", book_filename)):
        with open(os.path.join(os.path.curdir, "books", book_filename), "r", encoding="utf-8") as file:
            book = file.read().replace("<|endoftext|>", "").replace("</s>", "").replace("* * *", "").replace("***", "").replace("• • •", "").replace("\~ ", "").replace("\* ", "").replace("\_ ", "").replace("\*", "").replace("\_", "").replace("\~", "")
            book = re.sub("\[Genre:(.*?)\]\n", "", book)
            book = re.sub("(\n)+(?=[^\"'])", "\n\n", book)
            book = re.sub("(\n)+", "\n\n", book)
            book = re.sub("\[Genre:(.*?)\]\n", "", book)
            book = re.sub("(\n)+(?=[^\"'])", "\n\n", book)
            book = re.sub("\n\n\n", "\n\n", book)
            file.close()
        with open(os.path.join(os.path.curdir, "prompts", book_filename), "r", encoding="utf-8") as file:
            prompt = file.read()
            file.close()

        new_data.append(
            {
                "conversations": [
                    {"from": "system", "value": "Long story generator\n\n"},
                    {"from": "human", "value": prompt},
                    {"from": "gpt", "value": book},
                ]
            }
        )
        print(book_filename + " was added!")

with open("./bookgen.json", "w") as json_file:
    json.dump(new_data, json_file, indent=2)