import numpy as np
import pandas as pd
from pathlib import Path
import os.path
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from model.network import set_model
from model.dataloader import data_loader
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint,EarlyStopping
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def visualizez_data():
    import os
    import matplotlib.pyplot as plt
    # Đường dẫn đến thư mục chứa các thư mục con
    base_path = r"C:\Users\ngoct\OneDrive\Desktop\face_detection\train\datatrain"
    # Lấy danh sách tất cả các thư mục con trong thư mục cơ sở và sắp xếp chúng theo tên
    subdirectories = sorted([f.path for f in os.scandir(base_path) if f.is_dir()], key=lambda x: int(os.path.basename(x)))
    # Tạo danh sách lưu trữ tên thư mục và số lượng file trong mỗi thư mục
    folder_names = []
    file_counts = []
    # Lặp qua từng thư mục con
    for directory in subdirectories:
        folder_name = os.path.basename(directory)  # Lấy tên thư mục từ đường dẫn
        file_count = len(os.listdir(directory))    # Đếm số lượng file trong thư mục
        folder_names.append(folder_name)
        file_counts.append(file_count)
    # Chỉnh độ rộng của cột
    column_width = 0.5  # Điều chỉnh độ rộng ở đây
    # Vẽ đồ thị
    plt.figure(figsize=(16,9))
    plt.bar(folder_names, file_counts, color='blue', width=column_width)
    plt.xlabel('')
    plt.ylabel('')
    plt.title('Biểu đồ tập dữ liệu')
    # Thêm chỉ số chiều dài cột x
    plt.xticks(rotation=90, ha='right')  # Đặt góc xoay cho tên thư mục để tránh chồng lên nhau
    plt.xticks(range(len(folder_names)), folder_names)  # Thêm chỉ số và nhãn cho mỗi thư mục
    plt.show()
def main():
    # Load images
    visualizez_data() 
    image_dir = Path(r"C:\Users\ngoct\OneDrive\Desktop\face_detection\train\datatrain") #file train
    filepaths = pd.Series(list(image_dir.glob(r'**/*.jpg')), name='Filepath').astype(str)
    ages = pd.Series(filepaths.apply(lambda x: os.path.split(os.path.split(x)[0])[1]), name='Age').astype(int)
    # ages = pd.get_dummies(ages)
    images = pd.concat([filepaths, ages], axis=1).sample(frac=1.0, random_state=1).reset_index(drop=True)
    train_df, test_df = train_test_split(images, test_size=0.2, random_state=1, shuffle=True)

    train_images, val_images, test_images = data_loader(train_df, train_df, test_df)
    model = set_model()
    
    epochs = 120
    path_save = "Restnet_55"
    filename='log.csv'
    history_logger=tf.keras.callbacks.CSVLogger(filename, separator=",", append=True)
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=15)
    checkpoint = ModelCheckpoint(filepath="{}.tf".format(path_save),
                                #  monitor='val_accuracy',
                                save_best_only=False,
                                verbose=1
                                )
    history = model.fit(train_images,
                        validation_data=val_images,
                        epochs=epochs,
                        callbacks=[checkpoint, early_stopping, history_logger],
                        shuffle=False
                        )
    
    plotting_data_dict = history.history
    test_loss = plotting_data_dict['val_loss']
    training_loss = plotting_data_dict['loss']
    # test_accuracy = plotting_data_dict['val_accuracy']
    # training_accuracy = plotting_data_dict['accuracy']
    test_mae = plotting_data_dict['val_mean_absolute_error']
    training_mae = plotting_data_dict['mean_absolute_error']

    epochs = range(1,len(test_loss)+1)
    plt.figure(figsize=(12, 4))
    plt.subplot(121)
    plt.plot(epochs,training_loss, label='training_loss')
    plt.plot(epochs,test_loss, label='test_loss')
    plt.legend()

    plt.subplot(122)
    plt.plot(epochs, training_mae, label='train_mae')
    plt.plot(epochs,test_mae, label='test_mae')
    plt.legend()

    # plt.subplot(133)
    # plt.plot(epochs,test_accuracy,marker='X',label='test_accuracy')
    # plt.plot(epochs,training_accuracy,marker='X',label='training_accuracy')
    # plt.legend()
    plt.savefig('{}.png'.format(path_save))

if __name__ == '__main__':
    main()