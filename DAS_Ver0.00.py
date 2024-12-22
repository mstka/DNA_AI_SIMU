#数式
#エネルギー反応
#魔法プログラミング

'''
視界移動
移動角度変更
前に進む
捕食


満腹度
解像度(視野角10°ずつと距離30ずつ)
視野角x10
距離×5

腹を埋めた量
'''


import math
import Tensor_Module as TM
import random
import numpy as np

def Calculation_Multiplication(inp,parameter):
    return inp*parameter

def Calculation_Cos(inp,parameter):
    return math.cos(math.radians(inp))*parameter

def Calculation_Sin(inp,parameter):
    return math.sin(math.radians(inp))*parameter

def Calculation_Sigmoid(inp,parameter):
    return 1/(1+math.exp(-inp))*parameter

Define_List = [Calculation_Multiplication, Calculation_Cos, Calculation_Sin, Calculation_Sigmoid]

class Life_Unit:
    def __init__(self):
        '''
        [視野角10] × [距離5] + [満腹度1]
        ↓
        出力用感情2
        FB用感情1
        '''
        self.emo_TAC = TM.Tensor_AI_Class(51, 3, [3,3])
        '''
        [視野角10] × [距離5] + [感情2]
        ↓
        視界移動2
        移動角度変更2
        前に進む
        捕食
        '''
        self.logic_TAC = TM.Tensor_AI_Class(52, 6, [5,5])
        
        self.DNA = [[Define_List[random.randint(0,3)], -2+random.random()*4] for i in range(3)]
        
        self.eye_angle = 0.0
        self.body_angle = 0.0
        
        self.x = 0.0
        self.y = 0.0

        self.nut_level = 0.0
    
    def move_front(self, distance):
        self.x += math.cos(math.radians(self.body_angle)) * distance
        self.y += math.sin(math.radians(self.body_angle)) * distance
    
    def rotate_sight(self, angle):
        self.eye_angle += angle
    
    def rotate_body(self, angle):
        self.body_angle += angle
    
    def eat(self, sight, nut_level,reward):
        true_reward = reward - self.nut_level
        self.nut_level += reward

        emo_inp = sight + nut_level
        logic_inp = sight + self.emo_TAC.predict(emo_inp)[0:2]

        self.logic_TAC.train(logic_inp, self.emo_TAC.predict(emo_inp)[2])
        self.emo_TAC.train(emo_inp, true_reward)
    
    def predict(self, sight, nut_level):
        emo_inp = sight + nut_level
        emo_out = self.emo_TAC.predict(emo_inp)

        logic_inp = sight + emo_out[0:2]
        logic_out = self.logic_TAC.predict(logic_inp)

        self.nut_level -= 0.01

        # NumPy配列に変換（リストも対応可能）
        logic_out = np.array(logic_out)
        
        # 最大値のインデックスを取得
        max_index = np.argmax(logic_out)

        return max_index



class Field_Operation_Class:
    def __init__(self, w,h, life_num):
        self.w = w
        self.h = h
        self.life_num = life_num
        self.life_list = []

        self.f_num = 5

        self.feed = [{'x':random.random()*w,
                      'y':random.random()*h,
                      'type':random.random()*4-2} for i in range(self.f_num)]

        for i in range(self.life_num):
            self.life_list.append(Life_Unit())
        
    def step(self):
        
