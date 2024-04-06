import torch
import numpy as np
import collections
from typing import OrderedDict


'''
[S.L]
Uniform Quantization functoin
model_state - 체크포인팅에 필요한 옵티마이저 파라미터 입력
N-bit - Quantization의 N-bit 파라미터 입력, 정수화 범위 설정에 사용

Uniform De-Quantizaion function
model_state - Uniform Quantizaion된 옵티마이저 파라미터 입력
'''


class UniformOptimizer:
    

    def __init__(self, model_state,N_bit):

        #계산에 필요한 옵티마이저 파라미터 요소의 최댓값 최솟값을 확인하기 위한 리스트 생성
        all_values = []

        #optimizer.state_dict()의 디렉토리 구조를 탐색하며 모든 요소를 리스트에 넣는 과정
        for i in range(len(model_state['state'])):
            step = model_state['state'][i]

            #'state' 내부 디렉토리의 value 요소들을 탐색하여 리스트에 추가
            for key, value in step.items():
                if key == 'exp_avg' or key == 'exp_avg_sq':
                    flat = value.flatten().tolist()
                    all_values.extend(flat)
                                
            

        #옵티마이저 파라미터의 요소 중 최솟값 및 최댓값 
        x_max = max(all_values)
        x_min = min(all_values)

        #옵티마이저 파라미터를 모두 저장한 리스트는 역할을 다했기 때문에 할당 해제
        del all_values
        
        #zero_point는 옵티마이저 압축 및 복원에 필요, 클래스 인스턴스 속성으로 할당
        zero_point = self.zero_point = x_min

        #정수화 범위
        N_range = (2 ** N_bit - 1)

        #모델 파라미터의 범위와 정수화 범위의 비율, 클래스 인스턴스 속성으로 할당
        scale = self.scale =  (x_max - x_min)/N_range
    
    #압축 메소드
    def Quantization(self, model_state, N_bit):
        
        #클래스 인스턴스인 scale과 zero_point를 변수로 지정
        scale = self.scale
        zero_point = self.zero_point
 
        #옵티마이저 파라미터 정수화
        #옵티마이저 파라미터 디렉토리 구조를 탐색
        for i in range(len(model_state['state'])):
            state = model_state['state'][i]

            #각 요소에 접근
            for key, value in state.items():
                if key == 'exp_avg' or key == 'exp_avg_sq':

                    #디렉토리 value 접근하여 원본 텐서 추출
                    tensor_row = state[key]

                    #각 텐서에 정수화 공식을 대입
                    tensor_quantized = torch.round((tensor_row - zero_point)/scale).to(torch.int8)

                    #압축된 텐서를 디렉토리 value에 수정
                    state[key] = tensor_quantized

            #옵티마이저 파라미터 디렉토리 구조에 압축된 값으로 대체
            model_state['state'][i] = state
        return model_state



        #모델 파라미터 복원
    def De_Quantization(self, model_state, N_bit):
        scale = self.scale
        zero_point = self.zero_point

        for i in range(len(model_state['state'])):
            state = model_state['state'][i]
            for key, value in state.items():
                if key == 'exp_avg' or key == 'exp_avg_sq':
                    tensor_quantized = state[key]
                    tensor_recovered = scale * tensor_quantized + zero_point
                    state[key] = tensor_recovered
            model_state['state'][i] = state
        return model_state
'''
Uniform Quantization functoin
model_state - 체크포인팅에 필요한 모델 파라미터 입력
N-bit - Quantization의 N-bit 파라미터 입력, 정수화 범위 설정에 사용

Uniform De-Quantizaion function
model_state - Uniform Quantizaion된 모델 파라미터 입력
'''

class UniformModel:


    def __init__(self, model_state,N_bit):

        #계산에 필요한 모델 파라미터 요소의 최댓값 최솟값을 확인하기 위한 리스트 생성
        all_values = []

        #model.state_dict()의 디렉토리 구조를 탐색하며 모든 요소를 리스트에 넣는 과정
        for tensor in model_state.values():
            
            #모델 파라미터의 다차원 구조를 직렬화
            flat = tensor.flatten().tolist()

            #직렬화한 flat에서 float만 추출, 리스트에 추가
            flat_float = [getfloat for getfloat in flat if isinstance(getfloat,float)]
            all_values.extend(flat_float)
        

        #모델 파라미터 모든 요소를 포함한 리스트에서 최댓값 최솟값 추출
        x_max = max(all_values)
        x_min = min(all_values)

        #모델 파라미터를 모두 저장한 리스트는 역할을 다했기 때문에 해제
        del all_values

        #압축 및 복원에 필요, 인스턴스 속성으로 할당
        zero_point = self.zero_point = x_min

        #정수화 범위, 압축에 사용
        N_range = (2 ** N_bit - 1)

        #모델 파라미터의 범위, 압축 및 복원에 필요하기 때문에 인스턴스 속성으로 할당
        scale = self.scale =  (x_max - x_min)/N_range

    #압축 메소트
    def Quantization(self, model_state, N_bit):

        #클래스 인스턴스인 scale과 zero_point를 변수로 지정
        scale = self.scale
        zero_point = self.zero_point
 
        #모델 파라미터 정수화
        #모델 파라미터를 탐색하여 각 요소에 접근
        for keys in model_state.keys():

            #디렉토리 value 접근하여 원본 텐서 추출
            tensor_row = model_state[keys]

            #각 텐서에 정수화 공식을 대입
            tensor_quantized = torch.round((tensor_row - zero_point)/scale).to(torch.int8)

            #압축된 텐서를 디렉토리 value에 수정
            model_state[keys] = tensor_quantized

        return model_state
    
    def De_Quantization(self, model_state, N_bit):
        scale = self.scale
        zero_point = self.zero_point

        #모델 파라미터 복원
        for keys in model_state.keys():
            tensor_quantized = model_state[keys]
            tensor_recovered = scale * tensor_quantized + zero_point
            model_state[keys] = tensor_recovered

        return model_state
