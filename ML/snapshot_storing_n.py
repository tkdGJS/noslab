import torch
from torch.multiprocessing import Pool, Process, set_start_method, Manager, Value, Lock
import os

PID = os.getpid()
print('subprocess:', PID)
#print(mp.set_start_method)
OUTPUT_PATH = './fio_test/covid-checkpoint/'

class async_checkpointing:

    def __init__(self, model_state, op_state, epoch):
        self.model_state = model_state
        self.epoch = epoch
        self.op_state = op_state
    def snapshot_storing(self, model_state, op_state, epoch):
        
        model_state = _to_cpu(self.model_state)
        op_state = _to_cpu(self.op_state)
#        for i, j in model_state.items():
#            model_state[i] = j.cpu()
#        for keys in model_state.keys():
#            model_state[keys] = model_state[keys].cpu()
        
        PATH = OUTPUT_PATH + "covid_checkpoint" + str(epoch + 1) + ".pt"
        torch.save({
            'model_state_dict': model_state,
            'optimizer_state_dict' : op_state
        }, PATH)
        PID_w = os.system("cat /proc/"+str(PID)+"/io")
        return 0


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
