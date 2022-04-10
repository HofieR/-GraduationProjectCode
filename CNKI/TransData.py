from xlrd import open_workbook
import os

#{"text": "0000000", "label": {"keyword": {"1111": [[0, 2]], "2222": [[9, 13]]}}}


def findAllIndex(str_, a):
    index_list = []
    start = 0
    while True:
        x = str_.find(a, start)
        if x > -1:
            start = x+1
            index_list.append(x)
        else:
            break
    return index_list


xlsFile = open_workbook(r'./selenium_data/test.xls')
sheet = xlsFile.sheet_by_index(0)
textSet = sheet.col_values(0)
keywordsSet = sheet.col_values(1)
jsonText = ""
os.remove("train2.json")
os.remove("dev2.json")
os.remove("test2.json")
trainFile = open("train2.json", "a")
devFile = open("dev2.json", "a")
testFile = open("test2.json", "a")

for i in range(8000):
    text = textSet[i]
    keywords = keywordsSet[i].split(".")
    jsonText = "{\"text\": \"" + text + "\", \"label\": {\"keyword\": {"
    tmp1 = 0
    for keyword in keywords:
        if text.find(keyword) > -1:
            if tmp1 != 0:
                jsonText += ", "
            tmp1 += 1
            jsonText += "\"" + keyword + "\": ["
            begIdxes = findAllIndex(text, keyword)
            keywordLen = len(keyword)
            tmp2 = 0
            for begIdx in begIdxes:
                if tmp2 != 0:
                    jsonText += ", "
                tmp2 += 1
                jsonText += "[" + str(begIdx) + ", " + str(begIdx + keywordLen - 1) + "]"
            jsonText = jsonText + "]"
    if tmp1 == 0:
        jsonText = ""
    else:
        jsonText += "}}}\n"
    trainFile.write(jsonText)

for i in range(8000, 9000):
    text = textSet[i]
    keywords = keywordsSet[i].split(".")
    jsonText = "{\"text\": \"" + text + "\", \"label\": {\"keyword\": {"
    tmp1 = 0
    for keyword in keywords:
        if text.find(keyword) > -1:
            if tmp1 != 0:
                jsonText += ", "
            tmp1 += 1
            jsonText += "\"" + keyword + "\": ["
            begIdxes = findAllIndex(text, keyword)
            keywordLen = len(keyword)
            tmp2 = 0
            for begIdx in begIdxes:
                if tmp2 != 0:
                    jsonText += ", "
                tmp2 += 1
                jsonText += "[" + str(begIdx) + ", " + str(begIdx + keywordLen - 1) + "]"
            jsonText = jsonText + "]"
    if tmp1 == 0:
        jsonText = ""
    else:
        jsonText += "}}}\n"
    devFile.write(jsonText)

jsonFile.close()








