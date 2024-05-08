import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from main.manager.user_manager import UserManager
from main.manager.car_manager import CarManager
from main.module.user import User
from main.module.car import Car
from tkcalendar import DateEntry
import threading
from datetime import datetime
from main.manager.rent_manager import RentManager
from main.module.rent_order import RentOrder

local_data = threading.local()


def set_current_user(user):
    local_data.user = user


def get_current_user():
    return getattr(local_data, 'user', None)


def on_closing():
    user = get_current_user()
    if user:
        print(f"User {user} logged out.")
        del local_data.user
    root.destroy()


def set_login_user(user):
    set_current_user(user)
    print(f"User {user} logged in.")


def regist_user(role):
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    # 在这里添加保存用户信息的逻辑
    userManager = UserManager()
    userManager.create_user_table()

    user = userManager.select_user_fields({"user_name": username, "role": role});

    if user:
        messagebox.showerror("Error", "The user is exit, Please login.")
        clear_popup()
        return

    userManager.insert_user((username, password, datetime.now(), datetime.now(), role, 0))
    messagebox.showinfo("Success", "Registration successful!")
    clear_popup()


def login_user(role):
    global current_user_label
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    userManager = UserManager()
    userManager.create_user_table()

    result = userManager.select_user_fields({"user_name": username, "role": role});

    if not result:
        messagebox.showerror("Error", "The user is not exit, Please regist.")
        clear_popup()
        return

    user = User(*result)

    if password != user.password:
        messagebox.showerror("Error", "The password is not correct, Please try again.")
        return

    set_login_user(user)

    clear_popup()
    button1.place_forget()
    button2.place_forget()
    button3.place_forget()
    button4.place_forget()
    text = "Admin" if role == 1 else "Customer"
    current_user_label = tk.Label(root, text="Hello " + text + ": " + user.userName, font=("Arial", 13))
    current_user_label.place(relx=0.95, rely=0.03, anchor="ne")
    current_user_label.config(highlightbackground="gray", highlightthickness=1)

    # 管理员首页menu
    if role == 1:
        carListButton = tk.Button(root, text="Car List", command=lambda: show_car_list(role))
        carListButton.place(relx=0.05, rely=0.05, anchor=tk.NW)

        addCarButton = tk.Button(root, text="Add Car", command=show_form_popup)
        addCarButton.place(relx=0.13, rely=0.05, anchor=tk.NW)

        addCarButton = tk.Button(root, text="Order Review", command=lambda: show_rent_list(role))
        addCarButton.place(relx=0.21, rely=0.05, anchor=tk.NW)
        return

    carListButton = tk.Button(root, text="Car List", command=lambda: show_car_list(role))
    carListButton.place(relx=0.05, rely=0.05, anchor=tk.NW)

    addCarButton = tk.Button(root, text="Rent Order", command=lambda: show_rent_list(role))
    addCarButton.place(relx=0.13, rely=0.05, anchor=tk.NW)


def edit_car(car_id):
    print(f"Editing car with ID {car_id}")


def delete_car(carId):
    carManager = CarManager()
    carManager.update_car_field("deleted", 1, "id", carId)


def show_rent_list(role):
    rentManager = RentManager()
    rent_data = None

    rent_cars = rentManager.select_rental_fields({"deleted": 0});
    rent_data = [RentOrder.create_rental_from_tuple(data) for data in rent_cars]

    # 创建表格框架
    tree_frame = tk.Frame(root, bd=2, relief="groove")
    tree_frame.place(relx=0.05, rely=0.15, anchor=tk.NW, relwidth=0.9, relheight=0.8)

    # 创建表格标题
    columns = (
        "ID", "UserName", "Make", "Model", "Year", "Mileage", "Rental Start Day", "Rental Days", "Rate", "Cost",
        "Status")
    for i, column in enumerate(columns):
        label = tk.Label(tree_frame, text=column, bd=1, relief="groove")
        label.grid(row=0, column=i, sticky="nsew")

    for i, rent in enumerate(rent_data, start=1):
        rent_attributes = [rent.id, rent.userName, rent.make, rent.model, rent.year, rent.mileage, rent.rentalStartDay,
                           rent.rentalDays,
                           rent.rate, rent.cost, rent.status]

        for j, item in enumerate(rent_attributes):
            label = tk.Label(tree_frame, text=item, bd=1, relief="groove")
            label.grid(row=i, column=j, sticky="nsew")
        if role == 1 and rent.status == "Pending Review":
            # 创建 Approve 和 Reject 按钮
            approve_button = ttk.Button(tree_frame, text="Approve",
                                        command=lambda rentId=rent.id: operate_rent_order("approve", rentId))
            approve_button.grid(row=i, column=len(rent_attributes) + 1)

            reject_button = ttk.Button(tree_frame, text="Reject",
                                       command=lambda rentId=rent.id: operate_rent_order("reject", rentId))
            reject_button.grid(row=i, column=len(rent_attributes) + 2)

        if role == 2 and rent.status == "Approved":
            rent_button = ttk.Button(tree_frame, text="Pay", command=lambda carId=rent.id: rent_form_popup(carId))
            rent_button.grid(row=i, column=len(rent_attributes) + 1)
        elif role == 2 and rent.status == "Paid":
            rent_button = ttk.Button(tree_frame, text="Picked Up", command=lambda carId=rent.id: rent_form_popup(carId))
            rent_button.grid(row=i, column=len(rent_attributes) + 1)
        elif role == 2 and rent.status == "Picked Up":
            rent_button = ttk.Button(tree_frame, text="Return Car", command=lambda carId=rent.id: rent_form_popup(carId))
            rent_button.grid(row=i, column=len(rent_attributes) + 1)

