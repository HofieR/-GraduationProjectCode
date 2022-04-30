import re
import json
from xlrd import open_workbook


def extractStandard(standardsList):
    newStandardsList = []
    for standard in standardsList:
        standard = re.sub(r"-", "", standard)
        standard = re.sub(r":", "", standard)
        standard = re.sub(r"：", "", standard)
        standard = re.sub(r"第.*部分", "", standard)
        standard = re.sub(r"\s+", ",", standard)
        newStandardsList.append(standard)
    return newStandardsList


def readStandard(filePath):
    standardXls = open_workbook(filePath)
    standardSheet = standardXls.sheet_by_index(0)
    return extractStandard(standardSheet.col_values(1))


def extractPatent(keywordsList):
    res = []
    for keyword in keywordsList:
        if "、" not in keyword:
            res.append(keyword)
    return res


def readPatent(filePath):
    idKeywordsDict = {}
    with open(filePath, encoding='UTF-8') as F:
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
    return idKeywordsDict
