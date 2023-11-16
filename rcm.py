import tkinter as tk
import webbrowser

def recommend_fashion(predicted_age):
    if predicted_age < 13:
        return "https://shopee.vn/bitas_store?shopCollection=120740926#product_list","https://shopee.vn/obeahvn?shopCollection=158829356#product_list",'https://shopee.vn/benty.vn?shopCollection=246246813#product_list'
    elif 13 <= predicted_age <= 19:
        return "https://shopee.vn/bitas_store?shopCollection=120740926#product_list","https://shopee.vn/obeahvn?shopCollection=158829356#product_list",'https://shopee.vn/benty.vn?shopCollection=246246813#product_list'
    elif 20 <= predicted_age <= 29:
        return "https://shopee.vn/bitas_store?shopCollection=120740926#product_list","https://shopee.vn/obeahvn?shopCollection=158829356#product_list",'https://shopee.vn/benty.vn?shopCollection=246246813#product_list'
    elif 30 <= predicted_age <= 50:
        return "https://shopee.vn/bitas_store?shopCollection=120740926#product_list","https://shopee.vn/obeahvn?shopCollection=158829356#product_list",'https://shopee.vn/benty.vn?shopCollection=246246813#product_list'
    else:
        return "https://shopee.vn/bitas_store?shopCollection=120740926#product_list","https://shopee.vn/obeahvn?shopCollection=158829356#product_list",'https://shopee.vn/benty.vn?shopCollection=246246813#product_list'

def open_web(predicted_age):
    shoe_url, shirt_url, hat_url = recommend_fashion(predicted_age)

    root = tk.Tk()
    root.title("Classifying fashion by age")

    label_result = tk.Label(root, text=f"Hello, I wonder if you need any suggestions from us?", bg="white", font=('Comic Sans MS', 15))
    label_result.pack(padx=20, pady=20)

    def open_web_page(url):
        webbrowser.open(url)

    button_shoe = tk.Button(root, text="Shoes", command=lambda: open_web_page(shoe_url), bg="#CDB7B5", font=('Comic Sans MS', 15), width=5)
    button_shoe.pack(side="left", padx=10)

    button_shirt = tk.Button(root, text="Clothes", command=lambda: open_web_page(shirt_url), bg="#CDB7B5", font=('Comic Sans MS', 15), width=10)
    button_shirt.pack(side="left", padx=10)

    button_hat = tk.Button(root, text="Hat", command=lambda: open_web_page(hat_url), bg="#CDB7B5", font=('Comic Sans MS', 15), width=5)
    button_hat.pack(side="left", padx=10)

    root.configure(background="#B0E2FF")
    root.mainloop()


# # Example usage:
# predicted_age = 25
# open_web(predicted_age)