def operate_rent_order(option, rentId):
    status = None
    if "approve" == option:
        status = 2
    elif "reject" == option:
        status = -1

    rentManager = RentManager()
    rentManager.update_rental_fields("status",status,"id",rentId)
    messagebox.showinfo("Success", option + " successful!")


def show_car_list(role):
    carManager = CarManager()
    car_data = None
    if role == 1:
        cars = carManager.select_car_fields({"deleted": 0});
        car_data = [Car.create_car_from_tuple(data) for data in cars]
    else:
        cars = carManager.select_car_fields({"deleted": 0, "available_now": 1});
        car_data = [Car.create_car_from_tuple(data) for data in cars]

    # 创建表格框架
    tree_frame = tk.Frame(root, bd=2, relief="groove")
    tree_frame.place(relx=0.05, rely=0.15, anchor=tk.NW, relwidth=0.9, relheight=0.8)

    # 创建表格标题
    columns = ("ID", "Make", "Model", "Year", "Mileage", "Available Now", "Minimum Rent Period", "Maximum Rent Period")
    for i, column in enumerate(columns):
        label = tk.Label(tree_frame, text=column, bd=1, relief="groove")
        label.grid(row=0, column=i, sticky="nsew")

    for i, car in enumerate(car_data, start=1):
        # 将 Car 对象的属性存储到一个列表中，以便用于创建 Label
        car_attributes = [car.id, car.make, car.model, car.year, car.mileage, car.availableNow, car.minRentPeriod,
                          car.maxRentPeriod]

        for j, item in enumerate(car_attributes):
            label = tk.Label(tree_frame, text=item, bd=1, relief="groove")
            label.grid(row=i, column=j, sticky="nsew")

        if role == 1:
            # 创建 Edit 和 Delete 按钮
            edit_button = ttk.Button(tree_frame, text="Edit", command=lambda carId=car.id: edit_car(carId))
            edit_button.grid(row=i, column=len(car_attributes) + 1)

            delete_button = ttk.Button(tree_frame, text="Delete", command=lambda carId=car.id: delete_car(carId))
            delete_button.grid(row=i, column=len(car_attributes) + 2)
            return

        rent_button = ttk.Button(tree_frame, text="Rent", command=lambda carId=car.id: rent_form_popup(carId))
        rent_button.grid(row=i, column=len(car_attributes) + 1)


