system = "<|begin_of_text|>Long story generator\n\n"
input_tag = "### Instruction:\n"
output_tag = "\n### Response:\n"
eot_id = "<|eot_id|>"

import re
import os

if not os.path.exists("books"): 
    print("You didn't have a required folder, did you use promptgen?.")
    exit(1)
if not os.path.exists("prompts"): 
    print("You didn't have a required folder, did you use promptgen?.")
    exit(1)
if not os.path.exists("combined"): 
    os.makedirs("combined") 

for book_filename in os.listdir('books'):
    if os.path.isfile(os.path.join(os.path.curdir, 'prompts', book_filename)):
        with open(os.path.join(os.path.curdir, 'books', book_filename), 'r', encoding='utf-8') as file:
            book = file.read().replace("<|endoftext|>", "").replace("</s>", "").replace("* * *", "").replace("***", "").replace("• • •", "").replace("\~ ", "").replace("\* ", "").replace("\_ ", "").replace("\*", "").replace("\_", "").replace("\~", "")
            book = re.sub("\[Genre:(.*?)\]\n", "", book)
            book = re.sub("(\n)+(?=[^\"'])", "\n\n", book)
            book = re.sub("(\n)+", "\n\n", book)
            book = re.sub("\[Genre:(.*?)\]\n", "", book)
            book = re.sub("(\n)+(?=[^\"'])", "\n\n", book)
            file.close()
        with open(os.path.join(os.path.curdir, 'prompts', book_filename), 'r', encoding='utf-8') as file:
            prompt = file.read()
            file.close()
        combined = system + input_tag + prompt + output_tag + book + eot_id
        with open(os.path.join(os.path.curdir, 'combined', book_filename), 'w', encoding='utf-8') as file:
            file.write(combined)
            print(book_filename + " was combined!")
            file.close()