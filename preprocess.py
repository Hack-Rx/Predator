import tensorflow as tf
import numpy as np

def excersice(workout):
    if workout=='less':
        w=[1,0,0]
    elif workout=='med':
        w=[0,1,0]
    elif workout=='high':
        w=[0,0,1]
    return w   

def sex(gender):
    if gender=='m':
        g=[1,0]
    elif gender=='f':
        g=[0,1]
    return g
        
def cal(calorie):
    if calorie<=2000:
        c=[1,0,0]
    elif calorie<=2500:
        c=[0,1,0]
    elif calorie>2500:
        c=[0,0,1]
    return c

def preprocessing(workout,bmi,gender,calorie):
    w=np.array(excersice(workout),dtype='float32')
    g=np.array(sex(gender),dtype='float32')
    w_b=np.append(w,[bmi],axis=0)
    w_b_g=np.append(w_b,g,axis=0)
    c=np.array(cal(calorie))
    return np.array([np.append(w_b_g,c,axis=0)],dtype='float32')

def output(array):
    r=np.array(np.reshape(array,(6,)),dtype='int')
    j=1
    for i in r:
        if i==0:
            j=j+1
    return j

model=tf.keras.models.load_model("recc_diet.h5")
"""
Example:-
Input in preprocessing (workout,bmi,gender,calorie)
ans=output(model.predict(preprocessing('less',25,'m',3000)))
"""

ans=output(model.predict(preprocessing('less',25,'m',3000)))