def rent_form_popup(carId):
    global make_entry, model_entry, year_entry, mileage_entry, min_rent_entry, max_rent_entry, rate_entry, start_date_entry, rent_days_entry
    # 查询车辆信息
    carManager = CarManager()
    car_info = carManager.select_car("id", int(carId))
    car = Car(*car_info)

    # 创建弹出窗口
    rental_window = tk.Toplevel(root)
    rental_window.title("Rent Info")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 400
    window_height = 400
    window_x = (screen_width - window_width) // 2
    window_y = (screen_height - window_height) // 2

    rental_window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    # 车辆基本信息
    make_label = tk.Label(rental_window, text="Make:")
    make_label.grid(row=0, column=0, padx=10, pady=5)
    make_entry = tk.Entry(rental_window)
    make_entry.insert(0, car.make)
    make_entry.configure(state='readonly')
    make_entry.grid(row=0, column=1, padx=10, pady=5)

    model_label = tk.Label(rental_window, text="Model:")
    model_label.grid(row=1, column=0, padx=10, pady=5)
    model_entry = tk.Entry(rental_window)
    model_entry.insert(0, car.model)
    model_entry.configure(state='readonly')
    model_entry.grid(row=1, column=1, padx=10, pady=5)

    year_label = tk.Label(rental_window, text="Year:")
    year_label.grid(row=2, column=0, padx=10, pady=5)
    year_entry = tk.Entry(rental_window)
    year_entry.insert(0, car.year)
    year_entry.configure(state='readonly')
    year_entry.grid(row=2, column=1, padx=10, pady=5)

    mileage_label = tk.Label(rental_window, text="Mileage:")
    mileage_label.grid(row=3, column=0, padx=10, pady=5)
    mileage_entry = tk.Entry(rental_window)
    mileage_entry.insert(0, car.mileage)
    mileage_entry.configure(state='readonly')
    mileage_entry.grid(row=3, column=1, padx=10, pady=5)

    min_rent_label = tk.Label(rental_window, text="Minimum Rent Period:")
    min_rent_label.grid(row=4, column=0, padx=10, pady=5)
    min_rent_entry = tk.Entry(rental_window)
    min_rent_entry.insert(0, car.minRentPeriod)
    min_rent_entry.configure(state='readonly')
    min_rent_entry.grid(row=4, column=1, padx=10, pady=5)

    max_rent_label = tk.Label(rental_window, text="Maximum Rent Period:")
    max_rent_label.grid(row=5, column=0, padx=10, pady=5)
    max_rent_entry = tk.Entry(rental_window)
    max_rent_entry.insert(0, car.maxRentPeriod)
    max_rent_entry.configure(state='readonly')
    max_rent_entry.grid(row=5, column=1, padx=10, pady=5)

    rate_label = tk.Label(rental_window, text="Rate|$/day:")
    rate_label.grid(row=6, column=0, padx=10, pady=5)
    rate_entry = tk.Entry(rental_window)
    rate_entry.insert(0, 100)
    rate_entry.configure(state='readonly')
    rate_entry.grid(row=6, column=1, padx=10, pady=5)

    start_date_label = tk.Label(rental_window, text="Rental Start Day:")
    start_date_label.grid(row=7, column=0, padx=10, pady=5)
    start_date_entry = DateEntry(rental_window)
    start_date_entry.grid(row=7, column=1, padx=10, pady=5)

    rent_days_label = tk.Label(rental_window, text="Rental Days:")
    rent_days_label.grid(row=8, column=0, padx=10, pady=5)
    rent_days_entry = tk.Entry(rental_window)
    rent_days_entry.grid(row=8, column=1, padx=10, pady=5)
    rent_days_entry.config(validate="key", validatecommand=(root.register(validate_number), "%P"))

    # 提交按钮
    submit_button = tk.Button(rental_window, text="Submit", command=lambda: save_rental_data(carId, rental_window))
    submit_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10)


def save_rental_data(carId, rental_window):
    global make_entry, model_entry, year_entry, mileage_entry, min_rent_entry, max_rent_entry, rate_entry, start_date_entry, rent_days_entry

    make = make_entry.get()
    model = model_entry.get()
    year = year_entry.get()
    mileage = mileage_entry.get()
    rate = rate_entry.get()
    start_date_str = start_date_entry.get()
    rent_day = rent_days_entry.get()
    user = get_current_user()

    if not start_date_str or not rent_day:
        messagebox.showerror("Error", "Please enter both start_date and rent_day.")
        return
    rentManager = RentManager()
    rentManager.create_rental_table()

    cost = int(rent_day) * int(rate)
    date_format = "%m/%d/%y"
    start_date = datetime.strptime(start_date_str, date_format).date()

    rentManager.insert_rental((user.id, user.userName, carId, make, model, year, mileage, start_date, rent_day, rate,
                               round(cost, 2), 1, datetime.now(), datetime.now(), 0))

    carManager = CarManager()
    carManager.update_car_field("available_now", 0, "id", carId)

    # 提示保存成功
    tk.messagebox.showinfo("Success", "Rent successful!")
    rental_window.destroy()


