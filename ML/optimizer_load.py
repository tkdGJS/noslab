import torch
import numpy as np
import collections
from typing import OrderedDict
import Uniform as U

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)

checkpoint = torch.load('./cervical_checkpoint1.pt',
        map_location=torch.device('cpu'))

optimizer_state = checkpoint['optimizer_state_dict']
model_state = checkpoint['model_state_dict']

def _to_cpu(ele, snapshot=None):
    #while True:
    if snapshot is None:
        snapshot = {}
    if hasattr(ele, 'cpu'):
        snapshot = ele.cpu()
    elif isinstance(ele, dict):
        snapshot = {}
        for k,v in ele.items():
            snapshot[k] = None
            snapshot[k] = _to_cpu(v, snapshot[k])
    elif isinstance(ele, list):
        snapshot  = [None for _ in range(len(ele))]
        for idx, v in enumerate(ele):
            snapshot[idx] = _to_cpu(v, snapshot[idx])

    return snapshot

a = _to_cpu(model_state)
Uniform2 = U.UniformModel(a, 8)
test2 = Uniform2.Quantization(a, 8)
#print(a)
#print(model_state)
print(test2)
#print(_to_cpu(model_state['param_groups'][0]))
