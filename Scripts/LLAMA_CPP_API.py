from llama_cpp import Llama
from enum import Enum

class Questions(str, Enum):
    HABITS = 'Потребител: Пациентът от този текст има ли вредни навици като тютюнопушене? - "{text}" Отговори само с "Да" или "Не". Асистент:'
    SMOKING = 'Потребител: Пациентът от този текст пушач ли е? - "{text}" Отговори само с "Да" или "Не". Асистент:'
    CONDITIONS = 'Потребител: Има ли информация от колко години пациентът е с диабет в този текст? - "{text}" Отговори само с "Да" или "Не". Асистент:'
    DURATION = 'Потребител: Пациентът от този текст от колко години има диабет? - "{text}" Отговори само с брой години. Асистент:'

#Add the path to your model below.
llm = Llama(model_path='{PATH}', n_gpu_layers=-1)

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
        output = llm(q)
        line += ';' +  output['choices'][0]['text'].replace(',', '').replace('.', '').replace(';', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()
    line = line.rstrip(';') + '\n'
    fw.write(line)

fw.close()