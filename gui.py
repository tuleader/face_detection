import cv2
import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from datetime import datetime
from tkinter import messagebox, filedialog
from face_detection import detect,detect2
from rcm import open_web
# tạo giao diện
def createwidgets():
    root.feedlabel = Label(root, bg="steelblue", fg="white", text="WEBCAM FEED", font=('Comic Sans MS',20))
    root.feedlabel.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

    root.cameraLabel = Label(root, bg="steelblue", borderwidth=3, relief="groove")
    root.cameraLabel.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

    root.captureBTN = Button(root, text="CAPTURE", command=Capture, bg="#CDB7B5", font=('Comic Sans MS',15), width=20)
    root.captureBTN.grid(row=4, column=1, padx=10, pady=10)

    root.CAMBTN = Button(root, text="STOP CAMERA", command=StopCAM, bg="#CDB7B5", font=('Comic Sans MS',15), width=13)
    root.CAMBTN.grid(row=4, column=2)

    root.previewlabel = Label(root, bg="steelblue", fg="white", text="IMAGE PREVIEW", font=('Comic Sans MS',20))
    root.previewlabel.grid(row=1, column=4, padx=10, pady=10, columnspan=2)

    root.imageLabel = Label(root, bg="steelblue", borderwidth=3, relief="groove")
    root.imageLabel.grid(row=2, column=4, padx=10, pady=10, columnspan=2)
    # Tạo một đối tượng hình ảnh Tkinter từ ảnh đã mở.
    saved_image = PhotoImage(file='./img_preview.png')
    # Cập nhật ảnh của nhãn root.imageLabel để hiển thị ảnh đã chụp.
    root.imageLabel.config(image=saved_image)
    # Lưu trữ đối tượng hình ảnh Tkinter để tránh bị thu hồi bởi garbage collector.
    root.imageLabel.photo = saved_image

    root.openImageEntry = Entry(root, width=55, textvariable=imagePath)
    root.openImageEntry.grid(row=4, column=4, padx=10, pady=10)

    root.openImageButton = Button(root, width=10, text="BROWSE", command=imageBrowse)
    root.openImageButton.grid(row=3, column=5, padx=10, pady=10)
    
    root.startPredict = Button(root, text="START PREDICT", command=StartPredict, bg="#CDB7B5", font=('Comic Sans MS',15), width=15)
    root.startPredict.grid(row=4, column=5, padx=10, pady=10)

    # khởi động hàm ShowFeed cùng giao diện
    ShowFeed()

def ShowFeed():
    # Dùng phương thức read() của đối tượng root.cap để đọc một frame từ camera.
    # ret là một biến boolean, nếu là True thì việc đọc frame thành công, ngược lại là False.
    ret, frame = root.cap.read()

    if ret:
        # Sử dụng cv2.flip để lật ngược frame theo chiều ngang giúp cho ảnh không bị ngược.
        frame = cv2.flip(frame, 1)

        # Thêm văn bản hiển thị thời gian lên frame.
        cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))

        # Chuyển đổi màu từ BGR sang RGBA. Đối với OpenCV, mô hình màu thường là BGR, nhưng Pillow (PIL) sử dụng RGBA.
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        
        # Gọi hàm detect xử lý.
        canvas = detect(rgb, frame)

        # Chuyển đổi frame sau khi đã được xử lý (với khuôn mặt được đánh dấu) từ mảng NumPy thành đối tượng hình ảnh Pillow.
        videoImg = Image.fromarray(canvas)

        # Tạo đối tượng hình ảnh Tkinter từ đối tượng hình ảnh Pillow.
        imgtk = ImageTk.PhotoImage(image = videoImg)

        # Cập nhật ảnh root.cameraLabel để hiển thị frame đã được xử lý.
        root.cameraLabel.configure(image=imgtk)

        # Lưu trữ đối tượng hình ảnh Tkinter để tránh việc bị thu hồi bởi garbage collector.
        root.cameraLabel.imgtk = imgtk

        # Sử dụng after để gọi lại chính hàm ShowFeed sau 10 miligiây, tạo ra một vòng lặp liên tục cho việc hiển thị feed từ camera.
        root.cameraLabel.after(10, ShowFeed)
    else:
        # Tạo đối tượng PhotoImage từ đường dẫn hình ảnh
        imgtkk = PhotoImage(file='./img_source.png')
        # Cập nhật ảnh root.cameraLabel để hiển thị frame đã được xử lý.
        root.cameraLabel.configure(image=imgtkk)
        # Lưu trữ đối tượng hình ảnh Tkinter để tránh việc bị thu hồi bởi garbage collector.
        root.cameraLabel.imgtk = imgtkk
    
