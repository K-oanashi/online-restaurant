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
- Place orders through checkout
- Store orders in PostgreSQL
- Manage dishes and orders through Django Admin

## Technologies Used

- **Backend:** Python, Django
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Development Environment:** PyCharm

## How to Run the Project

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install the required packages:

   `pip install -r requirements.txt`

4. Set up the PostgreSQL database and configure the connection in `config/settings.py`.
5. Apply database migrations:

   `python manage.py migrate`

6. Start the Django development server:

   `python manage.py runserver`

7. Open `http://127.0.0.1:8000/` in your browser.

**Note:** The PostgreSQL database and its existing records are not automatically included when cloning the repository.

## About the Project

This project was created to practice Django backend development, database relationships, user authentication, session-based shopping carts, and order management.

The restaurant focuses on traditional Georgian cuisine and provides a simple interface for browsing and ordering dishes.