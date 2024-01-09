import numpy as np
import pandas as pd
from pathlib import Path
import os.path
from sklearn.model_selection import train_test_split
from tensorflow import keras
import tensorflow as tf
from sklearn.metrics import r2_score

def main():
    image_dir = Path(r'') #Đường dẫn tới file test
    filepaths = pd.Series(list(image_dir.glob(r'*.jpg')), name='Filepath').astype(str)
    ages = pd.Series(filepaths.apply(lambda x: os.path.split(os.path.split(x)[0])[1]), name='Age').astype(int)
    images = pd.concat([filepaths, ages], axis=1).sample(frac=1.0, random_state=1).reset_index(drop=True)

    # Load Model
    model = tf.keras.models.load_model(r'C:\Users\ngoct\OneDrive\Desktop\face_detection\train\Restnet_52.tf') #đường dẫn tới tập đã train
    print('ok')
    model.summary()
    # Create ImageDataGenerator
    train_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    # Change images to dataframe
    test_images = train_generator.flow_from_dataframe(
        dataframe=images,
        x_col='Filepath',
        y_col='Age',
        target_size=(224, 224),
        color_mode='rgb',
        class_mode='raw',
        # color_mode='grayscale',
        batch_size=128,
        shuffle=False
    )

    # Predict images
    predicted_ages = np.squeeze(model.predict(test_images)).astype(int)
    true_ages = test_images.labels

    # rmse = np.sqrt(model.evaluate(test_images, verbose=0))
    # print("     Test RMSE: {:.5f}".format(rmse))

    r2 = r2_score(true_ages, predicted_ages)
    print("Test R^2 Score: {:.5f}".format(r2))
    print("Predict age: \n", predicted_ages)
    print("True age: \n", true_ages)
    print("Mean age predict: ", np.mean(predicted_ages))
    print("Mean age true: ", np.mean(true_ages[0:100]))
    print(model.evaluate(test_images, verbose=1))
if __name__ == '__main__':
    main()