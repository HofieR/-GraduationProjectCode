from copy import deepcopy
from collections import defaultdict
import pandas as pd
from config import *
from utils import *
from train import *

config = Config()
train_iter, dev_iter, test_iter = create_dataloader(config)
model = create_model(config)
# model.load_state_dict(torch.load('../input/knowledeg-graph-ner-model/bilstm_crf.h5'))
model.load_state_dict(torch.load('./bilstm_crf.h5'))


def compute_f1(df):
    df['p'] = df['tp']/(df['pred']+1)
    df['r'] = df['tp']/(df['real']+1)
    df['f1'] = 2*df['p']*df['r']/(df['p']+df['r'])


def test(model, test_iter, config):
    acc, matrix = eval(model, test_iter, True)
    map = create_entity_to_index(config)
    df_index = list(map) + ['total']
    df = pd.DataFrame(index=df_index, columns=['tp', 'pred', 'real', 'p', 'r', 'f1'])
    df = df.fillna(0)

    for col_index, col_name in enumerate(['tp', 'pred', 'real']):
        for row_name in df_index:
            for row_index in map[row_name]:
                df[col_name][row_name] += matrix[row_index, col_index]
                df[col_name]['total'] += matrix[row_index, col_index]

    compute_f1(df)
    return acc, df


def create_entity_to_index(config):
    itos = deepcopy(config.LABEL.vocab.itos)
    entities = set([name.split('-')[-1] for name in itos])
    map = defaultdict(list)
    for entity in entities:
        for label,index in config.LABEL.vocab.stoi.items():
            if entity in label:
                map[entity].append(index)
    return map


acc, df = test(model, dev_iter, config)