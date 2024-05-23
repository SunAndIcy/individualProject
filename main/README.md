## Car_Rental_System

### Description:
> This is a car rental system based on CUI. Administrators can manage vehicles through the backend, and customers can view currently available vehicles and select vehicles for rental. Customers can also choose the rental time and duration.

### Programming Language:
> Python

### Database:
>SQLite

### Version Control:
>Git

### Module Description：

#### 1.view module
>The entry class for the program is typically referred to as the "main class"
#### 2.manager module
>The layer responsible for the logic processing of the program is commonly referred to as the "business logic layer" 
#### 3.dao module
>The layer responsible for managing objects and database operations is commonly referred to as the "data access layer"

### How To Usage
#### Run the application:

```python 
python index.py
```
#### Account
> Admin Account:
> 1. account number: admin1 | password: 123456
> 2. account number: admin2 | password: 123456
> 
> Customer Account:
> 1. account number: customer1 | password: 123456

#### Admin operation steps
> ![img.png](home.png)
> 1. admin user can choose Admin Register or Admin Login
> 2. if admin user login
> 
> ![img.png](admin_menu.png)
> 1. if admin user View Cars 
> 
> ![img.png](admin_view_cars.png)
> 1.1 admin user can Edit Car or Delete Car
> 
> ![img.png](admin_operate_car.png)
> 2. if admin user Add Car
> 
> ![img.png](admin_add_car.png)
> 3. if admin user Rent Order Review
> 
> ![img.png](admin_rent_order_review.png)
> 3.1 if the order status equal Pending Review, admin user can Approve Rent Order or Reject Rent Order
>
> ![img.png](admin_operate_rent_order.png)

#### Customer operation steps
> ![img.png](home.png)
> 
> 1. customer can choose Customer Register or Customer Login
> 2. if customer login
> 
> ![img.png](customer_menu.png)
> 
> 1. if customer View Cars (customer only can view Available now equal Yes)
> ![img.png](customer_view_cars.png)
>
> 1.1 customer can Rent A Car
> 
> ![img.png](customer_rent_car.png)
> 
> 1.2 if customer Rent A Car
>   
> 2. if customer select My Rent Order
>   
> ![img_1.png](enter_car_id.png)
>
> 2.1 customer can view all customer's rent oders
> ![img.png](my_rent_oder.png)
> 
> 2.2 customer can Pay Rent Order
> 
> ![img_1.png](pay_rent_order.png)
>

### About the Feature

Our car rental system has fully encapsulated the core interfaces and functionalities. This means that users can easily interact with the system whether it's through a Command-Line Interface (CLI) or a Graphical User Interface (GUI).

This encapsulation brings several advantages:

- **Flexibility and Scalability:** Encapsulation of core functionalities makes the system more flexible and scalable. We can seamlessly switch between interaction modes, from CLI to GUI, without needing to modify the core functionalities.
  
- **Cost-Effectiveness:** With the core functionalities already encapsulated, future development efforts can focus solely on designing and optimizing the interface, significantly saving on development costs and time.
  
- **Enhanced User Experience:** Users can choose the interaction mode that best suits their preferences and habits, thereby enhancing user experience and satisfaction.

This approach allows our car rental system to operate flexibly in different environments and scenarios, providing users with consistent, high-quality service.





