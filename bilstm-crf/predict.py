from operator import itemgetter
from model import BilstmCrf
from config import Config

import torch
import dill


def predictSingle(model, SRC, LABEL, inputs):
    model.eval()
    res = itemgetter(*inputs)(SRC.vocab.stoi)
    res = torch.tensor(res).unsqueeze(0)
    device = torch.device('cuda:0')
    res = res.to(device)
    answers = model.decode(res)

    extracted_entities = extract(answers[0], LABEL.vocab.itos)
    L = []
    for extracted_entity in extracted_entities:
        start_index = int(extracted_entity['start_index'])
        end_index = int(extracted_entity['end_index']) + 1
        entity = {'content': inputs[start_index: end_index], 'label': extracted_entity['name']}
        L.append(entity)

    return L, inputs


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


if __name__ == '__main__':
    config = Config()
    with open(config.pkl_path, 'rb') as F:
        src_label = dill.load(F)

    config.SRC = src_label['src']
    config.LABEL = src_label['label']
    model = BilstmCrf(config).to(config.device)
    model.load_state_dict(torch.load(config.model_path))
    inputs = "元数据管理"

    res = predictSingle(model, config.SRC, config.LABEL, inputs)
    print(res)