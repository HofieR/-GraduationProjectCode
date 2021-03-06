import json

from torchtext.legacy.data import Field
from torchtext.legacy import data
from tqdm import tqdm


# 读取文件
def readAndProcess(path):
    list_data = []
    with open(path, encoding='UTF-8') as F:
        for line in F:
            try:
                line = json.loads(line)
            except ValueError:
                continue
            text = line['text']
            if not line.get('label'):
                text = list(text)
                label = len(text) * ['O']
            else:
                label = line['label']
                text, label = transformSample(text, label)
            list_data.append((text, label))
    return list_data


class MyDataset(data.Dataset):
    def __init__(self, datatuple, text_field, label_field, test=False):  # datatuple指的是元组('this moive is great',1)
        fields = [("text", text_field), ("label", label_field)]
        lists = []
        if test:
            # 如果为测试集，则不加载label
            for content, label in tqdm(datatuple):
                lists.append(data.Example.fromlist([content, None], fields))
        else:
            for content, label in tqdm(datatuple):
                # Example: Defines a single training or test example.Stores each column of the example as an attribute.
                lists.append(data.Example.fromlist([content, label], fields))
        # 之前是一些预处理操作，此处调用super初始化父类，构造自定义的Dataset类
        super().__init__(lists, fields)


def transformSample(text, label):
    text = list(text)
    count = len(text)
    processed_label = ['O'] * count
    for key, value in label.items():
        label_indexes = value.values()
        # start_idx: 实体开始索引
        # end_idx: 实体结束索引
        for label_index in label_indexes:
            for start_idx, end_idx in label_index:

                if start_idx == end_idx:
                    processed_label[start_idx] = 'S-' + key

                elif start_idx + 1 == end_idx:
                    processed_label[start_idx:end_idx + 1] = ['B-' + key, 'E-' + key]

                elif end_idx - start_idx > 1:
                    new_labels = ['B-' + key] + ['I-' + key] * (end_idx - start_idx - 1) + ['E-' + key]
                    processed_label[start_idx:end_idx + 1] = new_labels

    return text, processed_label


def createDataset(data_list, config, is_train=True):
    if is_train:
        SRC = Field(tokenize=lambda x: x, fix_length=config.fix_length)
        LABEL = Field(tokenize=lambda x: x, fix_length=config.fix_length)  # 针对文本分类的类别标签
        config.SRC = SRC
        config.LABEL = LABEL
    else:
        SRC = config.SRC
        LABEL = config.LABEL

    return MyDataset(data_list, SRC, LABEL), SRC, LABEL


def builtIter(dataset, config):
    return data.BucketIterator(dataset=dataset, batch_size=config.batch_size,
                               shuffle=True, sort_key=lambda x: len(x.text), sort_within_batch=False, repeat=False,device=config.device)


def createDataloader(config):
    train_data_list = readAndProcess(config.train_path)
    dev_data_list = readAndProcess(config.dev_path)
    test_data_list = readAndProcess(config.test_path)

    SRC = Field(tokenize=lambda x: x, fix_length=config.fix_length)
    LABEL = Field(tokenize=lambda x: x, fix_length=config.fix_length)

    train_dataset = MyDataset(train_data_list, SRC, LABEL)
    dev_dataset = MyDataset(dev_data_list, SRC, LABEL)
    test_dataset = MyDataset(test_data_list, SRC, LABEL)

    SRC.build_vocab(train_dataset, )
    LABEL.build_vocab(train_dataset)

    LABEL.vocab.stoi.pop('<unk>')
    LABEL.vocab.stoi[LABEL.vocab.itos[-1]] = 0
    LABEL.vocab.itos = sorted(LABEL.vocab.stoi, key=lambda x: LABEL.vocab.stoi[x])

    config.SRC = SRC
    config.LABEL = LABEL

    train_iter, dev_iter, test_iter = map(builtIter,
                                          [train_dataset, dev_dataset, test_dataset], [config] * 3)

    return train_iter, dev_iter, test_iter