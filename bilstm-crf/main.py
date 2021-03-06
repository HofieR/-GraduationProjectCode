from config import *
from utils import *
from train import *
import dill

config = Config()
train_iter, dev_iter, test_iter = createDataloader(config)
model = createModel(config)
src_label = {'label': config.LABEL, 'src': config.SRC}
with open(config.pkl_path, 'wb') as f:
    dill.dump(src_label, f)

epochs = config.epochs
optimizer = torch.optim.SGD(model.parameters(), lr=config.lr, momentum=config.momentum)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.9)
train(model, train_iter, dev_iter, optimizer, epochs, scheduler)