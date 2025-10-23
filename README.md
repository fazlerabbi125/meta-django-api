# Project Structure and API Routes

## Introduction
This document provides an overview of the project scope, required API endpoints, and implementation notes for the Little Lemon restaurant API project. It serves as a guide to help you successfully complete the project. Read it carefully and refer to it during development to stay on track.

## Scope
The goal is to create a fully functional API for the Little Lemon restaurant, enabling client application developers to build web and mobile applications. The API will allow users with different roles to:
- Browse, add, and edit menu items
- Place and browse orders
- Assign delivery crew to orders
- Deliver orders

In this project, your APIs need to make it possible for your end-users to perform the following functionalities:

1.	The admin can assign users to the manager group

2.	You can access the manager group with an admin token

3.	The admin can add menu items 

4.	The admin can add categories

5.	Managers can log in 

6.	Managers can update the item of the day

7.	Managers can assign users to the delivery crew

8.	Managers can assign orders to the delivery crew

9.	The delivery crew can access orders assigned to them

10.	The delivery crew can update an order as delivered

11.	Customers can register

12.	Customers can log in using their username and password and get access tokens

13.	Customers can browse all categories 

14.	Customers can browse all the menu items at once

15.	Customers can browse menu items by category

16.	Customers can paginate menu items

17.	Customers can sort menu items by price

18.	Customers can add menu items to the cart

19.	Customers can access previously added items in the cart

20.	Customers can place orders

21.	Customers can browse their own orders

The following sections outline the required endpoints, authorization levels, and additional notes to guide your implementation.

## Structure
Name the project directory `LittleLemon` and create a single Django app named `LittleLemonAPI` to implement all API endpoints. Use `pipenv` to manage dependencies in a virtual environment. Our APIs should be created using Django, DRF and Djoser. You need to use SQLite as the database for this project. 

## Function or Class-Based Views
You may use function-based views, class-based views, or a combination of both. Follow proper API naming conventions throughout the project.

## User Groups
Create the following user groups in the Django admin panel and assign random users to them:
- **Manager**
- **Delivery crew**

Users not assigned to any group are considered **customers**.

## Error Checking and HTTP Status Codes
Implement error messages with appropriate HTTP status codes for the following scenarios:
- Requesting a non-existing resource
- Unauthorized API requests
- Invalid data in POST, PUT, or PATCH requests

| HTTP Status Code | Reason |
|------------------|--------|
| 200 - OK         | For all successful GET, PUT, PATCH, and DELETE calls |
| 201 - Created    | For all successful POST requests |
| 400 - Bad Request| If validation fails for POST, PUT, PATCH, or DELETE calls |
| 401 - Forbidden  | If user authentication fails |
| 403 - Unauthorized | If authorization fails for the current user token |
| 404 - Not Found  | If the request is for a non-existing resource |

## API Endpoints
Below are the required API routes, grouped by category, with their roles, methods, and purposes.

### User Registration and Token Generation Endpoints
Use the Djoser library to implement the following endpoints. Use DRF's built-in Token Authentication.

| Endpoint                | Role                          | Method | Purpose                                                                 |
|-------------------------|-------------------------------|--------|-------------------------------------------------------------------------|
| `/api/users`            | No role required              | POST   | Creates a new user with name, email, and password                       |
| `/api/users/me/`  | Anyone with a valid user token | GET    | Displays the current user                                               |
| `/token/login/`         | Anyone with valid credentials | POST   | Generates access tokens for use in other API calls                      |

### Menu-Items Endpoints

| Endpoint                     | Role                     | Method            | Purpose                                                                 |
|------------------------------|--------------------------|-------------------|-------------------------------------------------------------------------|
| `/api/menu-items`            | Customer, Delivery crew  | GET               | Lists all menu items (200 - OK)                                         |
| `/api/menu-items`            | Customer, Delivery crew  | POST, PUT, PATCH, DELETE | Denies access (403 - Unauthorized)                                      |
| `/api/menu-items/{menuItem}` | Customer, Delivery crew  | GET               | Lists a single menu item                                                |
| `/api/menu-items/{menuItem}` | Customer, Delivery crew  | POST, PUT, PATCH, DELETE | Denies access (403 - Unauthorized)                                      |
| `/api/menu-items`            | Manager                 | GET               | Lists all menu items                                                    |
| `/api/menu-items`            | Manager                 | POST              | Creates a new menu item (201 - Created)                                 |
| `/api/menu-items/{menuItem}` | Manager                 | GET               | Lists a single menu item                                                |
| `/api/menu-items/{menuItem}` | Manager                 | PUT, PATCH        | Updates a single menu item                                              |
| `/api/menu-items/{menuItem}` | Manager                 | DELETE            | Deletes a menu item                                                     |

### User Group Management Endpoints

| Endpoint                               | Role    | Method | Purpose                                                                 |
|----------------------------------------|---------|--------|-------------------------------------------------------------------------|
| `/api/groups/manager/users`            | Manager | GET    | Returns all managers                                                    |
| `/api/groups/manager/users`            | Manager | POST   | Assigns a user to the manager group (201 - Created)                     |
| `/api/groups/manager/users/{userId}`   | Manager | DELETE | Removes a user from the manager group (200 - OK, 404 - Not Found if user not found) |
| `/api/groups/delivery-crew/users`      | Manager | GET    | Returns all delivery crew members                                       |
| `/api/groups/delivery-crew/users`      | Manager | POST   | Assigns a user to the delivery crew group (201 - Created)               |
| `/api/groups/delivery-crew/users/{userId}` | Manager | DELETE | Removes a user from the delivery crew group (200 - OK, 404 - Not Found if user not found) |

### Cart Management Endpoints

| Endpoint                | Role    | Method | Purpose                                                                 |
|-------------------------|---------|--------|-------------------------------------------------------------------------|
| `/api/cart/menu-items`  | Customer | GET    | Returns current items in the cart for the authenticated user            |
| `/api/cart/menu-items`  | Customer | POST   | Adds a menu item to the cart, setting the authenticated user as the owner |
| `/api/cart/menu-items`  | Customer | DELETE | Deletes all menu items in the cart for the authenticated user           |

### Order Management Endpoints

| Endpoint                | Role          | Method            | Purpose                                                                 |
|-------------------------|---------------|-------------------|-------------------------------------------------------------------------|
| `/api/orders`           | Customer      | GET               | Returns all orders with order items created by the authenticated user   |
| `/api/orders`           | Customer      | POST              | Creates a new order with items from the cart, then clears the cart      |
| `/api/orders/{orderId}` | Customer      | GET               | Returns all items for the specified order ID. Returns an error if the order doesn’t belong to the user |
| `/api/orders`           | Manager       | GET               | Returns all orders with order items by all users                        |
| `/api/orders/{orderId}` | Manager       | PUT, PATCH        | Updates the order (e.g., assign delivery crew, update status to 0 or 1) |
| `/api/orders/{orderId}` | Manager       | DELETE            | Deletes the specified order                                             |
| `/api/orders`           | Delivery crew | GET               | Returns all orders assigned to the delivery crew                        |
| `/api/orders/{orderId}` | Delivery crew | PATCH             | Updates the order status to 0 (out for delivery) or 1 (delivered)       |

#### Order Status Notes
- Status = 0: Order is out for delivery (delivery crew assigned).
- Status = 1: Order has been delivered (delivery crew assigned).

## Additional Steps
- Implement filtering, pagination, and sorting for `/api/menu-items` and `/api/orders` endpoints.
- Apply throttling for authenticated and unauthenticated users.