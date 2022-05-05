from gensim.summarization import bm25


def getMaxIds(scores):
    scoreDic = {}
    for i in range(len(scores)):
        scoreDic[i] = scores[i]
    scoreDic = sorted(scoreDic.items(), key=lambda k: k[1], reverse=True)
    rst = []
    for i in range(len(scoreDic[0:5])):
        if scoreDic[i][1] != 0:
            rst.append(scoreDic[i])
    return rst




def splitList(inputs):
    rst = []
    for input in inputs:
        rst.append(input.strip().split(" "))
    return rst


def main():
    standardFile = open("data/split/standard.txt", "r", encoding="UTF-8")
    patentFile = open("data/split/patent.txt", "r", encoding="UTF-8")

    standards = standardFile.read().split("\n")
    patents = patentFile.read().split("\n")

    standardsList = splitList(standards)
    patentsList = splitList(patents)

    curPatent = patentsList[100]
    bm25Model = bm25.BM25(standardsList)
    scores = bm25Model.get_scores(curPatent)
    maxIds = getMaxIds(scores)
    print("patent keywords are: \n" + str(curPatent) + "\n")
    print("standards keywords are: ")
    for maxId in maxIds:
        print(str(standardsList[maxId[0]]) + "\n")

if __name__ == "__main__":
    main()

