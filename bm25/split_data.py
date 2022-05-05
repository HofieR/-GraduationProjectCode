import jieba
import re


def getStopwordsList():
    stopwords = [line.strip() for line in open('./data/stopwords.txt', encoding='UTF-8').readlines()]
    return stopwords


def splitSentence(sentence):
    sentence_depart = jieba.lcut(sentence.strip(), cut_all=False)
    stopwords = getStopwordsList()
    out = ''
    for word in sentence_depart:
        if word not in stopwords and word != " " and re.match("[\u4e00-\u9fa5]+", word):
            out += word
            out += " "
    return out


def main():
    standardFile = open("data/output/standard.txt", "r", encoding="UTF-8")
    patentFile = open("data/output/patent.txt", "r", encoding="UTF-8")
    splitStandardFile = open("data/split/standard.txt", "w", encoding="UTF-8")
    splitPatentFile = open("data/split/patent.txt", "w", encoding="UTF-8")
    standards = standardFile.read().split("\n")
    patents = patentFile.read().split("\n")
    print("start split standard\n")
    for standard in standards:
        splitStandardFile.write(splitSentence(standard) + "\n")
    print("start split patent\n")
    for patent in patents:
        splitPatentFile.write(splitSentence(patent) + "\n")


if __name__ == "__main__":
    main()