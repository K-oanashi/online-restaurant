# ცისფერი მთები 🍽️
### Online Georgian Restaurant

**ცისფერი მთები** is an online Georgian restaurant application developed using Django and PostgreSQL as part of a college backend development project.

The website allows users to browse Georgian dishes, filter them by different criteria, add dishes to a shopping cart, and place orders.

## Features

- Browse Georgian dishes by category
- Filter dishes by category, spiciness (0–4), walnuts, and vegetarian options
- View dish images, prices, and ingredient information
- Add dishes to the shopping cart
- Increase, decrease, or remove items from the cart
- Automatically calculate the total order price
- Register, log in, and log out
- Support shopping carts for both guests and registered users
- Store shopping carts and cart items in PostgreSQL
- Place orders through checkout
- Store orders and order items in PostgreSQL
- Manage dishes and orders through Django Admin

## Technologies Used

- **Backend:** Python, Django
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Development Environment:** PyCharm
- **Version Control:** Git, GitHub

## Django Applications

The project is organized into two main Django applications:

### Restaurant Application

The `restaurant` application handles:

- Dish categories and menu
- Dish filtering
- Shopping carts and cart items
- Quantity management
- Checkout and order processing

### Users Application

The `users` application handles:

- User registration
- User login
- User logout
- Authentication using Django's built-in User model

## Shopping Cart Implementation

The shopping cart is implemented using Django's `Cart` and `CartItem` models, with data stored in PostgreSQL instead of Django sessions.

- **Registered users:** Shopping carts are associated with their user accounts.
- **Guest users:** Shopping carts are identified using a unique token stored in a browser cookie.
- **Checkout:** Orders and order items are saved to PostgreSQL, and purchased items are removed from the cart.

## How to Run the Project

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install the required packages:

   `pip install -r requirements.txt`

4. Create a PostgreSQL database and configure the database connection and required environment variables.
5. Apply database migrations:

   `python manage.py migrate`

6. Start the Django development server:

   `python manage.py runserver`

7. Open `http://127.0.0.1:8000/` in your browser.

**Note:** The PostgreSQL database and its existing records are not automatically included when cloning the repository. Environment variables must also be configured locally.

## About the Project

This project was created to practice Django backend development, PostgreSQL database relationships, user authentication, database-based shopping carts, and order management.

The restaurant focuses on traditional Georgian cuisine and provides a simple interface for browsing and ordering dishes.