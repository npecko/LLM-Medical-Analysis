import anthropic
from enum import Enum
import re
import time

class Questions(str, Enum):
    HABITS = 'Потребител: Пациентът от този текст има ли вредни навици като тютюнопушене? - "{text}"|||Отговори само с "Да" или "Не".'
    SMOKING = 'Потребител: Пациентът от този текст пушач ли е? - "{text}"|||Отговори само с "Да" или "Не".'
    CONDITIONS = 'Потребител: Има ли информация от колко години пациентът е с диабет в този текст? - "{text}"|||Отговори само с "Да" или "Не".'
    DURATION = 'Потребител: Пациентът от този текст от колко години има диабет? - "{text}"|||Отговори само с брой години.'

#Load your API key to make requests.
client = anthropic.Anthropic(
    api_key="{KEY}",
)

#Load manually classified file.
fr = open('{PATH}', 'r', encoding="utf8")
data = fr.readlines()
fr.close()

#Load generated output file.
fw = open('{PATH}', 'w', encoding="utf8")

for i in range(len(data)):
    print('Processing line ' + str(i+1) + ' of ' + str(len(data)) + '...' + '\n')

    data[i] = data[i].strip().split(';')[0]
    line = data[i]
	
    for question in Questions:
        q = question.value.format(text = data[i])
        
        message = client.messages.create(
            #Choose Claude model.
            model="{MODEL}",
            max_tokens=5,
            temperature=0.0,
            system=q.split('|||')[1],
            messages=[
                {"role": "user", "content": q.split('|')[0]}
            ]
        )

        line += ';' +  re.findall(r'(?<=\[ContentBlock\(text\=\')(.*?)(?=\'\, type\=\'text\'\)\])', str(message.content))[0].replace(',', '').replace('.', '').replace(';', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()
    line = line.rstrip(';') + '\n'
    fw.write(line)
    
    time.sleep(60)

fw.close()