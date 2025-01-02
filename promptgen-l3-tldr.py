import requests
import os

if not os.path.exists("books"): 
    os.makedirs("books") 
    print("You didn't have a books folder, I made one for you but you will have to put some books in it in utf-8 format.")
    exit(1)
if not os.path.exists("prompts"): 
    os.makedirs("prompts") 

ENDPOINT = "http://10.0.0.4:5001/api"
summary_to_prompt_prompt = "<SUMMARY>\nJohn Carter is a Confederate veteran who finds himself mysteriously transported to Mars, where he becomes embroiled in conflict between various warring tribes. He falls in love with Dejah Thoris, Princess of Helium, and eventually rescues her from captivity. Together, they face numerous challenges, including an attack from Zodanga forces during the Battle of Thark, before returning safely to Helium. The story concludes with the revelation that John must return to Earth after saving Barsoom's atmosphere plant.\n<PROMPT>\nWrite a science fiction book about John Carter, a Confederate veteran who finds himself mysteriously transported to Mars, where he becomes embroiled in conflict between various warring tribes. He falls in love with Dejah Thoris, Princess of Helium, and eventually rescues her from captivity. Together, they face numerous challenges, including an attack from Zodanga forces during the Battle of Thark, before returning safely to Helium. The story concludes with the revelation that John must return to Earth after saving Barsoom's atmosphere plant.\n<SUMMARY>\nLucy Honeychurch is an upper-class Englishwoman living in Florence, Italy. After returning from Italy, Lucy becomes engaged to Cecil Vyse, a man who has been arranged for her to marry. However, after breaking off her engagement, Lucy embarks on a journey of self-discovery, during which she learns about love, relationships, and life's complexities. Eventually, she finds love and happiness with George Emerson, another character from the Bertolini pension.\n<PROMPT>\nGenerate a book which follows Lucy Honeychurch, an upper-class Englishwoman living in Florence, Italy. After returning from Italy, Lucy becomes engaged to Cecil Vyse, a man who has been arranged for her to marry. However, after breaking off her engagement, Lucy embarks on a journey of self-discovery, during which she learns about love, relationships, and life's complexities. Eventually, she finds love and happiness with George Emerson, another character from the Bertolini pension.\n<SUMMARY>\nCharles Darnay navigates the tumultuous times leading up to and during the French Revolution. In 1815, he returns to France to aid his downtrodden fellow countrymen only to be imprisoned on trumped-up charges. With the help of a friend named Sydney Carton, who has secretly loved Lucie for years, Darnay escapes the guillotine and flees to England.\n<PROMPT>\nWrite a historical fiction book that follows Charles Darnay as he navigates the tumultuous times leading up to and during the French Revolution. In 1815, he returns to France to aid his downtrodden fellow countrymen only to be imprisoned on trumped-up charges. With the help of a friend named Sydney Carton, who has secretly loved Lucie for years, Darnay escapes the guillotine and flees to England.\n<SUMMARY>\nA plain, unmarried woman named Valancy Stirling. The Stirling family believes she has heart disease; she believes it herself. She escapes from the burden of her dreary existence when she marries a free spirit named Barney Snaith and moves into his house on Mistawis Lake. There they live for a year together, during which time Valancy discovers that Dr. Trent made an error in his diagnosis and she is not dying.\n<PROMPT>\nWrite a romance book about a plain, unmarried woman named Valancy Stirling. The Stirling family believes she has heart disease; she believes it herself. She escapes from the burden of her dreary existence when she marries a free spirit named Barney Snaith and moves into his house on Mistawis Lake. There they live for a year together, during which time Valancy discovers that Dr. Trent made an error in his diagnosis and she is not dying.\n<SUMMARY>\nSherlock Holmes helps solve several mysteries, including those involving missing coronets, a governess in an odd situation, and a murderous doctor.\n<PROMPT>\nWrite a detective book where Sherlock Holmes helps solve several mysteries, including those involving missing coronets, a governess in an odd situation, and a murderous doctor.\n<SUMMARY>\nChief Inspector Kerry, of New Scotland Yard, who is investigating the murder of Sir Lucien Pyne and the mysterious disappearance of Mrs. Monte Irvin, while Sin Sin Wa, a Chinese drug dealer, and his wife are also involved in the case. Seton Pasha, a Home Office agent, works independently of the police, and together with Kerry they unravel the mystery surrounding the Kazmah group, composed of Sir Lucien, Sin Sin Wa, and Mrs. Sin.\n<PROMPT>\nWrite a crime fiction book about Chief Inspector Kerry, of New Scotland Yard, who is investigating the murder of Sir Lucien Pyne and the mysterious disappearance of Mrs. Monte Irvin, while Sin Sin Wa, a Chinese drug dealer, and his wife are also involved in the case. Seton Pasha, a Home Office agent, works independently of the police, and together with Kerry they unravel the mystery surrounding the Kazmah group, composed of Sir Lucien, Sin Sin Wa, and Mrs. Sin.\n<SUMMARY>\nThe crew of the Solar Queen must deal with an outbreak of illness aboard their ship while fulfilling a contract with Sargolian clansmen. They descend upon Terraport without authorization to search for a medic to assist them. Medic Hovan joins the crew and identifies the source of the plague as alien creatures infesting their cargo from Sargol. The Queen is cleared of the plague charges after a dramatic broadcast by the crew, but a broken contract threatens their future in space.\n<PROMPT>\nWrite a space opera book in which the crew of the Solar Queen must deal with an outbreak of illness aboard their ship while fulfilling a contract with Sargolian clansmen. They descend upon Terraport without authorization to search for a medic to assist them. Medic Hovan joins the crew and identifies the source of the plague as alien creatures infesting their cargo from Sargol. The Queen is cleared of the plague charges after a dramatic broadcast by the crew, but a broken contract threatens their future in space.<SUMMARY>\n"
book_summerization_prompt = "\n<|eot_id|><|start_header_id|>user<|end_header_id|>\n\Give me the TLDR of the above.\n<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
def get_prompt_summary(user_msg):
    return {
        "prompt": f"{user_msg}",
        "use_story": "False", # Use the story from the KoboldAI UI, can be managed using other API calls (See /api for the documentation)
        "use_memory": "False", # Use the memnory from the KoboldAI UI, can be managed using other API calls (See /api for the documentation)
        "use_authors_note": "False", # Use the authors notes from the KoboldAI UI, can be managed using other API calls (See /api for the documentation)
        "use_world_info": "False", # Use the World Info from the KoboldAI UI, can be managed using other API calls (See /api for the documentation)
        "max_context_length": 2048, # How much of the prompt will we submit to the AI generator? (Prevents AI / memory overloading)
        "max_length": 512, # How long should the response be?
        "rep_pen": 1.03, # Prevent the AI from repeating itself
        "rep_pen_range": 2048, # The range to which to apply the previous
        "rep_pen_slope": 0.7, # This number determains the strength of the repetition penalty over time
        "temperature": 0.1, # How random should the AI be? In a low value we pick the most probable token, high values are a dice roll
        "tfs": 1.0, # Tail free sampling, https://www.trentonbricken.com/Tail-Free-Sampling/
        "top_a": 0.0, # Top A sampling , https://github.com/BlinkDL/RWKV-LM/tree/4cb363e5aa31978d801a47bc89d28e927ab6912e#the-top-a-sampling-method
        "top_k": 0, # Keep the X most probable tokens
        "top_p": 0, # Top P sampling / Nucleus Sampling, https://arxiv.org/pdf/1904.09751.pdf
        "typical": 1.0, # Typical Sampling, https://arxiv.org/pdf/2202.00666.pdf
        "sampler_order": [6,0,1,3,4,2,5], # Order to apply the samplers, our default in this script is already the optimal one. KoboldAI Lite contains an easy list of what the
        "stop_sequence": ["<", ". [", "<SUMMARY", "SUMMARY>", "PROMPT>", "<PROMPT", ".assistant", "###", " # ", " * ", ". Please", ". I", "Note:", ". I", ". 1", ".  ", "Word Count", ". (", ">", "  .", "-end-", ". End"], # When should the AI stop generating? In this example we stop when it tries to speak on behalf of the user.
        #"sampler_seed": 1337, # Use specific seed for text generation? This helps with consistency across tests.
        "singleline": "False", # Only return a response that fits on a single line, this can help with chatbots but also makes them less verbose
        "sampler_full_determinism": "False", # Always return the same result for the same query, best used with a static seed
        "frmttriminc": "True", # Trim incomplete sentences, prevents sentences that are unfinished but can interfere with coding and other non english sentences
        "frmtrmblln": "False", #Remove blank lines
        "quiet": "False", # Don't print what you are doing in the KoboldAI console, helps with user privacy
        "trim_stop": "True",
        "use_default_badwordsids": "False"
        }

