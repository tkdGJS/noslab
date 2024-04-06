import torch
import os
from torch.multiprocessing import Pool, Process, set_start_method, Manager, Value, Lock
import Uniform as U

if __name__ == '__main__':
    import numpy as np 
    import random
    import copy
    import torch.nn as nn
    import torch.nn.functional as F
    import torchvision
    import torchvision.transforms as tt
    import torchvision.models as models
    from torchvision.datasets import ImageFolder
    #from torchvision.utils import make_grid
    from torch.utils.data import random_split, DataLoader
    from sklearn.model_selection import train_test_split
    import time
    import timm
    import threading
    import snapshot_storing_n as ss
try:
    set_start_method('spawn')
except RuntimeError:
    pass
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
lock = Lock()

if __name__ == '__main__':


    class Model(nn.Module):
        def __init__(self, model_name, pretrained = True, num_classes = 3):
            super().__init__()
            self.model_name = model_name
            self.cnn = timm.create_model(self.model_name, pretrained = pretrained, num_classes = num_classes)

        def forward(self, x):
            x = self.cnn(x)
            return x
    script_start = time.time()
    print(os.getpid())

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(device)

    epochs = 30
    BATCH_SIZE = 24
    OUTPUT_PATH = './fio_test/covid-checkpoint/'



    data_dir = "./data/covid/chest_xray/chest_xray/"

    classes = os.listdir(data_dir + "/train")

    pneumonia_files = os.listdir(data_dir + "/train/PNEUMONIA")

    normal_files = os.listdir(data_dir + "/train/NORMAL")

    dataset = ImageFolder(data_dir+'/train', 
                          transform=tt.Compose([tt.Resize(255),
                                                tt.CenterCrop(224),
                                                tt.RandomHorizontalFlip(),
                                                tt.RandomRotation(10),
                                                tt.RandomGrayscale(),
                                                tt.RandomAffine(translate=(0.05,0.05), degrees=0),
                                                tt.ToTensor()
                                                #tt.Normalize(mean=[0.485, 0.456, 0.406], 
                                                #std=[0.229, 0.224, 0.225] ,inplace=True)
                                               ]))

    train_set, test_set = train_test_split(dataset, test_size = 0.3, random_state= 42)

    train_loader = torch.utils.data.DataLoader(train_set, batch_size=BATCH_SIZE)
    test_loader = torch.utils.data.DataLoader(test_set, batch_size=BATCH_SIZE)

    train_iter = iter(train_loader)
    batch_data, batch_labels = next(train_iter)

    model_resNet50 = Model('resnet50', pretrained = True, num_classes = 3)
    model_resnet50 = model_resNet50.to(device)

    criterion = nn.CrossEntropyLoss().to(device)
    optimizer = torch.optim.Adam(model_resNet50.parameters(),lr = 1e-4)


    checkpoint_list = []
    epoch_list = []
    start_model_time = time.time()
    
    #GPU index, single = 0
    gpu = 0
    cost = 0
    print("training start" + str(start_model_time - script_start ))
    manager = Manager()
    activate_snapshot = manager.Value('i', 0)

def main():
    for epoch in range(epochs):
        avg_cost = 0
        start_epoch_time = time.time()
        for idx, (data, target) in enumerate(train_loader):
    #        data, target 
            if  idx == 0:
                data = data.float().to(device)
                target = target.to(device)
                optimizer.zero_grad()
                hypothesis = model_resNet50(data)
                cost = criterion(hypothesis, target)
                cost.backward()
                optimizer.step()
                avg_cost += cost / len(train_loader)
                model_state = model_resNet50.state_dict()
                op_state = optimizer.state_dict()
                
                start_checkpoint_time = time.time()
                save = ss.async_checkpointing(model_state, epoch)

                fn = globals()["Process"]
                
                P = fn(target=save.snapshot_storing, args=(model_state, op_state, epoch))
                P.start()

#                time.sleep(10)

                end_checkpoint_time = time.time()
                print("check"+str(end_checkpoint_time - script_start))
                checkpoint_delta = np.round(end_checkpoint_time - start_checkpoint_time, 5)
                checkpoint_list.append(checkpoint_delta)
            else:
                data = data.float().to(device)
                target = target.to(device)
                optimizer.zero_grad()
                hypothesis = model_resNet50(data)
                cost = criterion(hypothesis, target)
                cost.backward()
                optimizer.step()
                avg_cost += cost / len(train_loader)


    print('[Epoch: {:>4}) cost = {:>.9}'.format(epoch +1, avg_cost))
    end_epoch_time = time.time()
    print("epoch"+str(end_epoch_time - script_start))
    epoch_delta = np.round(end_epoch_time - start_epoch_time, 5)
    epoch_list.append(epoch_delta)


if __name__ == '__main__':
    main()
    end_model_time = time.time()
    model_delta = np.round(end_model_time - start_model_time, 5)
    print(script_start - start_model_time)
    #model_resNet50.eval()
    #with torch.no_grad():
    #    correct = 0
    #    total = 0
    #
    #    for data, target in test_loader:
    #        data = data.float().to(device)
    #        target = target.to(device)
    #        out = model_resNet50(data)
    #        preds = torch.max(out, 1)[1]
    #        total += len(target)
    #        correct += (preds==target).sum().item()
    #
    #print('Test Accuracy: ', 100.*correct/total, '%')
    print(model_delta)
    print(epoch_list)
    print(checkpoint_list)
