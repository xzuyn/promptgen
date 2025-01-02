import requests
import os


if not os.path.exists("books"):
    os.makedirs("books")
    print(
        "You didn't have a books folder, I made one for you but you will have to put some books in it in utf-8 format."
    )
    exit(1)
if not os.path.exists("prompts"):
    os.makedirs("prompts")

ENDPOINT = "http://10.0.0.4:5001/api"
summary_to_prompt_prompt = """<|start_header_id|>system<|end_header_id|>

Your primary purpose is to generate writing prompts based on a story summary.<|eot_id|><|start_header_id|>user<|end_header_id|>

John Carter is a Confederate veteran who finds himself mysteriously transported to Mars, where he becomes embroiled in conflict between various warring tribes. He falls in love with Dejah Thoris, Princess of Helium, and eventually rescues her from captivity. Together, they face numerous challenges, including an attack from Zodanga forces during the Battle of Thark, before returning safely to Helium. The story concludes with the revelation that John must return to Earth after saving Barsoom's atmosphere plant.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Write a science fiction book about John Carter, a Confederate veteran who finds himself mysteriously transported to Mars, where he becomes embroiled in conflict between various warring tribes. He falls in love with Dejah Thoris, Princess of Helium, and eventually rescues her from captivity. Together, they face numerous challenges, including an attack from Zodanga forces during the Battle of Thark, before returning safely to Helium. The story concludes with the revelation that John must return to Earth after saving Barsoom's atmosphere plant.<|eot_id|><|start_header_id|>user<|end_header_id|>

Lucy Honeychurch is an upper-class Englishwoman living in Florence, Italy. After returning from Italy, Lucy becomes engaged to Cecil Vyse, a man who has been arranged for her to marry. However, after breaking off her engagement, Lucy embarks on a journey of self-discovery, during which she learns about love, relationships, and life's complexities. Eventually, she finds love and happiness with George Emerson, another character from the Bertolini pension.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Generate a book which follows Lucy Honeychurch, an upper-class Englishwoman living in Florence, Italy. After returning from Italy, Lucy becomes engaged to Cecil Vyse, a man who has been arranged for her to marry. However, after breaking off her engagement, Lucy embarks on a journey of self-discovery, during which she learns about love, relationships, and life's complexities. Eventually, she finds love and happiness with George Emerson, another character from the Bertolini pension.<|eot_id|><|start_header_id|>user<|end_header_id|>

Charles Darnay navigates the tumultuous times leading up to and during the French Revolution. In 1815, he returns to France to aid his downtrodden fellow countrymen only to be imprisoned on trumped-up charges. With the help of a friend named Sydney Carton, who has secretly loved Lucie for years, Darnay escapes the guillotine and flees to England.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Write a historical fiction book that follows Charles Darnay as he navigates the tumultuous times leading up to and during the French Revolution. In 1815, he returns to France to aid his downtrodden fellow countrymen only to be imprisoned on trumped-up charges. With the help of a friend named Sydney Carton, who has secretly loved Lucie for years, Darnay escapes the guillotine and flees to England.<|eot_id|><|start_header_id|>user<|end_header_id|>

A plain, unmarried woman named Valancy Stirling. The Stirling family believes she has heart disease; she believes it herself. She escapes from the burden of her dreary existence when she marries a free spirit named Barney Snaith and moves into his house on Mistawis Lake. There they live for a year together, during which time Valancy discovers that Dr. Trent made an error in his diagnosis and she is not dying.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Write a romance book about a plain, unmarried woman named Valancy Stirling. The Stirling family believes she has heart disease; she believes it herself. She escapes from the burden of her dreary existence when she marries a free spirit named Barney Snaith and moves into his house on Mistawis Lake. There they live for a year together, during which time Valancy discovers that Dr. Trent made an error in his diagnosis and she is not dying.<|eot_id|><|start_header_id|>user<|end_header_id|>

Sherlock Holmes helps solve several mysteries, including those involving missing coronets, a governess in an odd situation, and a murderous doctor.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Write a detective book where Sherlock Holmes helps solve several mysteries, including those involving missing coronets, a governess in an odd situation, and a murderous doctor.<|eot_id|><|start_header_id|>user<|end_header_id|>

Chief Inspector Kerry, of New Scotland Yard, who is investigating the murder of Sir Lucien Pyne and the mysterious disappearance of Mrs. Monte Irvin, while Sin Sin Wa, a Chinese drug dealer, and his wife are also involved in the case. Seton Pasha, a Home Office agent, works independently of the police, and together with Kerry they unravel the mystery surrounding the Kazmah group, composed of Sir Lucien, Sin Sin Wa, and Mrs. Sin.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Write a crime fiction book about Chief Inspector Kerry, of New Scotland Yard, who is investigating the murder of Sir Lucien Pyne and the mysterious disappearance of Mrs. Monte Irvin, while Sin Sin Wa, a Chinese drug dealer, and his wife are also involved in the case. Seton Pasha, a Home Office agent, works independently of the police, and together with Kerry they unravel the mystery surrounding the Kazmah group, composed of Sir Lucien, Sin Sin Wa, and Mrs. Sin.<|eot_id|><|start_header_id|>user<|end_header_id|>

The crew of the Solar Queen must deal with an outbreak of illness aboard their ship while fulfilling a contract with Sargolian clansmen. They descend upon Terraport without authorization to search for a medic to assist them. Medic Hovan joins the crew and identifies the source of the plague as alien creatures infesting their cargo from Sargol. The Queen is cleared of the plague charges after a dramatic broadcast by the crew, but a broken contract threatens their future in space.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Write a space opera book in which the crew of the Solar Queen must deal with an outbreak of illness aboard their ship while fulfilling a contract with Sargolian clansmen. They descend upon Terraport without authorization to search for a medic to assist them. Medic Hovan joins the crew and identifies the source of the plague as alien creatures infesting their cargo from Sargol. The Queen is cleared of the plague charges after a dramatic broadcast by the crew, but a broken contract threatens their future in space.<|eot_id|>"""


