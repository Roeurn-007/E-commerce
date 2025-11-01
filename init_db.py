from app import create_app, db
from app.models.user import User
from app.models.category import Category
from app.models.product import Product


def init_database():
    app = create_app()

    with app.app_context():
        # Drop and create all tables
        db.drop_all()
        db.create_all()

        # Create admin user
        admin = User(
            username='admin',
            email='admin@electronics.com',
            first_name='Admin',
            last_name='User',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # Create regular user
        user = User(
            username='john_doe',
            email='john@example.com',
            first_name='John',
            last_name='Doe'
        )
        user.set_password('password123')
        db.session.add(user)

        # Create categories
        categories = [
            Category(name='Smartphones',
                     description='Latest smartphones and mobile devices'),
            Category(name='Laptops',
                     description='Laptops, notebooks and ultrabooks'),
            Category(name='Tablets', description='Tablets and iPads'),
            Category(name='Headphones',
                     description='Audio devices and headphones'),
            Category(name='Smart Watches', description='Wearable technology'),
            Category(name='Cameras',
                     description='Digital cameras and accessories'),
        ]

        for category in categories:
            db.session.add(category)

        db.session.commit()

        # Create products
        products = [
            # Smartphones
            Product(name='iPhone 15 Pro', description='Latest iPhone with A17 Pro chip and titanium design', price=999.99, stock_quantity=50,
                    image_url='images/iphone15-pro.png', category_id=1, specifications='6.1" Super Retina XDR, 128GB Storage, 5G'),
            Product(name='Samsung Galaxy S24', description='Powerful Android smartphone with advanced camera', price=849.99, stock_quantity=45,
                    image_url='images/galaxy-s24.png', category_id=1, specifications='6.2" Dynamic AMOLED, 256GB Storage, 5G'),
            Product(name='Google Pixel 8', description='Google\'s flagship with best-in-class camera', price=699.99, stock_quantity=30,
                    image_url='images/pixel-8.png', category_id=1, specifications='6.2" OLED, 128GB Storage, Google Tensor G3'),

            # Laptops
            Product(name='MacBook Pro 16"', description='Professional laptop with M3 Pro chip', price=2399.99, stock_quantity=25,
                    image_url='images/macbook-pro-16.png', category_id=2, specifications='16" Liquid Retina XDR, 16GB RAM, 1TB SSD'),
            Product(name='Dell XPS 13', description='Ultra-thin laptop with infinity edge display', price=1199.99, stock_quantity=35,
                    image_url='images/dell-xps-13.png', category_id=2, specifications='13.4" FHD+, Intel Core i7, 16GB RAM, 512GB SSD'),

            # Tablets
            Product(name='iPad Pro 12.9"', description='Professional tablet with M2 chip', price=1099.99, stock_quantity=40,
                    image_url='images/ipad-pro-12-9.png', category_id=3, specifications='12.9" Liquid Retina XDR, 128GB, Wi-Fi + Cellular'),

            # Headphones
            Product(name='Sony WH-1000XM5', description='Industry leading noise canceling headphones', price=399.99, stock_quantity=60,
                    image_url='images/sony-wh1000xm5.png', category_id=4, specifications='30hr battery, Quick Charge, Touch Controls'),

            # Smart Watches
            Product(name='Apple Watch Series 9', description='Advanced smartwatch with health monitoring', price=399.99, stock_quantity=55,
                    image_url='images/apple-watch-series9.png', category_id=5, specifications='45mm, GPS + Cellular, Always-On Retina'),

            # Cameras
            Product(name='Canon EOS R5', description='Professional mirrorless camera', price=3899.99, stock_quantity=15,
                    image_url='images/canon-eos-r5.png', category_id=6, specifications='45MP, 8K Video, 5-axis IBIS'),
        ]

        for product in products:
            db.session.add(product)

        db.session.commit()
        print("✅ Database initialized with sample data!")
        print("👤 Admin login: admin@electronics.com / admin123")
        print("👤 User login: john@example.com / password123")
        print("🚀 Run: python run.py to start the application")


if __name__ == "__main__":
    init_database()

app = create_app()

with app.app_context():
    db.create_all()
