import json

with open('./testRes/titles.json','r') as file:
    data = json.load(file)

you = quali = 0
for title in data:
    if 'you' in title.lower():
        you+=1
    if 'qualification' in title.lower():
        quali+=1

print('Qualification: ',quali)
print('about you: ',you)
print('length:', len(data))