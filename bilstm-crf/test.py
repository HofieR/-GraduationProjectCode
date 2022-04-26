from copy import deepcopy
from collections import defaultdict
import pandas as pd
from config import *
from utils import *
from train import *


def computeF1(df):
    df['p'] = df['tp']/(df['pred']+1)
    df['r'] = df['tp']/(df['real']+1)
    df['f1'] = 2*df['p']*df['r']/(df['p']+df['r'])


def test(model, test_iter, config):
    acc, matrix = eval(model, test_iter, True)
    map = createEntityToIndex(config)
    df_index = list(map) + ['total']
    df = pd.DataFrame(index=df_index, columns=['tp', 'pred', 'real', 'p', 'r', 'f1'])
    df = df.fillna(0)

    for col_index, col_name in enumerate(['tp', 'pred', 'real']):
        for row_name in df_index:
            for row_index in map[row_name]:
                df[col_name][row_name] += matrix[row_index, col_index]
                df[col_name]['total'] += matrix[row_index, col_index]

    computeF1(df)
    return acc, df


def createEntityToIndex(config):
    itos = deepcopy(config.LABEL.vocab.itos)
    entities = set([name.split('-')[-1] for name in itos])
    map = defaultdict(list)
    for entity in entities:
        for label,index in config.LABEL.vocab.stoi.items():
            if entity in label:
                map[entity].append(index)
    return map


if __name__ == '__main__':
    config = Config()
    train_iter, dev_iter, test_iter = createDataloader(config)
    model = createModel(config)
    model.load_state_dict(torch.load(config.model_path))
    acc, df = test(model, dev_iter, config)
    print(df)