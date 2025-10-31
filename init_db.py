from app import create_app, db


def init_database():

    app = create_app()

    with app.app_context():
        # Clear existing data and create tables
        db.drop_all()
        db.create_all()
        print("🗃️  Database tables created")

        # Create users
        create_users()

        # Create categories and products
        create_categories_and_products()

        print("✅ Database initialized with sample data!")
        print("\n📋 Login Credentials:")
        print("   👤 Admin:  admin@electronics.com / admin123")
        print("   👤 User:   john@example.com / password123")
        print("\n🚀 Start the application: python run.py")


def create_users():
    """Create admin and regular user accounts"""
    users_data = [
        {
            'username': 'admin',
            'email': 'admin@electronics.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'password': 'admin123',
            'is_admin': True
        },
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123',
            'is_admin': False
        }
    ]

    for user_data in users_data:
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            is_admin=user_data['is_admin']
        )
        user.set_password(user_data['password'])
        db.session.add(user)

    db.session.commit()
    print("👥 User accounts created")


def create_categories_and_products():
    """Create product categories and sample products"""
    # Define categories
    categories_data = [
        {
            'name': 'Smartphones',
            'description': 'Latest smartphones and mobile devices'
        },
        {
            'name': 'Laptops',
            'description': 'Laptops, notebooks and ultrabooks'
        },
        {
            'name': 'Tablets',
            'description': 'Tablets and iPads'
        },
        {
            'name': 'Headphones',
            'description': 'Audio devices and headphones'
        },
        {
            'name': 'Smart Watches',
            'description': 'Wearable technology'
        },
        {
            'name': 'Cameras',
            'description': 'Digital cameras and accessories'
        },
    ]

    # Create categories and store their IDs
    category_ids = {}
    for category_data in categories_data:
        category = Category(
            name=category_data['name'],
            description=category_data['description']
        )
        db.session.add(category)
        db.session.flush()  # Get the ID without committing
        category_ids[category_data['name']] = category.id

    db.session.commit()
    print("📂 Product categories created")

    # Define products
    products_data = [
        # Smartphones (Category ID: 1)
        {
            'name': 'iPhone 15 Pro',
            'description': 'Latest iPhone with A17 Pro chip and titanium design',
            'price': 999.99,
            'stock_quantity': 50,
            'image_url': 'images/iphone15-pro.png',
            'category_id': category_ids['Smartphones'],
            'specifications': '6.1" Super Retina XDR, 128GB Storage, 5G'
        },
        {
            'name': 'Samsung Galaxy S24',
            'description': 'Powerful Android smartphone with advanced camera',
            'price': 849.99,
            'stock_quantity': 45,
            'image_url': 'images/galaxy-s24.png',
            'category_id': category_ids['Smartphones'],
            'specifications': '6.2" Dynamic AMOLED, 256GB Storage, 5G'
        },
        {
            'name': 'Google Pixel 8',
            'description': 'Google\'s flagship with best-in-class camera',
            'price': 699.99,
            'stock_quantity': 30,
            'image_url': 'images/pixel-8.png',
            'category_id': category_ids['Smartphones'],
            'specifications': '6.2" OLED, 128GB Storage, Google Tensor G3'
        },

        # Laptops (Category ID: 2)
        {
            'name': 'MacBook Pro 16"',
            'description': 'Professional laptop with M3 Pro chip',
            'price': 2399.99,
            'stock_quantity': 25,
            'image_url': 'images/macbook-pro-16.png',
            'category_id': category_ids['Laptops'],
            'specifications': '16" Liquid Retina XDR, 16GB RAM, 1TB SSD'
        },
        {
            'name': 'Dell XPS 13',
            'description': 'Ultra-thin laptop with infinity edge display',
            'price': 1199.99,
            'stock_quantity': 35,
            'image_url': 'images/dell-xps-13.png',
            'category_id': category_ids['Laptops'],
            'specifications': '13.4" FHD+, Intel Core i7, 16GB RAM, 512GB SSD'
        },

        # Tablets (Category ID: 3)
        {
            'name': 'iPad Pro 12.9"',
            'description': 'Professional tablet with M2 chip',
            'price': 1099.99,
            'stock_quantity': 40,
            'image_url': 'images/ipad-pro-12-9.png',
            'category_id': category_ids['Tablets'],
            'specifications': '12.9" Liquid Retina XDR, 128GB, Wi-Fi + Cellular'
        },

        # Headphones (Category ID: 4)
        {
            'name': 'Sony WH-1000XM5',
            'description': 'Industry leading noise canceling headphones',
            'price': 399.99,
            'stock_quantity': 60,
            'image_url': 'images/sony-wh1000xm5.png',
            'category_id': category_ids['Headphones'],
            'specifications': '30hr battery, Quick Charge, Touch Controls'
        },

        # Smart Watches (Category ID: 5)
        {
            'name': 'Apple Watch Series 9',
            'description': 'Advanced smartwatch with health monitoring',
            'price': 399.99,
            'stock_quantity': 55,
            'image_url': 'images/apple-watch-series9.png',
            'category_id': category_ids['Smart Watches'],
            'specifications': '45mm, GPS + Cellular, Always-On Retina'
        },

        # Cameras (Category ID: 6)
        {
            'name': 'Canon EOS R5',
            'description': 'Professional mirrorless camera',
            'price': 3899.99,
            'stock_quantity': 15,
            'image_url': 'images/canon-eos-r5.png',
            'category_id': category_ids['Cameras'],
            'specifications': '45MP, 8K Video, 5-axis IBIS'
        },
    ]

    # Create products
    for product_data in products_data:
        product = Product(**product_data)
        db.session.add(product)

    db.session.commit()
    print("📦 Sample products created")


if __name__ == "__main__":
    init_database()
