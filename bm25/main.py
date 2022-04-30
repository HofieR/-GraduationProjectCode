import ReadData
import jieba

from gensim.summarization import bm25

standards = ReadData.readStandard("data/standard.xls")
patents = ReadData.readPatent("data/patent_ner_train_by_summary.json")
splitStandardsList = []
for standard in standards:
    data = jieba.lcut(standard, cut_all=False)
    splitStandardsList.append(list(data))

testData = patents[5]
print(testData)
bm25Model = bm25.BM25(splitStandardsList)
scores = bm25Model.get_scores(testData)
for i in range(len(scores)):
    if scores[i] > 0:
        print(splitStandardsList[i])