def get_prompt_summary(user_msg):
    return {
        "prompt": f"{user_msg}",
        "use_story": "False",  # Use the story from the KoboldAI UI, can be managed using other API calls (See /api for the documentation)
        "use_memory": "False",  # Use the memnory from the KoboldAI UI, can be managed using other API calls (See /api for the documentation)
        "use_authors_note": "False",  # Use the authors notes from the KoboldAI UI, can be managed using other API calls (See /api for the documentation)
        "use_world_info": "False",  # Use the World Info from the KoboldAI UI, can be managed using other API calls (See /api for the documentation)
        "max_context_length": 2048,  # How much of the prompt will we submit to the AI generator? (Prevents AI / memory overloading)
        "max_length": 512,  # How long should the response be?
        "rep_pen": 1.03,  # Prevent the AI from repeating itself
        "rep_pen_range": 2048,  # The range to which to apply the previous
        "rep_pen_slope": 0.7,  # This number determains the strength of the repetition penalty over time
        "temperature": 0.1,  # How random should the AI be? In a low value we pick the most probable token, high values are a dice roll
        "tfs": 1.0,  # Tail free sampling, https://www.trentonbricken.com/Tail-Free-Sampling/
        "top_a": 0.0,  # Top A sampling , https://github.com/BlinkDL/RWKV-LM/tree/4cb363e5aa31978d801a47bc89d28e927ab6912e#the-top-a-sampling-method
        "top_k": 0,  # Keep the X most probable tokens
        "top_p": 0,  # Top P sampling / Nucleus Sampling, https://arxiv.org/pdf/1904.09751.pdf
        "typical": 1.0,  # Typical Sampling, https://arxiv.org/pdf/2202.00666.pdf
        "sampler_order": [  # Order to apply the samplers, our default in this script is already the optimal one. KoboldAI Lite contains an easy list of what the
            6,
            0,
            1,
            3,
            4,
            2,
            5,
        ],
        "stop_sequence": [  # When should the AI stop generating? In this example we stop when it tries to speak on behalf of the user.
            "<",
            ". [",
            "<SUMMARY",
            "SUMMARY>",
            "PROMPT>",
            "<PROMPT",
            ".assistant",
            "###",
            " # ",
            " * ",
            ". Please",
            ". I",
            "Note:",
            ". I",
            ". 1",
            ".  ",
            "Word Count",
            ". (",
            ">",
            "  .",
            "-end-",
            ". End",
        ],
        # "sampler_seed": 1337, # Use specific seed for text generation? This helps with consistency across tests.
        "singleline": "False",  # Only return a response that fits on a single line, this can help with chatbots but also makes them less verbose
        "sampler_full_determinism": "False",  # Always return the same result for the same query, best used with a static seed
        "frmttriminc": "True",  # Trim incomplete sentences, prevents sentences that are unfinished but can interfere with coding and other non english sentences
        "frmtrmblln": "False",  # Remove blank lines
        "quiet": "False",  # Don't print what you are doing in the KoboldAI console, helps with user privacy
        "trim_stop": "True",
        "use_default_badwordsids": "False",
    }


