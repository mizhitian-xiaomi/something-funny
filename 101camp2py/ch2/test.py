str1 = 'daf'
str2 = "def"
print(type(str1))
print(type(str2))

import json


# load & dump 对文件进行操作
listStr = [{"city": " 长沙", "name": "臭豆腐"}]
with open('listStr.json', 'w', encoding="utf-8") as file:
    json.dump(listStr, file, ensure_ascii=False)

print("-" * 25)

f = open('listStr.json', encoding='utf-8')
listStr = json.load(f)
print(listStr)
print(type(listStr))
f.close()
