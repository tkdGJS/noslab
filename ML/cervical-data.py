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
from PIL import Image

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


#print(train_paths[:])

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

#print(dataset[1][0])

train_set, test_set = train_test_split(dataset, test_size = 0.3, random_state= 42)

train_loader = torch.utils.data.DataLoader(train_set, batch_size=BATCH_SIZE)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=BATCH_SIZE)

train_iter = iter(train_loader)
batch_data, batch_labels = next(train_iter)

# 미니배치의 형태 확인
print(batch_data[0]*255)
#print(batch_labels)
#

pil_image = Image.fromarray((batch_data[0]*255))