def show_form_popup():
    global add_car_window
    add_car_window = tk.Toplevel(root)
    add_car_window.title("Add Car")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 计算位置
    window_width = 400
    window_height = 300
    window_x = (screen_width - window_width) // 2
    window_y = (screen_height - window_height) // 2

    add_car_window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    # ID, make, model, year, mileage, available now, minimum rent period, maximum rent period
    make_label = tk.Label(add_car_window, text="Make:")
    make_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    make_entry = tk.Entry(add_car_window)
    make_entry.grid(row=0, column=1, padx=10, pady=5)

    model_label = tk.Label(add_car_window, text="Model:")
    model_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    model_entry = tk.Entry(add_car_window)
    model_entry.grid(row=1, column=1, padx=10, pady=5)

    year_label = tk.Label(add_car_window, text="Year:")
    year_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    year_entry = tk.Entry(add_car_window)
    year_entry.grid(row=2, column=1, padx=10, pady=5)
    year_entry.config(validate="key", validatecommand=(root.register(validate_number), "%P"))

    mileage_label = tk.Label(add_car_window, text="Mileage:")
    mileage_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    mileage_entry = tk.Entry(add_car_window)
    mileage_entry.grid(row=3, column=1, padx=10, pady=5)
    mileage_entry.config(validate="key", validatecommand=(root.register(validate_number), "%P"))

    radio_var = tk.StringVar()
    radio_var.set(1)
    radio_label = tk.Label(add_car_window, text="Available Now:")
    radio_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    manual_radio = tk.Radiobutton(add_car_window, text="Yes", variable=radio_var, value=1)
    manual_radio.grid(row=4, column=1, padx=(5, 2), pady=5, sticky="w")
    automatic_radio = tk.Radiobutton(add_car_window, text="No", variable=radio_var, value=0)
    automatic_radio.grid(row=4, column=1, padx=(50, 5), pady=5, sticky="w")

    minimum_rent_label = tk.Label(add_car_window, text="Minimum Rent Period:")
    minimum_rent_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    minimum_rent_entry = tk.Entry(add_car_window)
    minimum_rent_entry.grid(row=5, column=1, padx=10, pady=5)
    minimum_rent_entry.config(validate="key", validatecommand=(root.register(validate_number), "%P"))

    maximum_rent_label = tk.Label(add_car_window, text="Maximum Rent Period:")
    maximum_rent_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
    maximum_rent_entry = tk.Entry(add_car_window)
    maximum_rent_entry.grid(row=6, column=1, padx=10, pady=5)
    maximum_rent_entry.config(validate="key", validatecommand=(root.register(validate_number), "%P"))

    submit_button = tk.Button(add_car_window, text="Submit",
                              command=lambda: submit_form(make_entry, model_entry, year_entry, mileage_entry, radio_var,
                                                          minimum_rent_entry, maximum_rent_entry))
    submit_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    cancel_button = tk.Button(add_car_window, text="Cancel", command=add_car_window.destroy)
    cancel_button.grid(row=7, column=1, columnspan=2, padx=10, pady=10)


def validate_number(number):
    return number.isdigit() or number == ""


def submit_form(make_entry, model_entry, year_entry, mileage_entry, radio_var,
                minimum_rent_entry, maximum_rent_entry):
    make = make_entry.get()
    model = model_entry.get()
    year = year_entry.get()
    mileage = mileage_entry.get()
    radio = radio_var.get()
    minimumRent = minimum_rent_entry.get()
    maximumRent = maximum_rent_entry.get()
    print(make, model, year, mileage, radio, minimumRent, maximumRent)
    if not make or not model or not year or not mileage or not radio or not minimumRent or not maximumRent:
        messagebox.showerror("Error", "Please enter complete information.")
        return
    # 保存数据库
    carManager = CarManager();
    carManager.create_car_table()

    carManager.insert_car((make, model, year, mileage, radio, minimumRent, maximumRent, datetime.now(),
                           datetime.now(), 0))
    messagebox.showinfo("Success", "Add car successful!")
    add_car_window.destroy()


def clear_popup():
    popup.destroy()


def show_login_popup(role, type):
    global username_entry, password_entry, popup

    popup = tk.Toplevel(root)

    window_width = 300
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_x = (screen_width - window_width) // 2
    window_y = (screen_height - window_height) // 2

    popup.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    username_frame = ttk.Frame(popup)
    username_frame.pack(padx=10, pady=5)

    username_label = ttk.Label(username_frame, text="Username:")
    username_label.pack(side="left")
    username_entry = ttk.Entry(username_frame)
    username_entry.pack(side="left")

    password_frame = ttk.Frame(popup)
    password_frame.pack(padx=10, pady=5)

    password_label = ttk.Label(password_frame, text="Password:")
    password_label.pack(side="left")
    password_entry = ttk.Entry(password_frame, show="*")
    password_entry.pack(side="left")

    if type == "regist":
        popup.title("Regist")
        register_button = ttk.Button(popup, text="Regist", command=lambda: regist_user(role))
        register_button.pack(padx=10, pady=10)

    if type == "login":
        popup.title("Login")
        login_button = ttk.Button(popup, text="Login", command=lambda: login_user(role))
        login_button.pack(padx=10, pady=10)


def main():
    global root, button1, button2, button3, button4
    root = tk.Tk()
    root.title("Button Window")

    root.protocol("WM_DELETE_WINDOW", on_closing)

    window_width = 1000
    window_height = 700

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_x = (screen_width - window_width) // 2
    window_y = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    # 按钮
    button1 = tk.Button(root, text="administrator regist", command=lambda: show_login_popup(1, "regist"))
    button1.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    button2 = tk.Button(root, text="administrator login", command=lambda: show_login_popup(1, "login"))
    button2.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

    button3 = tk.Button(root, text="customer regist", command=lambda: show_login_popup(2, "regist"))
    button3.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    button4 = tk.Button(root, text="customer login", command=lambda: show_login_popup(2, "login"))
    button4.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

    root.mainloop()


if __name__ == "__main__":
    main()
