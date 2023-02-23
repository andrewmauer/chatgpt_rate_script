import openai
import csv

# Variables

openai.api_key = 'Your api key from https://platform.openai.com/account/api-keys'
model_engine = "text-davinci-003"
reviews_list = list()

# Functions

def answer(prompt):
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    result = ''.join(i for i in completion.choices[0].text if i.isdigit())
    if len(result) <= 2: # Проверка на правильность информации, иногда бот выдает оценку в формате "7 out of 10", а иногда просто "7"
        return result
    elif len(result) == 3:
        return result[0:1]
    elif len(result) >= 4:
        return result[0:2]

# Context Managers

# Reading unanalyzed csv file
with open('/Users/andrewmauer/Documents/Python Projects/ChatGPT API/reviews.csv', mode='r', encoding='utf-8') as input:#, open('', 'w') as output:
    file_reader = csv.reader(input, delimiter = ",")
    count = 0
    for row in file_reader:
        prompt = f'Act like a review analyst, who knows how to analyze and rank user reviews, rate a review "{row[1]}" from 1 to 10, where 10 is most enthusiastic and 1 is the most negative.'
        if count > 0:
            reviews_list.append([row[0], row[1], row[2], answer(prompt)])
        count += 1

# Creating analyzed csv file
with open('/Users/andrewmauer/Documents/Python Projects/ChatGPT API/reviews_analyzed.csv', mode="w", encoding='utf-8') as output:
    reviews_list = sorted(reviews_list, key=lambda x: x[3], reverse=True)
    file_writer = csv.writer(output, delimiter = ",", lineterminator="\r")
    file_writer.writerow(["email", "review text", "date", "rate"])
    for i in range(len(reviews_list)):
        file_writer.writerow([reviews_list[i][0], reviews_list[i][1], reviews_list[i][2], reviews_list[i][3]])
    print('Analysis is over. New file "reviews_analyzed.scv" has been created.')
