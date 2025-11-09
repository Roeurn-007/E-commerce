# TechHub - Electronics E-Commerce Platform

![MoneTech](https://img.shields.io/badge/MoneTech-Electronics%20Store-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)

A modern, full-featured e-commerce platform built with Flask for selling electronics and gadgets.

## 🚀 Features

### User Features
- **User Authentication** - Secure registration and login system
- **Product Browsing** - Browse products with search and filter capabilities
- **Shopping Cart** - Add, update, and remove items from cart
- **Wishlist** - Save products for later
- **Order Management** - Place orders and track order history
- **Product Reviews** - View detailed product information and specifications

### Admin Features
- **Dashboard** - Overview of products, categories, and orders
- **Product Management** - Add, edit, and delete products
- **Category Management** - Manage product categories
- **Order Management** - View and update order status
- **Inventory Management** - Track stock levels

## 🛠️ Technology Stack

- **Backend**: Flask 2.3.3
- **Database**: SQLite (with SQLAlchemy ORM)
- **Authentication**: Flask-Login with Bcrypt
- **Frontend**: Bootstrap 5, Jinja2 Templates
- **Icons**: Font Awesome

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Setup

1. **Clone or Download the Project**
   ```bash
   git clone <https://github.com/Roeurn-007/E-commerce.git>
   cd monetch
   ```

2. **Create Virtual Environment**
    ```bash
    python -m venv venv

    # On Windows
    venv\Scripts\activate

    # On macOS/Linux
    source venv/bin/activate
   ```
3. **Install Dependencies**
    ```bash
        pip install -r requirements.txt
    ```
4. **Initialize Database**
    ```bash
    python init_db.py
    ```
5. **Run Application**
    ```bash
    python run.py
    ```

## 👤 Default Accounts

### Admin Account
- **Email** : admin@electronics.com

- **Password** : admin123

### Test User Account
- **Email** : john@example.com

- **Password** : password123
