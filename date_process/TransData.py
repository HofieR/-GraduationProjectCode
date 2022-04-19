from xlrd import open_workbook
import os
import csv


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


def splitText(textSet, keywordsSet):
    textKeywordsSet = []
    for i in range(len(textSet)):
        text = textSet[i]
        keywords = keywordsSet[i]
        if keywords == "":
            continue
        tmpTextSet = text.split("。")
        for j in range(len(tmpTextSet)):
            tmpText = tmpTextSet[j]
            if len(tmpText) > 10:
                textKeywordsSet.append((tmpText, keywords))
    return textKeywordsSet


def processDate(outFile, textKeywordsSet):
    for i in range(len(textKeywordsSet)):
        text = textKeywordsSet[i][0]
        keywordsSet = textKeywordsSet[i][1]
        keywords = keywordsSet.split(",")
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
        outFile.write(jsonText)
    outFile.close()


xlsFile = open_workbook(r'../date_process/data_native/dev.xls')
sheet = xlsFile.sheet_by_index(0)
textSet = sheet.col_values(0)
keywordsSet = sheet.col_values(1)
textKeywordsSet = splitText(textSet, keywordsSet)

jsonText = ""
os.remove("../date_process/data_processed/dev.json")
trainFile = open("../date_process/data_processed/dev.json", "a")

processDate(trainFile, textKeywordsSet)











