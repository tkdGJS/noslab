import torch
from torch.utils.data import Dataset,DataLoader
from torchvision import datasets, models, transforms
from torch import nn
from torch.optim import AdamW,Adam
import numpy as np
import os
import glob
#import albumentations as A
#from albumentations.pytorch import ToTensorV2
import cv2
import gc
#import torchmetrics 
import timm
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import pandas as pd
import torch.profiler
import time
from tqdm import tqdm
import Uniform as U
import copy

data_path = "./data/cervical/kaggle/train/train"
images  =  [glob.glob(os.path.join(data_path, d, "*.*")) for d in os.listdir(data_path)]
train_paths = np.hstack(images)
# Additional data
extra_1 = "./data/cervical/kaggle/additional_Type_1_v2"
extra_2 = "./data/cervical/kaggle/additional_Type_2_v2"
extra_3 = "./data/cervical/kaggle/additional_Type_3_v2"
images1  =  [glob.glob(os.path.join(extra_1, d, "*.*")) for d in os.listdir(extra_1)]
images2  =  [glob.glob(os.path.join(extra_2, d, "*.*")) for d in os.listdir(extra_2)]
images3  =  [glob.glob(os.path.join(extra_3, d, "*.*")) for d in os.listdir(extra_3)]
train_paths = np.append(train_paths, np.hstack(images1))
train_paths = np.append(train_paths, np.hstack(images2))
train_paths = np.append(train_paths, np.hstack(images3))

print(f'In this train set we have got a total of {len(train_paths)}')
epochs = 30
#OUTPUT_PATH = './checkpoint/cervical/cervical_epoch120/'

OUTPUT_PATH = './fio_test/cervical-checkpoint/'
BATCH_SIZE = 24
# detect and define device 
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)


print(train_paths[:])

def transform(image):
    image -= image.min()
    image = image/image.max()
    return image

class MyDataset(Dataset):

    def __init__(self, paths, transform=None, train=True, size=224):
        self.paths = paths
        self.transform = transform
        self.train = train
        self.size = size
    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        path = self.paths[idx]
        label = path.split("/")[-2].split("_")[-1]
        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = np.transpose(image, (2,0,1))
        image = transform(image) 
        return image, int(label)-1




dataset = MyDataset(train_paths)

print(dataset[1][0])

train_set, test_set = train_test_split(dataset, test_size = 0.3, random_state= 42)

train_loader = torch.utils.data.DataLoader(train_set, batch_size=BATCH_SIZE)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=BATCH_SIZE)

train_iter = iter(train_loader)
batch_data, batch_labels = next(train_iter)

# 미니배치의 형태 확인
print(batch_data.shape)
print(batch_labels)
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

            model_state = copy.deepcopy(model_resNet50.state_dict())
            optimizer_state = copy.deepcopy(optimizer.state_dict())

            Uniform1 = U.UniformModel(model_state, 8)
            test = Uniform1.Quantization(model_state, 8)

            Uniform2 = U.UniformOptimizer(optimizer_state, 8)
            test2 = Uniform2.Quantization(optimizer_state,8)



            start_checkpoint_time = time.time()
            PATH = OUTPUT_PATH +  "cervical_checkpoint" +str(epoch+1) + ".pt"
            a = torch.save({
                'inputs' : data,
                'epoch' : epoch + 1,
                'model_state_dict' : test,
                'optimizer_state_dict' : test2,
                'loss' : cost 
            }, PATH)
            a

            end_checkpoint_time = time.time()
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
    epoch_delta = np.round(end_epoch_time - start_epoch_time, 5)
    epoch_list.append(epoch_delta)
end_model_time = time.time()
model_delta = np.round(end_model_time - start_model_time, 5)
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
    













