# 🛍️ Simple E-Commerce Store

This is a Django-based web application for a simple e-commerce store. It includes user authentication, product listing, shopping cart, and basic frontend UI.

## 🚀 Features

- User Registration & Login
- Product Listing (Add/Edit/Delete via Admin Panel)
- Shopping Cart Functionality
- Add to Cart / Remove from Cart
- Django Admin Dashboard
- Responsive UI

## 🛠️ Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript (Bootstrap)
- **Database:** SQLite (default with Django)
- **Version Control:** Git & GitHub

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/likhithamuddala/CodeAlpha_simple-ecommerce-store.git

# Navigate into the project
cd simple-ecommerce-store/ecommerce

# (Optional) Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Run the server
python manage.py runserver
