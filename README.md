# Turing Back End Challenge
[![Build Status](https://travis-ci.com/Nta1e/Turing_backend_challenge.svg?token=QAfgj3KstfQjsmX6MRX8&branch=dev)](https://travis-ci.com/Nta1e/Turing_backend_challenge)


## Description
 This the backend of the turing E commerce application built with Django
The documentation of the API can be found [here](https://turing-backend-shadik.herokuapp.com/docs/)

## The project has the following routes

| REQUEST | ROUTE | FUNCTIONALITY |
| ------- | ----- | ------------- |
| *POST* | ```/customers``` | _Register new Customer_|
| *POST* | ```/customers/login``` | _Customer login_|
| *POST* | ```/customers/facebook``` | _Facebook Login_|
| *GET* | ```/customer``` | _Get Customer Details_|
| *PUT* | ```/customer/update``` | _Update Customer Details_|
| *PUT* | ```/customer/address``` | _Update Customer Address_ |
| *PUT* | ```/customer/creditCard``` | _Update Customer Credit Card_|
| *GET* | ```/shoppingcart/generateUniqueId``` | _Generate Shopping Cart ID_|
| *POST* | ```/shoppingcart/add``` | _Add product to cart_|
| *GET* | ```/shoppingcart/<cart_id>``` | _Get products in cart_|
| *PUT* | ```/shoppingcart/update/<item_id>``` | _Update Product Quantity_|
| *DELETE* | ```/shoppingcart/empty/<cart_id>``` | _Empty cart_|
| *DELETE* | ```/shoppingcart/removeProduct/<product_id>``` | _Remove item from cart_|
| *GET* | ```/products``` | _Retrieve products_|
| *GET* | ```/products/search?name=''&&description=''``` | _Search products_|
| *GET* | ```/products/<product_id>``` | _Get Single Product_|
| *GET* | ```/products/inCategory/{category_id}``` | _Get products in category_|
| *GET* | ```/products/inDepartment/<department_id>``` | _Get products in department_|
| *GET* | ```/products/reviews``` | _Get Products Reviews_|
| *GET* | ```/products/<product_id>/reviews``` | _Get Product Reviews_|
| *POST* | ```/orders``` | _Place an order_|
| *PUT* | ```/orders/<order_id>``` | _Get Single order_ |
| *GET* | ```/orders/InCustomer``` | _Get Customer Orders_|
| *GET* | ```/orders/shortDetail/<order_id>``` | _Get Order Short Detail_|
| *GET* | ```/categories``` | _Get Product Category_|
| *GET* | ```/categories/<category_id>``` | _Get Single Category_|
| *GET* | ```/categories/inProduct/{product_id}``` | _Get Product Category_|
| *GET* | ```/categories/inDepartment/<department_id>``` | _Get categories in department_|
| *GET* | ```/departments``` | _Get departments_ |
| *GET* | ```/departments/<department_id>``` | _Get Department_|
| *GET* | ```/attributes``` | _Get Attributes_|
| *GET* | ```/attributes/<attribute_id>``` | _Get Single Attribute_|
| *GET* | ```/attributes/values/<attribute_id>``` | _Get Attribute Values_|
| *GET* | ```/attributes/inProduct/<product_id>``` | _Get Product Attributes_|
| *GET* | ```/tax``` | _Get all taxes_|
| *GET* | ```/tax/<tax_id>``` | _Get single tax_ |
| *GET* | ```/shipping/regions``` | _Get shipping Regions_|
| *GET* | ```/shipping/regions/{shipping_region_id}``` | _Get region shippings_|
| *POST* | ```/stripe/charge``` | _Stripe Payment_|


## BUILT WITH

* Django - Python Web Framework
* Django Rest FrameWork - Web API Framework for Django

## SETTING UP APPLICATION
1. Install mysql


clone the repository and change directory to the `src` folder

**```git clone https://github.com/Nta1e/Turing_backend_challenge.git```**

**```cd Turing_backend_challenge && cd src```**


3. Create a virtual environment that you are going to use while running the application locally

    **```$ python3 -m venv env```**

    **```$ source  env/bin/activate```**

4. Install all project dependencies using

    **```pip3 install -r requirements.txt```**

5. Create tables and dump data into the database using the following command

    **``` mysql -u <user> -D <database> -p < ./src/sql/database.sql```**

6. Make Migrations

    **```python manage.py migrate auth && python manage.py migrate```**

7. Run the application
    **```python3 manage.py runserver```**

## Author

*Ntale Shadik*
