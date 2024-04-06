import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import copy
import os
import torch
from torch.utils.data import Dataset
import torchvision.transforms as transforms
from torch.utils.data import random_split
from torch.optim.lr_scheduler import ReduceLROnPlateau
import torch.nn as nn
from torchvision import utils
import torchvision.transforms as transforms
from PIL import Image
import timm
import time

labels_df = pd.read_csv('./data/lymph/train_labels.csv')

os.listdir('./data/lymph/')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)

labels_df[labels_df.duplicated(keep=False)]


labels_df.shape
labels_df['label'].value_counts()

imgpath ="./data/lymph/train/" # training data is stored in this folder
malignant = labels_df.loc[labels_df['label']==1]['id'].values    # get the ids of malignant cases
normal = labels_df.loc[labels_df['label']==0]['id'].values       # get the ids of the normal cases

class pytorch_data(Dataset):
    
    def __init__(self,data_dir,transform,data_type="train"):      
    
        # Get Image File Names
        cdm_data=os.path.join(data_dir,data_type)  # directory of files
        
        file_names = os.listdir(cdm_data) # get list of images in that directory  
        idx_choose = np.random.choice(np.arange(len(file_names)), 
                                      20000,
                                      replace=False).tolist()
        file_names_sample = [file_names[x] for x in idx_choose]
        self.full_filenames = [os.path.join(cdm_data, f) for f in file_names_sample]   # get the full path to images
        
        # Get Labels
        labels_data=os.path.join(data_dir,"train_labels.csv") 
        labels_df=pd.read_csv(labels_data)
        labels_df.set_index("id", inplace=True) # set data frame index to id
        self.labels = [labels_df.loc[filename[:-4]].values[0] for filename in file_names_sample]  # obtained labels from df
        self.transform = transform
      
    def __len__(self):
        return len(self.full_filenames) # size of dataset

    def __getitem__(self, idx):
        image = Image.open(self.full_filenames[idx]) 
        # open image, apply transforms and return with label
        image = self.transform(image) # Apply Specific Transformation to Image
        return image, self.labels[idx]
    
data_transformer = transforms.Compose([transforms.ToTensor(),
                                       transforms.Resize((224,224))])

data_dir = './data/lymph/'
img_dataset = pytorch_data(data_dir, data_transformer, "train") # Histopathalogic images

# load an example tensor
img,label=img_dataset[10]
print(img.shape,torch.min(img),torch.max(img))

len_img=len(img_dataset)
len_train=int(0.8*len_img)
len_val=len_img-len_train

# Split Pytorch tensor
train_set,test_set=random_split(img_dataset,
                             [len_train,len_val]) # random split 80/20

print("train dataset size:", len(train_set))
print("validation dataset size:", len(test_set))

print(img.shape)

BATCH_SIZE = 24
epochs = 30
OUTPUT_PATH = './fio_test/lymph-checkpoint/'

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

            start_checkpoint_time = time.time()
            PATH = OUTPUT_PATH +  "lymph_checkpoint" +str(epoch+1) + ".pt"
            a = torch.save({
                'inputs' : data,
                'epoch' : epoch + 1,
                'model_state_dict' : model_resNet50.state_dict(),
                'optimizer_state_dict' : optimizer.state_dict(),
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
    
