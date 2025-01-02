import os
import json

new_data = []

for book_filename in os.listdir("combined"):
    with open(os.path.join(os.path.curdir, "combined", book_filename), "r", encoding="utf-8") as file:
        book = file.read()
        new_data.append(
            {
                "segments": [
                    {"label": True},
                    {"text": book}
                ]
            }
        )

with open("./bookgen_inputoutput.json", "w") as json_file:
    json.dump(new_data, json_file, indent=2)