def imageBrowse():
    global imgName
    # Mở,chọn và lưu đường dẫn ảnh
    imgName = filedialog.askopenfilename(initialdir="YOUR DIRECTORY PATH", filetypes=[("Image Files", "*.png;*.jpg")])
    
    # Cập nhật đường dẫn
    imagePath.set(imgName)

    # Resize kích thước vừa với giao diện
    imageResize = resizeImage(imgName, max_width=640, max_height=480)

    # Tạo một đối tượng hình ảnh Tkinter từ đối tượng hình ảnh Pillow đã được thay đổi kích thước.
    imageDisplay = ImageTk.PhotoImage(imageResize)

    # Đưa ảnh lên GUI
    root.imageLabel.config(image=imageDisplay)
    root.imageLabel.photo = imageDisplay

def Capture():
    # Tạo tên đường dẫn
    image_name = datetime.now().strftime('%d-%m-%Y %H-%M-%S')

    # Khai báo biến imgName là biến toàn cục để có thể sử dụng nó trong phạm vi của hàm.
    global imgName
    imgName ="folder_image/" + image_name + ".jpg"

    # Sử dụng root.cap.read() để đọc một frame từ camera.
    ret, frame = root.cap.read()

    # Thêm văn bản hiển thị thời gian lên frame để định dạng ảnh.
    cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (430,460), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))

    # Lưu frame đã chụp thành file ảnh tại đường dẫn imgName.
    success = cv2.imwrite(imgName, frame)

    # Mở ảnh vừa lưu bằng thư viện Pillow (PIL).
    saved_image = Image.open(imgName)

    # Tạo một đối tượng hình ảnh Tkinter từ ảnh đã mở.
    saved_image = ImageTk.PhotoImage(saved_image)

    # Cập nhật ảnh của nhãn root.imageLabel để hiển thị ảnh đã chụp.
    root.imageLabel.config(image=saved_image)

    # Lưu trữ đối tượng hình ảnh Tkinter để tránh bị thu hồi bởi garbage collector.
    root.imageLabel.photo = saved_image

    # Cập nhật đường dẫn
    imagePath.set(imgName)

    # Hiển thị thông báo
    if success :
        messagebox.showinfo("SUCCESS", "IMAGE CAPTURED AND SAVED IN " + imgName)

# Tắt camera
def StopCAM():
    root.cap.release()

    root.CAMBTN.config(text="START CAMERA", command=StartCAM)

# Bật camera
def StartCAM():
    root.cap = cv2.VideoCapture(0)

    width_1, height_1 = 640, 480
    root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_1)
    root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height_1)

    root.CAMBTN.config(text="STOP CAMERA", command=StopCAM)
    root.cameraLabel.config(text="")

    ShowFeed()

def StartPredict():
    # Khai báo biến imgName là biến toàn cục để có thể sử dụng nó trong phạm vi của hàm.
    global imgName

    # Sử dụng OpenCV để đọc ảnh từ đường dẫn imgName và lưu nó trong biến image.
    image = cv2.imread(imgName)

    # Chuyển đổi ảnh từ không gian màu BGR sang BGRA (rgb) và RGBA để sử dụng cho việc dự đoán và hiển thị.
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)

    # Gọi hàm detect2 để dự đoán tuổi và tạo một canvas mới để hiển thị kết quả.
    canvas, predicted_age = detect2(rgb, frame)

    # Chuyển đổi mảng numpy (canvas) thành đối tượng hình ảnh của Pillow.
    predict_image = Image.fromarray(canvas)

    # Tạo một đối tượng hình ảnh Tkinter từ ảnh đã resize.
    predict_image = ImageTk.PhotoImage(predict_image)

    # Cập nhật ảnh của nhãn root.imageLabel để hiển thị ảnh đã dự đoán.
    root.imageLabel.config(image=predict_image)

    # Lưu trữ đối tượng hình ảnh Tkinter để tránh bị thu hồi bởi garbage collector.
    root.imageLabel.photo = predict_image

    # Gọi hàm đưa ra recommend về thời trang
    open_web(predicted_age)

# Chỉnh lại kích thước ảnh đầu vào hiển thị cho phù hợp với giao diện
def resizeImage(image_path, max_width=640, max_height= 480):
    # Mở ảnh
    original_image = Image.open(image_path)
    
    # Tính toán tỉ lệ giữa chiều rộng và chiều cao
    aspect_ratio = original_image.width / original_image.height
    
    # Tính toán chiều rộng mới và chiều cao mới dựa trên tỉ lệ và chiều rộng mục tiêu
    if int(max_width / aspect_ratio) < 480:
        new_width = max_width
        new_height = int(max_width / aspect_ratio)
    else:
        new_height = max_height
        new_width = int(max_height * aspect_ratio)
    
    # Resize ảnh
    resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
    
    return resized_image

root = tk.Tk()

# Kết nối với camera mặc định
root.cap = cv2.VideoCapture(0)

# Thiết lập kích thước khung hình cho camera
width, height = 640, 480
root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root.title("Pycam")
root.geometry("1340x700")
# Cho phép thay đổi kích thước cửa sổ chính theo cả chiều rộng và chiều cao.
root.resizable(True, True)
root.configure(background = "#B0E2FF")

# Khởi tạo biến imgName để lưu đường dẫn và tên file của ảnh khi được chụp.
imgName = ""
imagePath = StringVar()

createwidgets()
root.mainloop()
