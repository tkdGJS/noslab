import torch
import numpy as np
import collections
from typing import OrderedDict
import Uniform as U
import timm
import torch.nn as nn
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)

path = './fio_test/covid-checkpoint' 
checkpoint = torch.load(path + '/covid_checkpoint3.pt',
        map_location=torch.device('cpu'))

model_state = checkpoint['optimizer_state_dict']


all_values = []

#model.state_dict()의 디렉토리 구조를 탐색하며 모든 요소를 리스트에 넣는 과정
#for tensor in model_state.values():
#    
#    #모델 파라미터의 다차원 구조를 직렬화
#    flat = tensor.flatten().tolist()
#
#    #직렬화한 flat에서 float만 추출
#    flat_float = [getfloat for getfloat in flat if isinstance(getfloat,float)]
#    all_values.extend(flat_float)

#Uniform = U.UniformModel(model_state, 8)
#test2 = Uniform.Quantization(model_state, 8)
#test3 = Uniform.De_Quantization(test2, 8)
#print(test3)
#print(len(all_values))
class Model(nn.Module):
    def __init__(self, model_name, pretrained = True, num_classes = 3):
        super().__init__()
        self.model_name = model_name
        self.cnn = timm.create_model(self.model_name, pretrained = pretrained, num_classes = num_classes)

    def forward(self, x):
        x = self.cnn(x)
        return x

model_resNet50 = Model('resnet50', pretrained = True, num_classes = 3)
optimizer = torch.optim.Adam(model_resNet50.parameters(),lr = 1e-4)

print(model_state)
print(optimizer)

#test = Uniform.Quantization(model_state, 8)
#test2 = Uniform.De_Quantization(test,8)
#print(test2)









