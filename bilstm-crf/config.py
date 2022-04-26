import torch

feaStr = ["summary", "title", "native"]


class Config:
    def __init__(self):
        self.SRC = None
        self.LABEL = None

        self.train_path = 'input/train/' + feaStr[1] + 'Train.json'
        self.dev_path = 'input/train/' + feaStr[1] + 'Dev.json'
        self.test_path = 'input/train/' + feaStr[1] + 'Test.json'
        self.model_path = 'model/' + feaStr[1] + '.h5'
        self.pkl_path = 'model/' + feaStr[1] + '.pkl'

        self.fix_length = 50
        self.batch_size = 100
        self.embedding_dim = 768

        self.hid_dim = 300
        self.n_layers = 2
        self.dropout = 0.1

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.epochs = 30
        self.lr = 0.00005
        self.momentum = 0.95
