from xlrd import open_workbook
import os


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
        if keywords == "" or len(text) < 5:
            continue
        tmpTextSet = text.split("。")
        for j in range(len(tmpTextSet)):
            tmpText = tmpTextSet[j]
            if 50 > len(tmpText) > 10:
                textKeywordsSet.append((tmpText, keywords))
    return textKeywordsSet


def processDataWithLabel(outFile, textKeywordsSet):
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


def processDataWithoutLabel(outFile, textKeywordsSet):
    for i in range(len(textKeywordsSet)):
        text = textKeywordsSet[i][0]
        jsonText = "{\"id\": " + str(i) + ", \"text\": \"" + text + "\"}\n"
        outFile.write(jsonText)
    outFile.close()

if __name__ == '__main__':
    xlsFileTrain = open_workbook(r'train_data/data_native/train.xls')
    xlsFileDev = open_workbook(r'train_data/data_native/dev.xls')
    xlsFileTest = open_workbook(r'train_data/data_native/test.xls')

    sheetTrain = xlsFileTrain.sheet_by_index(0)
    sheetDev = xlsFileDev.sheet_by_index(0)
    sheetTest = xlsFileTest.sheet_by_index(0)
    titleKeywordsSetTrain = splitText(sheetTrain.col_values(0), sheetTrain.col_values(2))
    SummaryKeywordsSetTrain = splitText(sheetTrain.col_values(1), sheetTrain.col_values(2))
    titleKeywordsSetDev = splitText(sheetDev.col_values(0), sheetDev.col_values(2))
    SummaryKeywordsSetDev = splitText(sheetDev.col_values(1), sheetDev.col_values(2))
    titleKeywordsSetTest = splitText(sheetTest.col_values(0), sheetTest.col_values(2))
    SummaryKeywordsSetTest = splitText(sheetTest.col_values(1), sheetTest.col_values(2))

    jsonText = ""
    os.remove("train_data/data_processed/titleTrain.json")
    os.remove("train_data/data_processed/titleDev.json")
    os.remove("train_data/data_processed/titleTest.json")
    os.remove("train_data/data_processed/summaryTrain.json")
    os.remove("train_data/data_processed/summaryDev.json")
    os.remove("train_data/data_processed/summaryTest.json")

    trainTitleFile = open("train_data/data_processed/titleTrain.json", "a")
    devTitleFile = open("train_data/data_processed/titleDev.json", "a")
    testTitleFile = open("train_data/data_processed/titleTest.json", "a")
    trainSummaryFile = open("train_data/data_processed/summaryTrain.json", "a")
    devSummaryFile = open("train_data/data_processed/summaryDev.json", "a")
    testSummaryFile = open("train_data/data_processed/summaryTest.json", "a")

    processDataWithLabel(trainTitleFile, titleKeywordsSetTrain)
    processDataWithLabel(trainSummaryFile, SummaryKeywordsSetTrain)
    processDataWithLabel(devTitleFile, titleKeywordsSetDev)
    processDataWithLabel(devSummaryFile, SummaryKeywordsSetDev)
    processDataWithoutLabel(testTitleFile, titleKeywordsSetTest)
    processDataWithoutLabel(testSummaryFile, SummaryKeywordsSetTest)
