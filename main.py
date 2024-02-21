import requests
from PRIVATE_KEYS import OPENAI_API_KEY


# API endpoint for ChatGPT
api_url = 'https://api.openai.com/v1/chat/completions'

# Headers including the Authorization with your API key
headers = {
    'Authorization': f'Bearer {OPENAI_API_KEY}',
    'Content-Type': 'application/json'
}

#model = 'gpt-4-1106-preview'
model = "gpt-3.5-turbo"


#person_1 = "Olaf Scholz von der SPD, deutscher Bundeskanzler"
person_1 = "Robert Habeck von den Grünen, deutscher Wirtschaftsminister"
person_1 = "Christian Lindner von der FDP, deutscher Finanzminister"
person_2 = "Bernd Striezel, Reporter vom Wirtschafts-Magazin Kurse, Trends und Rendite"
person_1_short = "Lindner"#"Habeck"
person_2_short = "Reporter"

first_sentence = f"Die Wirtschaft in Deutschland wächst weniger als erwartet. Lediglich um 0,2 Prozent mehr soll das Bruttoinlandsprodukt steigen. Wie möchten Sie dem entgegen, Herr {person_1_short}?"
#first_sentence = "Sollten wir wegen Herausforderungen in Wirtschaft und Klima neue Schulden aufnehmen?"

swap = True
if swap:
    tmp = person_1
    tmp_s = person_1_short
    person_1 = person_2
    person_1_short = person_2_short
    person_2 = tmp
    person_2_short = tmp_s

robert = [
    {'role': 'system', 'content': f'Du schauspielst so, als wärst du {person_1}. Du hältst dich jedoch sehr kurz, benutzt maximal 30 Wörter. Dein Gesprächspartner tut so, als sei er {person_2}. Manchmal, wenn ihr zu einem Fazit kommt, beginnst du eine neue Diskussion oder provokante Aussage zu aktuellem politischen Thema. Manchmal lässt du aber auch der anderen Person Raum für neue Themen. Nach längerer Zeit würgst du das Gespräch ab.'},
    {'role': 'assistant', 'content': first_sentence}
]


lindner = [
    {'role': 'system', 'content': f'Du schauspielst so, als wärst du {person_2}. Du hältst dich jedoch sehr kurz, benutzt maximal 30 Wörter. Dein Gesprächspartner tut so, als sei er {person_1}. Manchmal, wenn ihr zu einem Fazit kommt, beginnst du eine neue Diskussion oder provokante Aussage zu aktuellem politischen Thema. Manchmal lässt du aber auch der anderen Person Raum für neue Themen. Nach längerer Zeit würgst du das Gespräch ab.'},
    {'role': 'user', 'content': first_sentence}
]

print(f"{person_1_short}: {first_sentence}")

print_speed = 50.

import time
time.sleep(len(first_sentence)/print_speed)
print("------------------------------------------------------------------------------------------")

for i in range(10):

    # 2. LINDNERS ANTWORT

    # Data payload for the request, specifying the model and the input message
    data = {
        'model': model,
        'messages': lindner,
        #"max_tokens": 100,
        'temperature': 0.7
    }

    # Making the POST request
    response = requests.post(api_url, json=data, headers=headers)

    # Checking if the request was successful
    if response.status_code == 200:
        answer = response.json()
        print(f'{person_2_short}: {answer["choices"][0]["message"]["content"]}')
        time.sleep(len(answer["choices"][0]["message"]["content"])/print_speed)
        lindner.append({"role": "assistant", "content": answer["choices"][0]["message"]["content"]})
        robert.append({"role": "user", "content": answer["choices"][0]["message"]["content"]})
    else:
        print("Error:", response.status_code, response.text)

    print("------------------------------------------------------------------------------------------")

    # 1. ROBERTS ANTWORT

    # Data payload for the request, specifying the model and the input message
    data = {
        'model': model,
        'messages': robert,
        # "max_tokens": 100,
        'temperature': 0.7
    }

    # Making the POST request
    response = requests.post(api_url, json=data, headers=headers)

    # Checking if the request was successful
    if response.status_code == 200:
        answer = response.json()
        print(f'{person_1_short}: {answer["choices"][0]["message"]["content"]}')
        time.sleep(len(answer["choices"][0]["message"]["content"])/print_speed)
        robert.append({"role": "assistant", "content": answer["choices"][0]["message"]["content"]})
        lindner.append({"role": "user", "content": answer["choices"][0]["message"]["content"]})
    else:
        print("Error:", response.status_code, response.text)

    #print(robert)

    #print(lindner)
    print("------------------------------------------------------------------------------------------")

