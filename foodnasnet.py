import os
import tensorflow as tf
from tensorflow.keras.applications.nasnet import NASNetLarge
from tensorflow.keras.applications.nasnet import preprocess_input
#from tensorflow.keras.preprocessing import image


train_data_dir="/Users/sushmabansal/Desktop/food_data/images"

data=tf.keras.preprocessing.image.ImageDataGenerator(
    featurewise_center=False,
    samplewise_center=False,
    featurewise_std_normalization=False,
    samplewise_std_normalization=False,
    zca_whitening=False,
    zca_epsilon=1e-06,
    rotation_range=45,
    width_shift_range=0.0,
    height_shift_range=0.0,
    brightness_range=None,
    shear_range=0.1,
    zoom_range=0.1,
    channel_shift_range=0.0,
    fill_mode="nearest",
    cval=0.0,
    horizontal_flip=True,
    vertical_flip=False,
    rescale=1./255,
)
datagen=data.flow_from_directory(
        train_data_dir,
        target_size=(331, 331),
        batch_size=101,
        shuffle=True,
        class_mode='categorical')

base_model = NASNetLarge(weights='imagenet',input_shape=(331,331,3), include_top=False)


#base_model = tf.keras.applications.EfficientNetB7(weights='imagenet',input_shape=(360,360,3), include_top=False)

for layer in base_model.layers:
    layer.trainable = False


x = base_model.output
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dropout(0.4)(x)
x = tf.keras.layers.Dense(1024, activation='relu')(x)
x = tf.keras.layers.BatchNormalization()(x)
x = tf.keras.layers.Dense(512, activation='relu')(x)
x = tf.keras.layers.BatchNormalization()(x)
x = tf.keras.layers.Dense(256, activation='relu')(x)
predictions = tf.keras.layers.Dense(101, activation='softmax')(x)
model = tf.keras.models.Model(inputs=base_model.input, outputs=predictions)

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
    label_smoothing=0.1,
    reduction="auto",
    name="categorical_crossentropy",
),metrics=['accuracy'])
model.fit_generator(datagen,steps_per_epoch=10,epochs=20)

model.save('trained_food_new2.h5')


"""img_path = 'pizza.jpg'
img = image.load_img(img_path, target_size=(331, 331))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

outputclass= model.predict(x)"""
