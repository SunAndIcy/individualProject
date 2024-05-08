from main.manager.user_manager import UserManager
from main.manager.car_manager import CarManager
from main.module.user import User
from main.module.car import Car
from datetime import datetime
from main.manager.rent_manager import RentManager
from main.module.rent_order import RentOrder
import threading
import sys

local_data = threading.local()


def set_current_user(user):
    local_data.user = user


def get_current_user():
    return getattr(local_data, 'user', None)


def on_closing():
    user = get_current_user()
    if user:
        print(f"User {user.userName} logged out.")
        del local_data.user


def set_login_user(user):
    set_current_user(user)
    print(f"User {user.userName} logged in.")


class CarRentalSystem:

    def register(self, role):
        print(f"\n{role} Registration:")
        username = input("Enter username: ")
        password = input("Enter password: ")

        if not username or not password:
            print("Please enter both username and password!")
            return

        # 在这里添加保存用户信息的逻辑
        userManager = UserManager()
        userManager.create_user_table()

        user = userManager.select_user_fields({"user_name": username, "role": role});

        if user:
            print("The user is exit, Please login.")
            return

        userManager.insert_user((username, password, datetime.now(), datetime.now(), role, 0))
        print("Registration successful!")

    def login(self, role):
        print("Please Login:")
        username = input("Please Enter username: ")
        password = input("Please Enter password: ")

        if not username or not password:
            print("Please enter both username and password!")
            return

        userManager = UserManager()
        result = userManager.select_user_fields({"user_name": username, "role": role});

        if not result:
            print("The user is not exit, Please regist!")
            return

        user = User(*result)

        if password != user.password:
            print("The password is not correct, Please try again!")
            return

        set_login_user(user)

        # admin menu
        if role == 1:
            self.admin_menu(role)
            return
        # customer menu
        self.customer_menu(role)

    def customer_menu(self, role):
        while True:
            print("\nCustomer Menu")
            print("1. View Cars")
            print("2. My Rent Order")
            print("3. Back To Home")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_cars(role)
            elif choice == "2":
                self.my_rent_order(role)
            elif choice == "3":
                self.start()
                break
            else:
                print("Invalid choice. Please try again.")

    def my_rent_order(self, role):
        rentManager = RentManager()
        rentManager.create_rental_table()
        rent_data = None
        user = get_current_user()
        rent_cars = rentManager.select_rental_fields({"deleted": 0, "user_id": user.id});
        rent_data = [RentOrder.create_rental_from_tuple(data) for data in rent_cars]

        # 创建标题
        columns = (
            "ID", "UserName", "Make", "Model", "Year", "Mileage", "Rental Start Day", "Rental Days", "Rate", "Cost",
            "Status")
        # 输出标题
        field_width = 16
        formatted_title = "|"
        for field in columns:
            formatted_title += f"{field:^{field_width}}|"
        print(formatted_title)
        print("-" * 190)
        for i, rent in enumerate(rent_data, start=1):
            # 将 Rent 对象的属性存储到一个列表中，以便用于布局
            rent_attributes = [rent.id, rent.userName, rent.make, rent.model, rent.year, rent.mileage,
                               rent.rentalStartDay,
                               rent.rentalDays,
                               rent.rate, rent.cost, rent.status]
            formatted_value = "|"
            for value in rent_attributes:
                formatted_value += f"{value:^{field_width}}|"
            print(formatted_value)
            print("-" * 190)

        self.rent_order_option(role)

    def admin_menu(self, role):
        while True:
            print("\nAdmin Menu")
            print("1. View Cars")
            print("2. Add Car")
            print("3. Rent Order Review")
            print("4. Back To Home")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_cars(role)
            elif choice == "2":
                self.add_car()
            elif choice == "3":
                self.show_rent_list(role)
            elif choice == "4":
                self.start()
                break
            else:
                print("Invalid choice. Please try again.")

    def show_rent_list(self, role):
        rentManager = RentManager()
        rentManager.create_rental_table()
        rent_data = None

        rent_cars = rentManager.select_rental_fields({"deleted": 0});
        rent_data = [RentOrder.create_rental_from_tuple(data) for data in rent_cars]

        # 创建标题
        columns = (
            "ID", "UserName", "Make", "Model", "Year", "Mileage", "Rental Start Day", "Rental Days", "Rate", "Cost",
            "Status")
        # 输出标题
        field_width = 16
        formatted_title = "|"
        for field in columns:
            formatted_title += f"{field:^{field_width}}|"
        print(formatted_title)
        print("-" * 190)
        for i, rent in enumerate(rent_data, start=1):
            # 将 Rent 对象的属性存储到一个列表中，以便用于布局
            rent_attributes = [rent.id, rent.userName, rent.make, rent.model, rent.year, rent.mileage,
                               rent.rentalStartDay,
                               rent.rentalDays,
                               rent.rate, rent.cost, rent.status]
            formatted_value = "|"
            for value in rent_attributes:
                formatted_value += f"{value:^{field_width}}|"
            print(formatted_value)
            print("-" * 190)

        self.rent_order_option(role)

    def rent_order_option(self, role):
        if role == 1:
            self.admin_rent_order_option(role)
        else:
            self.customer_rent_order_option(role)

    def customer_rent_order_option(self, role):
        while True:
            print("\nOperate Rent Order List")
            print("1. Pay Rent Order")
            print("2. Back To Customer Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.pay_rent_order(role)
            elif choice == "2":
                self.customer_menu(role)
                break
            else:
                print("Invalid choice. Please try again.")

    def pay_rent_order(self, role):
        print("\nPlease enter you want to pay rent order id")
        rent_id = input("Enter rent order id: ")
        if not rent_id.isdigit():
            print("\nThe rent order id isn't correct, Please enter the correct rent order id")
            self.pay_rent_order(role)
        rentManager = RentManager()
        rent_info = rentManager.select_rental("id", int(rent_id))

        if rent_info is None:
            print("\nThe rent order isn't exit, Please enter the correct rent order id")
            self.pay_rent_order(role)

        rentOrder = RentOrder(*rent_info)
        if rentOrder.status == "Paid":
            print(f"The rent order is {rentOrder.status}.")
            self.my_rent_order(role)

        if rentOrder.status != "Approved":
            print(f"The rent order is {rentOrder.status}, only the |Approved| status can be paied.")
            self.pay_rent_order(role)

        rentManager.update_rental_fields("status", 3, "id", rentOrder.id)
        print("Rent order paied successfully!")

    def admin_rent_order_option(self, role):
        while True:
            print("\nOperate Rent Order List")
            print("1. Approve Rent Order")
            print("2. Reject Rent Order")
            print("3. Back To Admin Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.approve_rent_order(role)
            elif choice == "2":
                self.reject_rent_order(role)
            elif choice == "3":
                self.admin_menu(role)
                break
            else:
                print("Invalid choice. Please try again.")

    def approve_rent_order(self, role):
        print("\nPlease enter you want to approve rent order id")
        rent_id = input("Enter rent order id: ")
        if not rent_id.isdigit():
            print("\nThe rent order id isn't correct, Please enter the correct rent order id")
            self.approve_rent_order(role)
        rentManager = RentManager()
        rent_info = rentManager.select_rental("id", int(rent_id))

        if rent_info is None:
            print("\nThe rent order isn't exit, Please enter the correct rent order id")
            self.approve_rent_order(role)

        rentOrder = RentOrder(*rent_info)
        if rentOrder.status != "Pending Review":
            print(f"The rent order is {rentOrder.status}, only the |Pending Review| status can be approved.")
            self.approve_rent_order(role)

        rentManager.update_rental_fields("status", 2, "id", rentOrder.id)
        print("Rent order approved successfully!")

    def reject_rent_order(self, role):
        print("\nPlease enter you want to reject rent order id")
        rent_id = input("Enter rent order id: ")
        if not rent_id.isdigit():
            print("\nThe rent order id isn't correct, Please enter the correct rent order id")
            self.reject_rent_order(role)
        rentManager = RentManager()
        rent_info = rentManager.select_rental("id", int(rent_id))

        if rent_info is None:
            print("\nThe rent order isn't exit, Please enter the correct rent order id")
            self.reject_rent_order(role)

        rentOrder = RentOrder(*rent_info)
        if rentOrder.status != "Pending Review":
            print(f"The rent order is {rentOrder.status}, only the |Pending Review| status can be approved.")
            self.reject_rent_order(role)

        rentManager.update_rental_fields("status", -1, "id", rentOrder.id)
        print("Rent order rejected successfully!")

    def view_cars(self, role):
        carManager = CarManager()
        user = get_current_user()
        car_data = None
        if role == 1:
            carRes = carManager.select_car_fields({"deleted": 0, "user_id": user.id});
            car_data = [Car.create_car_from_tuple(data) for data in carRes]
        else:
            carRes = carManager.select_car_fields({"deleted": 0, "available_now": 1});
            car_data = [Car.create_car_from_tuple(data) for data in carRes]

        if not car_data:
            print("No cars available, Please add car!")

        title = ["ID", "Make", "Model", "Year", "Mileage", "Available now", "Rate $/day", "MinRentPeriod",
                 "MaxRentPeriod"]
        # 输出标题
        field_width = 14
        formatted_title = "|"
        for field in title:
            formatted_title += f"{field:^{field_width}}|"
        print(formatted_title)
        print("-" * 150)
        for i, car in enumerate(car_data, start=1):
            # 将 Car 对象的属性存储到一个列表中，以便用于布局
            car_attributes = [car.id, car.make, car.model, car.year, car.mileage, car.availableNow, car.rate,
                              car.minRentPeriod,
                              car.maxRentPeriod]
            formatted_value = "|"
            for value in car_attributes:
                formatted_value += f"{value:^{field_width}}|"
            print(formatted_value)
            print("-" * 150)
        if role == 1:
            self.admin_edit_option(role)
            return

        self.customer_option(role)

    def customer_option(self, role):
        while True:
            print("\nOperate Car List")
            print("1. Rent A Car")
            print("2. Back To Customer Menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.rent_car(role)
            elif choice == "2":
                self.customer_menu(role)
                break
            else:
                print("Invalid choice. Please try again.")

    def rent_car(self, role):
        print("\nPlease enter you want to rent car id")
        car_id = input("Enter car id: ")
        if not car_id.isdigit():
            print("\nThe car id isn't correct, Please enter the correct car id")
            self.rent_car(role)
        carManager = CarManager()
        car_info = carManager.select_car("id", int(car_id))
        if car_info is None:
            print("\nThe car isn't exit, Please enter the correct car id")
            self.rent_car(role)
        car = Car(*car_info)

        if car.availableNow == "No":
            print("\nThe car isn't available now, Please select another car")
            self.rent_car(role)

        field_width = 14
        title = ["ID", "Make", "Model", "Year", "Mileage", "Available now", "Rate $/day", "MinRentPeriod",
                 "MaxRentPeriod"]
        formatted_title = "|"
        for field in title:
            formatted_title += f"{field:^{field_width}}|"
        print(formatted_title)
        print("-" * 130)
        car_attributes = [car.id, car.make, car.model, car.year, car.mileage, car.availableNow, car.rate,
                          car.minRentPeriod,
                          car.maxRentPeriod]
        formatted_value = "|"
        for value in car_attributes:
            formatted_value += f"{value:^{field_width}}|"
        print(formatted_value)
        print("-" * 130)
        # 编辑属性
        startDay = input("Enter rent start day like |2024-05-10|: ")
        days = input("Enter rent days like |10|: ")

        if not startDay or not days:
            print("Please enter complete information.")
            self.rent_car(role)

        # 保存数据库
        rentManager = RentManager();
        rentManager.create_rental_table()

        user = get_current_user()
        cost = int(days) * int(car.rate)
        date_format = "%Y-%m-%d"
        start_date = datetime.strptime(startDay, date_format).date()

        current_date = datetime.now().date()
        if current_date > start_date:
            print("The start day should behind the current day!")
            self.rent_car(role)

        if int(days) > car.maxRentPeriod or int(days) < car.minRentPeriod:
            print("The rent days should bigger than minRentPeriod and less than maxRentPeriod!")
            self.rent_car(role)

        rentManager.insert_rental(
            (
                user.id, user.userName, car.id, car.make, car.model, car.year, car.mileage, start_date, int(days),
                car.rate,
                round(cost, 2), 1, datetime.now(), datetime.now(), 0))

        print("Rent car successfully!")
        self.my_rent_order(role)

    def admin_edit_option(self, role):
        while True:
            print("\nOperate Car List")
            print("1. Edit Car")
            print("2. Delete Car")
            print("3. Back To Admin Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.edit_car(role)
            elif choice == "2":
                self.delete_car(role)
            elif choice == "3":
                self.admin_menu(role)
                break
            else:
                print("Invalid choice. Please try again.")

    def edit_car(self, role):
        print("\nPlease enter you want to edit car id")
        car_id = input("Enter car id: ")
        if not car_id.isdigit():
            print("\nThe car id isn't correct, Please enter the correct car id")
            self.edit_car(role)
        user = get_current_user()
        carManager = CarManager()
        car_info = carManager.select_car("id", int(car_id), "user_id", user.id)
        if car_info is None:
            print("\nThe car isn't exit, Please enter the correct car id")
            self.edit_car(role)
        car = Car(*car_info)

        field_width = 14
        title = ["ID", "Make", "Model", "Year", "Mileage", "Available now", "Rate $/day", "MinRentPeriod",
                 "MaxRentPeriod"]
        formatted_title = "|"
        for field in title:
            formatted_title += f"{field:^{field_width}}|"
        print(formatted_title)
        print("-" * 130)
        car_attributes = [car.id, car.make, car.model, car.year, car.mileage, car.availableNow, car.rate,
                          car.minRentPeriod,
                          car.maxRentPeriod]
        formatted_value = "|"
        for value in car_attributes:
            formatted_value += f"{value:^{field_width}}|"
        print(formatted_value)
        print("-" * 130)
        # 编辑属性
        make = input("Edit car make like |BMW|: ")
        model = input("Edit car model like |325li|: ")
        year = input("Edit car year like |2023|: ")
        mileage = input("Edit car mileage like |1000|: ")
        rate = input("Edit car rate|$/day like |200|: ")
        available = input("Edit car available now like |Yes/No|: ")
        radio = None
        if available == "Yes":
            radio = 1
        if available == "No":
            radio = 0
        minimumRent = input("Edit car minimum rent period like |10|: ")
        maximumRent = input("Edit car maximum rent period like |30|: ")

        updateFields = {}
        if bool(make):
            updateFields['make'] = make
        if bool(model):
            updateFields['model'] = model
        if bool(year):
            updateFields['year'] = int(year)
        if bool(mileage):
            updateFields['mileage'] = int(mileage)
        if bool(rate):
            updateFields['rate'] = int(rate)
        if radio is not None:
            updateFields['available_now'] = radio
        if bool(minimumRent):
            updateFields['minimum_rent_period'] = int(minimumRent)
        if bool(maximumRent):
            updateFields['maximum_rent_period'] = int(maximumRent)
        print(updateFields)

        carManager.update_car_fields(updateFields, "id", car.id)
        self.view_cars(role)

    def delete_car(self, role):
        print("\nPlease enter you want to delete car id")
        car_id = input("Enter car id: ")
        if not car_id.isdigit():
            print("\nThe car id isn't correct, Please enter the correct car id")
            self.delete_car(role)
        user = get_current_user()
        carManager = CarManager()
        car_info = carManager.select_car("id", int(car_id), "user_id", user.id)
        if car_info is None:
            print("\nThe car isn't exit, Please enter the correct car id")
            self.delete_car(role)

        carManager.update_car_field("deleted", 1, "id", car_id)
        print("Car deleted successfully!")
        self.view_cars(role)

    def add_car(self):
        make = input("Enter car make like |BMW|: ")
        model = input("Enter car model like |325li|: ")
        year = input("Enter car year like |2023|: ")
        mileage = input("Enter car mileage like |1000|: ")
        rate = input("Enter car rate|$/day like |200|: ")
        available = input("Enter car available now like |Yes/No|: ")
        radio = 0
        if available == "Yes":
            radio = 1
        minimumRent = input("Enter car minimum rent period like |10|: ")
        maximumRent = input("Enter car maximum rent period like |30|: ")

        if not make or not model or not year or not mileage or not radio or not minimumRent or not maximumRent:
            print("Please enter complete information.")
            self.add_car()
        # 保存数据库
        carManager = CarManager();
        carManager.create_car_table()

        user = get_current_user()
        carManager.insert_car((make, model, year, mileage, radio, minimumRent, maximumRent, datetime.now(),
                               datetime.now(), 0, rate, user.id))
        self.view_cars(user.role)
        print("Car added successfully!")

    def start(self):
        global flag
        flag = False
        while True:
            print("\nWelcome To Car Rental System")
            print("1. Admin Register")
            print("2. Admin Login")
            print("3. Customer Register")
            print("4. Customer Login")
            print("5. Exit")
            choice = input("Please Enter your choice: ")

            if choice == "1":
                self.register(1)
            elif choice == "2":
                self.login(1)
            elif choice == "3":
                self.register(2)
            elif choice == "4":
                self.login(2)
            elif choice == "5":
                print("Bye Bye...")
                on_closing()
                sys.exit()
            else:
                print("Invalid choice. Please enter the correct choice.")


if __name__ == "__main__":
    car_rental_system = CarRentalSystem()
    car_rental_system.start()
