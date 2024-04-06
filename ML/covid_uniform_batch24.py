import numpy as np 
import random
import copy
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as tt
import torchvision.models as models
from torchvision.datasets import ImageFolder
from torchvision.utils import make_grid
from torch.utils.data import random_split, DataLoader
from sklearn.model_selection import train_test_split
import os
import time
import timm
import Uniform as U
#from pytorch_forecasting.utils import move_to_device
import threading
import multiprocessing as mp
import snapshot_storing as ss
try:
    mp.set_start_method('spawn')
except RuntimeError:
    pass

script_start = time.time()
print(os.getpid())

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)

epochs = 5
BATCH_SIZE = 8
OUTPUT_PATH = './fio_test/covid-checkpoint/'



data_dir = "./data/covid/chest_xray/chest_xray/"

#print(os.listdir(data_dir))
classes = os.listdir(data_dir + "/train")
#print(classes)

pneumonia_files = os.listdir(data_dir + "/train/PNEUMONIA")
#print('No. of training examples for Pneumonia:', len(pneumonia_files))
#print(pneumonia_files[:5])

normal_files = os.listdir(data_dir + "/train/NORMAL")
#print('No. of training examples for Normal:', len(normal_files))
#print(normal_files[:5])

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

#dataset
#img, label = dataset[0]
#print(img.shape, label)
#print(img)


train_set, test_set = train_test_split(dataset, test_size = 0.3, random_state= 42)

train_loader = torch.utils.data.DataLoader(train_set, batch_size=BATCH_SIZE)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=BATCH_SIZE)

train_iter = iter(train_loader)
batch_data, batch_labels = next(train_iter)

# 미니배치의 형태 확인
#print(batch_data.shape)
#print(batch_labels)
#



class Model(nn.Module):
    def __init__(self, model_name, pretrained = True, num_classes = 3):
        super().__init__()
        self.model_name = model_name
        self.cnn = timm.create_model(self.model_name, pretrained = pretrained, num_classes = num_classes)

    def forward(self, x):
        x = self.cnn(x)
        return x




model_resNet50 = Model('resnet50', pretrained = True, num_classes = 3)
model_resnet50 = model_resNet50.to(device)

criterion = nn.CrossEntropyLoss().to(device)
optimizer = torch.optim.Adam(model_resNet50.parameters(),lr = 1e-4)


checkpoint_list = []
epoch_list = []
start_model_time = time.time()

cost = 0
print("training start" + str(start_model_time - script_start ))
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
#            print(model_state)

            #ss = snapshot_storing.snapshot_storing(model_state, epoch)

            start_checkpoint_time = time.time()
#            ss = snapshot_storing.async_checkpointing(model_state, epoch)
#            ss.mpstart(model_state, epoch)

#            time.sleep(10)
            save = ss.async_checkpointing(model_state, epoch)
#            ss.mpstart(model_state, epoch)


#            save.snapshot_storing(model_state, epoch)

#            if __name__ == '__main__':
            P = mp.Process(target=save.snapshot_storing, args=(model_state, epoch))
            P.start()
            P.join()
            time.sleep(10)

#            snapshot_storing.mpstart(model_state)

#            Process.start()
#            Process.join()
#            model_state = model_resNet50.state_dict()
##            optimizer_state = optimizer.state_dict()
#            for i, j in model_state.items():
#                model_state[i] = j.cpu()
##            for i, j in optimizer_state.items():
##                optimizer_state[i] = move_to_device(j, 'cpu')
##            model_state = copy.deepcopy(model_resNet50.state_dict())
##            optimizer_state = copy.deepcopy(optimizer.state_dict())
#

#            Uniform1 = U.UniformModel(model_state, 8)
#            test = Uniform1.Quantization(model_state, 8)
##            assert False
#
##            Uniform2 = U.UniformOptimizer(optimizer_state, 8)
##            test2 = Uniform2.Quantization(optimizer_state,8)


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
    
