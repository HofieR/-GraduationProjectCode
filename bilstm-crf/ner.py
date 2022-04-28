import os
import re
from operator import itemgetter
from model import BilstmCrf
from config import Config
from xlrd import open_workbook

import torch
import dill


# {"id": 0, "text": "信息技术 用能单位能耗在线监测系统 第1部分：端设备数据传输接口", "keyword": ["信息技术", "数据传输接口"]}
def outputResult(idx, text, keywords, jsonFile):
    if len(keywords) == 0:
        return
    line = "{\"id\": " + str(idx) + ", \"text\": \"" + text + "\", \"keyword\": ["
    tmp = 0
    for keyword in keywords:
        if tmp != 0:
            line = line + ", "
        line = line + "\"" + keyword + "\""
        tmp = tmp + 1
    line = line + "]}\n"
    jsonFile.write(line)


def nerSingle(model, SRC, LABEL, text, jsonFile, idx):
    model.eval()
    res = itemgetter(*text)(SRC.vocab.stoi)
    res = torch.tensor(res).unsqueeze(0)
    device = torch.device('cuda:0')
    res = res.to(device)
    answers = model.decode(res)

    extracted_entities = extract(answers[0], LABEL.vocab.itos)
    keywords = []
    for extracted_entity in extracted_entities:
        start_index = int(extracted_entity['start_index'])
        end_index = int(extracted_entity['end_index']) + 1
        keywords.append(text[start_index: end_index])

    outputResult(idx, text, keywords, jsonFile)
    return


def extract(answer, idx_to_label):
    answer = itemgetter(*answer)(idx_to_label)
    extracted_entities = []
    current_entity = None
    for index, label in enumerate(answer):
        if label in ['O', '<pad>']:
            if current_entity:
                current_entity = None
                continue
            else:
                continue
        else:
            # position  B I E S
            position, entity_type = label.split('-')
            if current_entity:
                if entity_type == current_entity['name']:
                    if position == 'S':
                        extracted_entities.append({
                            'name': entity_type, 'start_index': index, 'end_index': index
                        })
                        current_entity = None
                    elif position == 'I':
                        continue
                    elif position == 'B':
                        current_entity = {
                            'name': entity_type, 'start_index': index, 'end_index': None
                        }
                        continue
                    else:
                        current_entity['end_index'] = index
                        extracted_entities.append(current_entity)
                        current_entity = None
                else:
                    if position == 'S':
                        extracted_entities.append({
                            'name': entity_type, 'start_index': index, 'end_index': index
                        })
                        current_entity = None
                    if position == 'B':
                        current_entity = {
                            'name': entity_type, 'start_index': index, 'end_index': None
                        }
            else:
                if position == 'S':
                    extracted_entities.append({
                        'name': entity_type, 'start_index': index, 'end_index': index
                    })
                    current_entity = None
                if position == 'B':
                    current_entity = {
                        'name': entity_type, 'start_index': index, 'end_index': None
                    }
    return extracted_entities


def readData(fileLoc):
    dataXls = open_workbook(fileLoc)
    dataSheet = dataXls.sheet_by_index(0)
    data = dataSheet.col_values(0)
    return data


def main():
    os.remove("input/target/standardKeywords.json")
    stdKwdJsonFile = open("input/target/standardKeywords.json", "a")
    texts = readData("input/target/patent.xls")

    config = Config()
    with open(config.pkl_path, 'rb') as F:
        src_label = dill.load(F)

    config.SRC = src_label['src']
    config.LABEL = src_label['label']
    model = BilstmCrf(config).to(config.device)
    model.load_state_dict(torch.load(config.model_path))

    for i in range(len(texts)):
        if i % 100 == 0 and i != 0:
            print("current id is " + str(i))
        try:
            # nerSingle(model, config.SRC, config.LABEL, texts[i], stdKwdJsonFile, i + 1)
            text = texts[i]
            splitText = re.split("[；，。]", text)
            for sentence in splitText:
                if 5 < len(sentence) < 50:
                    nerSingle(model, config.SRC, config.LABEL, sentence, stdKwdJsonFile, i + 1)
        except TypeError:
            print("TypeErrorID: " + str(i))
            continue
        except ValueError:
            print("ValueErrorID: " + str(i))
            continue
        except RuntimeError:
            print("RuntimeErrorID: " + str(i))
            continue

    stdKwdJsonFile.close()


if __name__ == '__main__':
    main()
