import re
import json
from xlrd import open_workbook


def extractStandard(standardsList, outputFile):
    for standard in standardsList:
        standard = re.sub(r"-", "", standard)
        standard = re.sub(r":", "", standard)
        standard = re.sub(r"：", "", standard)
        standard = re.sub(r"第.*部分", "", standard)
        standard = re.sub(r"\s+", " ", standard)
        if standard != "":
            outputFile.write(standard + "\n")


def processStandard(inputFile, outputFile):
    standardXls = open_workbook(inputFile)
    standardSheet = standardXls.sheet_by_index(0)
    extractStandard(standardSheet.col_values(1), outputFile)


def extractPatent(keywordsList):
    res = []
    for keyword in keywordsList:
        if "、" not in keyword:
            res.append(keyword)
    return res


def processPatent(inputFile, outputFile):
    idKeywordsDict = {}
    with open(inputFile, encoding='UTF-8') as F:
        for line in F:
            try:
                line = json.loads(line)
            except ValueError:
                continue
            id = line["id"]
            tmpKeywordsSet = set(line["keyword"])
            tmpKeywordsList = list(tmpKeywordsSet)
            tmpKeywordsList = extractPatent(tmpKeywordsList)
            if len(tmpKeywordsList) == 0:
                continue
            if id not in idKeywordsDict.keys():
                idKeywordsDict[id] = tmpKeywordsList
            else:
                oldKeywordsList = idKeywordsDict[id]
                oldKeywordsList.extend(tmpKeywordsList)
                curKeywordsSet = set(oldKeywordsList)
                curKeywordsList = list(curKeywordsSet)
                idKeywordsDict[id] = curKeywordsList
    for id in idKeywordsDict.keys():
        keywords = idKeywordsDict.get(id)
        for keyword in keywords:
            outputFile.write(keyword + " ")
        outputFile.write("\n")


def main():
    standardOutputFile = open("data/output/standard.txt", "w", encoding="UTF-8")
    patentOutputFile = open("data/output/patent.txt", "w", encoding="UTF-8")
    processStandard("data/input/standard.xls", standardOutputFile)
    processPatent("data/input/patent.json", patentOutputFile)


if __name__ == "__main__":
    main()