def get_book_summary(user_msg):
    return {
        "prompt": f"{user_msg}",
        "use_story": "False", # Use the story from the KoboldAI UI, can be managed using other API calls (See /api for the documentation)
        "use_memory": "False", # Use the memnory from the KoboldAI UI, can be managed using other API calls (See /api for the documentation)
        "use_authors_note": "False", # Use the authors notes from the KoboldAI UI, can be managed using other API calls (See /api for the documentation)
        "use_world_info": "False", # Use the World Info from the KoboldAI UI, can be managed using other API calls (See /api for the documentation)
        "max_context_length": 131072, # How much of the prompt will we submit to the AI generator? (Prevents AI / memory overloading)
        "max_length": 512, # How long should the response be?
        "rep_pen": 1.15, # Prevent the AI from repeating itself
        "rep_pen_range": 2048, # The range to which to apply the previous
        "rep_pen_slope": 0.7, # This number determains the strength of the repetition penalty over time
        "temperature": 0.5, # How random should the AI be? In a low value we pick the most probable token, high values are a dice roll
        "tfs": 1.0, # Tail free sampling, https://www.trentonbricken.com/Tail-Free-Sampling/
        "top_a": 0.0, # Top A sampling , https://github.com/BlinkDL/RWKV-LM/tree/4cb363e5aa31978d801a47bc89d28e927ab6912e#the-top-a-sampling-method
        "top_k": 0, # Keep the X most probable tokens
        "top_p": 0, # Top P sampling / Nucleus Sampling, https://arxiv.org/pdf/1904.09751.pdf
        "typical": 1.0, # Typical Sampling, https://arxiv.org/pdf/2202.00666.pdf
        "sampler_order": [6,0,1,3,4,2,5], # Order to apply the samplers, our default in this script is already the optimal one. KoboldAI Lite contains an easy list of what the
        "stop_sequence": ["<", ". [", "###", " # ", " * ", ". Please", ".assistant", ". I", "Note:", ". I", ". 1", ".  ", "Word Count", ". [", ". (", ">", "  .", "-end-", ". End", "\\n"], # When should the AI stop generating? In this example we stop when it tries to speak on behalf of the user.
        #"sampler_seed": 1337, # Use specific seed for text generation? This helps with consistency across tests.
        "singleline": "False", # Only return a response that fits on a single line, this can help with chatbots but also makes them less verbose
        "sampler_full_determinism": "False", # Always return the same result for the same query, best used with a static seed
        "frmttriminc": "True", # Trim incomplete sentences, prevents sentences that are unfinished but can interfere with coding and other non english sentences
        "frmtrmblln": "False", #Remove blank lines
        "quiet": "False", # Don't print what you are doing in the KoboldAI console, helps with user privacy
        "trim_stop": "True",
        "use_default_badwordsids": "False"
        }