def get_book_summary(user_msg):
    return {
        "prompt": f"{user_msg}",
        "use_story": "False",  # Use the story from the KoboldAI UI, can be managed using other API calls (See /api for the documentation)
        "use_memory": "False",  # Use the memnory from the KoboldAI UI, can be managed using other API calls (See /api for the documentation)
        "use_authors_note": "False",  # Use the authors notes from the KoboldAI UI, can be managed using other API calls (See /api for the documentation)
        "use_world_info": "False",  # Use the World Info from the KoboldAI UI, can be managed using other API calls (See /api for the documentation)
        "max_context_length": 131072,  # How much of the prompt will we submit to the AI generator? (Prevents AI / memory overloading)
        "max_length": 512,  # How long should the response be?
        "rep_pen": 1.15,  # Prevent the AI from repeating itself
        "rep_pen_range": 2048,  # The range to which to apply the previous
        "rep_pen_slope": 0.7,  # This number determains the strength of the repetition penalty over time
        "temperature": 0.5,  # How random should the AI be? In a low value we pick the most probable token, high values are a dice roll
        "tfs": 1.0,  # Tail free sampling, https://www.trentonbricken.com/Tail-Free-Sampling/
        "top_a": 0.0,  # Top A sampling , https://github.com/BlinkDL/RWKV-LM/tree/4cb363e5aa31978d801a47bc89d28e927ab6912e#the-top-a-sampling-method
        "top_k": 0,  # Keep the X most probable tokens
        "top_p": 0,  # Top P sampling / Nucleus Sampling, https://arxiv.org/pdf/1904.09751.pdf
        "typical": 1.0,  # Typical Sampling, https://arxiv.org/pdf/2202.00666.pdf
        "sampler_order": [  # Order to apply the samplers, our default in this script is already the optimal one. KoboldAI Lite contains an easy list of what the
            6,
            0,
            1,
            3,
            4,
            2,
            5,
        ],
        "stop_sequence": [  # When should the AI stop generating? In this example we stop when it tries to speak on behalf of the user.
            "<",
            ". [",
            "###",
            " # ",
            " * ",
            ". Please",
            ".assistant",
            ". I",
            "Note:",
            ". I",
            ". 1",
            ".  ",
            "Word Count",
            ". [",
            ". (",
            ">",
            "  .",
            "-end-",
            ". End",
            "\\n",
        ],
        # "sampler_seed": 1337, # Use specific seed for text generation? This helps with consistency across tests.
        "singleline": "False",  # Only return a response that fits on a single line, this can help with chatbots but also makes them less verbose
        "sampler_full_determinism": "False",  # Always return the same result for the same query, best used with a static seed
        "frmttriminc": "True",  # Trim incomplete sentences, prevents sentences that are unfinished but can interfere with coding and other non english sentences
        "frmtrmblln": "False",  # Remove blank lines
        "quiet": "False",  # Don't print what you are doing in the KoboldAI console, helps with user privacy
        "trim_stop": "True",
        "use_default_badwordsids": "False",
    }


for book_filename in os.listdir("books"):
    if not os.path.isfile(os.path.join(os.path.curdir, "prompts", book_filename)):
        with open(
            os.path.join(os.path.curdir, "books", book_filename), "r", encoding="utf-8"
        ) as file:
            book = file.read()

        prompt = get_book_summary(
            f"<|start_header_id|>user<|end_header_id|>\n\n"
            f"{book}"
            f"\n\n---"
            f"\n\nGive me the TLDR of the above.<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        )
        response = requests.post(f"{ENDPOINT}/v1/generate", json=prompt)
        if response.status_code == 200:
            results = response.json()["results"]
            text = results[0]["text"]
            summary = (
                text.replace("###", "")
                .replace(". Please", "")
                .replace("###", "")
                .replace(" ***", "")
                .replace("***", "")
                .replace(" # ", "")
                .replace(" * ", "")
                .replace("Note:", "")
                .replace(". 1", "")
                .replace("Word Count", "")
                .replace("</", "")
                .replace("</", "")
            )

        prompt = get_prompt_summary(
            summary_to_prompt_prompt
            + f"<|start_header_id|>user<|end_header_id|>\n\n{summary}<|eot_id|>"
            + "<|start_header_id|>assistant<|end_header_id|>\n\n"
        )
        response = requests.post(f"{ENDPOINT}/v1/generate", json=prompt)
        if response.status_code == 200:
            results = response.json()["results"]
            text = results[0]["text"]
            text = (
                text.replace("<PROMPT>\n", "")
                .replace("<SUMMARY>\n", "")
                .replace("\n<SUMMARY>", "")
                .replace("\n", "")
                .replace(" # ", "")
                .replace("</", "")
                .replace(" * ", "")
                .replace(". In", ".")
                .replace(". If", ".")
                .replace(". It", ".")
                .replace(".**", ".")
                .replace("Note:", "")
                .replace("The end.", "")
                .replace(". 1", "")
                .replace("Word Count", "")
                .replace(". .", ".")
                .replace(".  .", ".")
            )
            with open(
                os.path.join(os.path.curdir, "prompts", book_filename),
                "w",
                encoding="utf-8",
            ) as file:
                file.write(text)
            print("OUTPUT:", text)
        else:
            raise RuntimeError("Could not talk to the API")
