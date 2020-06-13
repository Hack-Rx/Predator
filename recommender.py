import numpy as np
import tensorflow as tf
from tensorflow.keras.utils import to_categorical

bmi= np.random.uniform(low=16, high=35, size=(1000,1))
gbmi=np.sort(np.random.normal(loc=22.5,scale=3.5,size=1000))
gage=np.sort(np.random.normal(loc=36,scale=10,size=1000))+5
low=np.array([[1,0,0] for i in range(400)])
med=np.array([[0,1,0] for i in range(300)])
high=np.array([[0,0,1] for i in range(300)])
""" low or no workout=[1,0,0]
    medium workout=[0,1,0]
    high workout=[0,0,1]
    """
workout=np.append(low,med,axis=0)
workout=np.append(workout,high,axis=0)
b_w=np.append(workout,np.flipud(np.reshape(gbmi,(1000,1))),axis=1)
gender_m=np.array([[1,0] for i in range(500)])
gender_f=np.array([[0,1] for i in range(500)])
m_f=np.append(gender_m,gender_f,axis=0)
np.random.shuffle(m_f)
b_w_g=np.append(b_w,m_f,axis=1)
daily_intake_low=np.array([[1,0,0] for i in range(400)])
daily_intake_med=np.array([[0,1,0] for i in range(300)])
daily_intake_high=np.array([[0,0,1] for i in range(300)])
daily=np.append(daily_intake_low,daily_intake_med,axis=0)
daily=np.append(daily,daily_intake_high,axis=0)
data=np.append(b_w_g,daily,axis=1)
labels=np.reshape(np.sort(
        np.array(np.random.uniform(low=0, high=6, size=(1000)),dtype='int')),(1000,1))
labels=to_categorical(labels)

model=tf.keras.Sequential([
        tf.keras.layers.Dense(12,activation="relu",input_shape=(9,)),
        tf.keras.layers.Dense(10,activation="relu"),
        tf.keras.layers.Dense(8,activation="relu"),
        tf.keras.layers.Dense(6,activation="softmax")
        ])

adam=tf.keras.optimizers.Adam(
    learning_rate=0.001,
    beta_1=0.9,
    beta_2=0.999,
    epsilon=1e-07,
    amsgrad=True,
    name="Adam",
    clipnorm=1.0
)


model.compile(optimizer=adam, loss=tf.keras.losses.CategoricalCrossentropy(
    from_logits=False,
    label_smoothing=0.0,
    reduction="auto",
    name="categorical_crossentropy"),metrics=['accuracy'])

model.fit(data,labels,epochs=1000)
model.save('recc_diet.h5')