for book_filename in os.listdir('books'):
    if not os.path.isfile(os.path.join(os.path.curdir, 'prompts', book_filename)):
        with open(os.path.join(os.path.curdir, 'books', book_filename), 'r', encoding='utf-8') as file:
            book = file.read()

        prompt = get_book_summary(book + book_summerization_prompt)
        response = requests.post(f"{ENDPOINT}/v1/generate", json=prompt)
        if response.status_code == 200:
            results = response.json()['results']
            text = results[0]['text']
            summary = text.replace("###", "").replace(". Please", "").replace("###", "").replace(" ***", "").replace("***", "").replace(" # ", "").replace(" * ", "").replace("Note:", "").replace(". 1", "").replace("Word Count", "").replace("</", "").replace("</", "")

        #with open('summary.txt', 'r') as file:
        #    summary = file.read()
        #summary = "Martians invade Earth with plans to colonize the planet. They create massive destruction using advanced technology and weaponry. Humans struggle to fight back against their seemingly unstoppable force until the Martian invaders fall victim to microscopic Earth bacteria they are unable to resist. The novel explores themes of colonialism, survival, and the limitations of human ingenuity when confronted by overwhelming power."
        #print("INPUT:", summary_to_prompt_prompt + summary)
        prompt = get_prompt_summary(summary_to_prompt_prompt + summary + "\n<PROMPT>\n")
        response = requests.post(f"{ENDPOINT}/v1/generate", json=prompt)
        if response.status_code == 200:
            results = response.json()['results']
            text = results[0]['text']
            text = text.replace("<PROMPT>\n", "").replace("<SUMMARY>\n", "").replace("\n<SUMMARY>", "").replace("\n", "").replace(" # ", "").replace("</", "").replace(" * ", "").replace(". In", ".").replace(". If", ".").replace(". It", ".").replace(".**", ".").replace("Note:", "").replace("The end.", "").replace(". 1", "").replace("Word Count", "").replace(". .", ".").replace(".  .", ".")
            with open(os.path.join(os.path.curdir, 'prompts', book_filename), 'w', encoding='utf-8') as file:
                file.write(text)
            print("OUTPUT:", text)
        else:
            raise RuntimeError("Could not talk to the API")