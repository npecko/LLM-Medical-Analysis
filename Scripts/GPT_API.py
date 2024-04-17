from openai import OpenAI
from enum import Enum
import time

class Questions(str, Enum):
    HABITS = 'Потребител: Пациентът от този текст има ли вредни навици като тютюнопушене? - "{text}" Отговори само с "Да" или "Не". Асистент:'
    SMOKING = 'Потребител: Пациентът от този текст пушач ли е? - "{text}" Отговори само с "Да" или "Не". Асистент:'
    CONDITIONS = 'Потребител: Има ли информация от колко години пациентът е с диабет в този текст? - "{text}" Отговори само с "Да" или "Не". Асистент:'
    DURATION = 'Потребител: Пациентът от този текст от колко години има диабет? - "{text}" Отговори само с брой години. Асистент:'

#Load your API key to make requests.
client = OpenAI(
    api_key='{KEY}'
)

#Load manually classified file.
fr = open('{PATH}', 'r', encoding="utf8")
data = fr.readlines()
fr.close()

#Load generated output file.
fw = open('{PATH}', 'w', encoding="utf8")

for i in range(len(data)):
    print('Processing line ' + str(i+1) + ' of ' + str(len(data)) + '...')

    data[i] = data[i].strip().split(';')[0]
    line = data[i]
	
    for question in Questions:
        response = client.chat.completions.create(
            #Choose GPT model.
            model = '{MODEL}',
            messages = [
                {
                    'role': 'user', 
                    'content': question.value.format(text = data[i])
                }
            ],
            max_tokens =  50
        )
        print(response)
        output = response.choices[0].message.content
        line += ';' +  output.replace(',', '').replace('.', '').replace('\n', '')
        time.sleep(5)
    
    line = line.rstrip(';') + '\n'
    fw.write(line)

fw.close()