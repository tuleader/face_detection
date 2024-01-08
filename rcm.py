import tkinter as tk
import webbrowser
import json
import datetime
def recommend_fashion(predicted_age):
    if predicted_age < 13:
        return "https://shopee.vn/bitas_store?shopCollection=120740926#product_list","https://shopee.vn/obeahvn?shopCollection=158829356#product_list",'https://shopee.vn/benty.vn?shopCollection=246246813#product_list'
    elif 13 <= predicted_age <= 19:
        return "https://shopee.vn/bitas_store?shopCollection=120740926#product_list","https://shopee.vn/2storegle?shopCollection=23302426#product_list",'https://shopee.vn/benty.vn?shopCollection=246246813#product_list'
    elif 20 <= predicted_age <= 29:
        return "https://shopee.vn/bitas_store?shopCollection=120740926#product_list","https://shopee.vn/2storegle?shopCollection=23302426#product_list",'https://shopee.vn/benty.vn?shopCollection=246246813#product_list'
    elif 30 <= predicted_age <= 50:
        return "https://shopee.vn/bitas_store?shopCollection=120740926#product_list","https://shopee.vn/obeahvn?shopCollection=158829356#product_list",'https://shopee.vn/benty.vn?shopCollection=246246813#product_list'
    else:
        return "https://shopee.vn/bitas_store?shopCollection=120740926#product_list","https://shopee.vn/obeahvn?shopCollection=158829356#product_list",'https://shopee.vn/benty.vn?shopCollection=246246813#product_list'

def open_web(predicted_age):
    shoe_url, shirt_url, hat_url = recommend_fashion(predicted_age)

    root = tk.Tk()
    root.title("Classifying fashion by age")

    label_result = tk.Label(root, text="Hello, I wonder if you need any suggestions from us?", bg="white", font=('Comic Sans MS', 15))
    label_result.pack(padx=20, pady=20)

    frame_buttons = tk.Frame(root, bg="#B0E2FF")  # Tạo một frame mới để chứa ba nút
    frame_buttons.pack()

    def open_web_page(url):
        webbrowser.open(url)

    button_shoe = tk.Button(frame_buttons, text="Shoes", command=lambda: open_web_page(shoe_url), bg="#CDB7B5", font=('Comic Sans MS', 15), width=5)
    button_shoe.pack(side="left", padx=10)

    button_shirt = tk.Button(frame_buttons, text="Clothes", command=lambda: open_web_page(shirt_url), bg="#CDB7B5", font=('Comic Sans MS', 15), width=10)
    button_shirt.pack(side="left", padx=10)

    button_hat = tk.Button(frame_buttons, text="Hat", command=lambda: open_web_page(hat_url), bg="#CDB7B5", font=('Comic Sans MS', 15), width=5)
    button_hat.pack(side="left", padx=10)

    root.configure(background="#B0E2FF")
    # root.mainloop()

    def on_return_from_browser():
        ask_for_rating()

    def ask_for_rating():
        rating_window = tk.Toplevel(root)
        rating_window.title("Rate your experience")

        tk.Label(rating_window, text="Please rate your experience", font=('Comic Sans MS', 15)).pack(padx=20, pady=10)

        # Tạo giao diện đánh giá sao
        rating_frame = tk.Frame(rating_window)  # Thêm khung cho các nút đánh giá
        rating_frame.pack(pady=10)
        rating_var = tk.IntVar(value=5)  # Thiết lập giá trị mặc định là 5
        def update_rating(value):
            rating_var.set(value)

        for i in range(1, 6):
            tk.Radiobutton(rating_frame, text=f"{i} Stars", variable=rating_var, value=i, font=('Comic Sans MS', 12),
                           command=lambda i=i: update_rating(i)).pack(side='left')

        # Ô nhập nội dung đánh giá
        tk.Label(rating_window, text="Your feedback:", font=('Comic Sans MS', 15)).pack(padx=20, pady=10)
        feedback_var = tk.StringVar()
        entry_feedback = tk.Entry(rating_window, textvariable=feedback_var, font=('Comic Sans MS', 15), width=50)
        entry_feedback.pack(padx=20, pady=10)
        def submit_rating():
            rating = rating_var.get()
            feedback = feedback_var.get()
            now = datetime.datetime.now().isoformat()
            data = {
                "timestamp": now,
                "rating": rating,
                "feedback": feedback
            }

            with open("ratings.txt", "a") as f:
                json.dump(data, f)
                f.write("\n")
            rating_window.destroy()

        submit_button = tk.Button(rating_window, text="Submit", command=submit_rating, font=('Comic Sans MS', 15))
        submit_button.pack(pady=10)

    button_rate = tk.Button(root, text="Rate Experience", command=on_return_from_browser, font=('Comic Sans MS', 15))
    button_rate.pack(pady=10)

    root.mainloop()