#Importing cv2
import cv2
import numpy as np
from tensorflow import keras
from tkinter import messagebox, filedialog

# Load Model
model = keras.models.load_model(r'C:\Users\ngoct\Downloads\Restnet_52.tf\Restnet_52.tf')
# Create ImageDataGenerator
test_generator = keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255
)
print('OK')

#Loading cascades
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Nhận một hình ảnh ở định dạng RGB (rgb) và khung tương ứng.
def detect(rgb, frame): 
    # Khởi tạo một biến cho kết quả dự đoán và phát hiện khuôn mặt trong hình ảnh đầu vào bằng cách sử dụng Haar face cascade.
    faces = face_cascade.detectMultiScale(rgb,scaleFactor=1.3,minNeighbors=5)

    # Lặp qua các khuôn mặt đã phát hiện. 
    for (x, y, w, h) in faces:
        # Vẽ một hình chữ nhật xung quanh khuôn mặt được phát hiện trên khung. 
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 3)

        # Trích xuất vùng khuôn mặt, thay đổi kích thước và chuyển đổi thành mảng float32.
        border = 0
        img_cat = frame[y-border:y+h+border, x-border:x+w+border] 
        img_age = np.resize(img_cat, (3, 224, 224, 3))  
        img_age = img_age.astype('float32')
        # cv2.imshow("test", img_cat)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # Tạo một luồng ảnh để dự đoán sử dụng generator dữ liệu hình ảnh.
        img_pedict = test_generator.flow(img_age, batch_size=32, shuffle=True) 
        
        #Sử dụng mô hình đã tải để dự đoán tuổi từ hình ảnh khuôn mặt.
        output_predict = int(np.squeeze(model.predict(img_pedict)).item(0)) # Predict
        print(output_predict)
        # Thêm văn bản vào khung hiển thị kết quả dự đoán tuổi phía trên hình chữ nhật.
        col = (0, 255, 0)
        cv2.putText(frame, str(output_predict), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, h/200, col ,2) # Display result 
    return frame
#Nhận một hình ảnh ở định dạng RGB (rgb) và khung tương ứng.
def detect2(rgb, frame): 
    # Khởi tạo một biến cho kết quả dự đoán và phát hiện khuôn mặt trong hình ảnh đầu vào bằng cách sử dụng Haar face cascade.
    faces = face_cascade.detectMultiScale(rgb,scaleFactor=1.3,minNeighbors=5)

    # Lặp qua các khuôn mặt đã phát hiện. 
    for (x, y, w, h) in faces:
        # Vẽ một hình chữ nhật xung quanh khuôn mặt được phát hiện trên khung. 
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 3)

        # Trích xuất vùng khuôn mặt, thay đổi kích thước và chuyển đổi thành mảng float32.
        border = 0
        img_cat = frame[y-border:y+h+border, x-border:x+w+border]
        img_age = np.resize(img_cat, (3, 224, 224, 3))  
        img_age = img_age.astype('float32')
        # cv2.imshow("test", img_cat)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # Tạo một luồng ảnh để dự đoán sử dụng generator dữ liệu hình ảnh.
        img_pedict = test_generator.flow(img_age, batch_size=32, shuffle=True) 
        
        #Sử dụng mô hình đã tải để dự đoán tuổi từ hình ảnh khuôn mặt.
        output_predict = int(np.squeeze(model.predict(img_pedict)).item(0)) # Predict
        print(output_predict)
        # Thêm văn bản vào khung hiển thị kết quả dự đoán tuổi phía trên hình chữ nhật.
        col = (0, 255, 0)
        cv2.putText(frame, str(output_predict), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, h/200, col ,2) # Display result 
    try:
        return frame,output_predict
    except Exception:
        messagebox.showerror("Error","Face not found")