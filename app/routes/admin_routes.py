from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order, OrderItem
from app.models.user import User
from app import db
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)


def admin_required(func):
    from functools import wraps

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Admin access required!", "danger")
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return decorated_view

# Dashboard


@admin_bp.route('/admin/dashboard')
@login_required
@admin_required
def dashboard():
    products_count = Product.query.count()
    categories_count = Category.query.count()
    orders_count = Order.query.count()
    users_count = User.query.count()

    # Get recent users (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_users_count = User.query.filter(User.created_at >= week_ago).count()

    # Get active users (users who have placed orders)
    active_users_count = db.session.query(User).join(Order).distinct().count()

    # Get recent orders for display
    recent_orders = Order.query.order_by(
        Order.created_at.desc()).limit(5).all()

    # Get recent users for display
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                           products_count=products_count,
                           categories_count=categories_count,
                           orders_count=orders_count,
                           users_count=users_count,
                           recent_users_count=recent_users_count,
                           active_users_count=active_users_count,
                           recent_orders=recent_orders,
                           recent_users=recent_users)

# User Management


@admin_bp.route('/admin/users')
@login_required
@admin_required
def manage_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/manage_users.html', users=users)


@admin_bp.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    # Prevent admin from deleting themselves
    if user_id == current_user.id:
        flash('You cannot delete your own account!', 'danger')
        return redirect(url_for('admin.manage_users'))

    user = User.query.get_or_404(user_id)

    try:
        # Delete associated data first (carts, wishlists, orders)
        from app.models.cart import Cart
        from app.models.wishlist import Wishlist
        from app.models.order import Order

        # Delete cart items
        Cart.query.filter_by(user_id=user_id).delete()

        # Delete wishlist items
        Wishlist.query.filter_by(user_id=user_id).delete()

        # For orders, you might want to keep them for records
        # But if you want to delete them too:
        # Order.query.filter_by(user_id=user_id).delete()

        # Now delete the user
        db.session.delete(user)
        db.session.commit()

        flash(f'User {user.username} has been deleted successfully!', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'danger')

    return redirect(url_for('admin.manage_users'))


# Product Management


@admin_bp.route('/admin/products')
@login_required
@admin_required
def manage_products():
    products = Product.query.all()
    return render_template('admin/manage_products.html', products=products)


@admin_bp.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    if request.method == 'POST':
        try:
            product = Product(
                name=request.form.get('name'),
                description=request.form.get('description'),
                price=float(request.form.get('price')),
                stock_quantity=int(request.form.get('stock_quantity')),
                category_id=int(request.form.get('category_id')),
                image_url=request.form.get(
                    'image_url') or 'images/main_product.png',
                specifications=request.form.get('specifications', '')
            )

            db.session.add(product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('admin.manage_products'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding product: {str(e)}', 'danger')

    categories = Category.query.all()
    return render_template('admin/add_product.html', categories=categories)


@admin_bp.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        try:
            product.name = request.form.get('name')
            product.description = request.form.get('description')
            product.price = float(request.form.get('price'))
            product.stock_quantity = int(request.form.get('stock_quantity'))
            product.category_id = int(request.form.get('category_id'))
            product.image_url = request.form.get(
                'image_url') or 'images/main_product.png'
            product.specifications = request.form.get('specifications', '')

            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('admin.manage_products'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating product: {str(e)}', 'danger')

    categories = Category.query.all()
    return render_template('admin/edit_product.html', product=product, categories=categories)


@admin_bp.route('/admin/products/delete/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    try:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting product: {str(e)}', 'danger')

    return redirect(url_for('admin.manage_products'))

# Category Management


@admin_bp.route('/admin/categories')
@login_required
@admin_required
def manage_categories():
    categories = Category.query.all()
    return render_template('admin/manage_categories.html', categories=categories)


@admin_bp.route('/admin/categories/add', methods=['POST'])
@login_required
@admin_required
def add_category():
    try:
        category = Category(
            name=request.form.get('name'),
            description=request.form.get('description', '')
        )

        db.session.add(category)
        db.session.commit()
        flash('Category added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding category: {str(e)}', 'danger')

    return redirect(url_for('admin.manage_categories'))


@admin_bp.route('/admin/categories/edit/<int:category_id>')
@login_required
@admin_required
def edit_category(category_id):
    editing_category = Category.query.get_or_404(category_id)
    categories = Category.query.all()
    return render_template('admin/manage_categories.html',
                           categories=categories,
                           editing_category=editing_category)


@admin_bp.route('/admin/categories/update/<int:category_id>', methods=['POST'])
@login_required
@admin_required
def update_category(category_id):
    category = Category.query.get_or_404(category_id)

    try:
        category.name = request.form.get('name')
        category.description = request.form.get('description', '')

        db.session.commit()
        flash('Category updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating category: {str(e)}', 'danger')

    return redirect(url_for('admin.manage_categories'))


@admin_bp.route('/admin/categories/delete/<int:category_id>', methods=['POST'])
@login_required
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)

    try:
        # Check if category has products
        if category.products:
            flash('Cannot delete category that has products. Please reassign or delete the products first.', 'danger')
        else:
            db.session.delete(category)
            db.session.commit()
            flash('Category deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting category: {str(e)}', 'danger')

    return redirect(url_for('admin.manage_categories'))

# Order Management


@admin_bp.route('/admin/orders')
@login_required
@admin_required
def manage_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/manage_orders.html', orders=orders)


@admin_bp.route('/admin/orders/<int:order_id>')
@login_required
@admin_required
def view_order(order_id):
    # Eager load order items and products
    order = Order.query.options(
        joinedload(Order.items).joinedload(OrderItem.product)
    ).get_or_404(order_id)

    return render_template('admin/view_order.html', order=order)


@admin_bp.route('/admin/orders/<int:order_id>/status/<string:status>')
@login_required
@admin_required
def update_order_status(order_id, status):
    order = Order.query.get_or_404(order_id)

    try:
        order.status = status
        db.session.commit()
        flash(f'Order status updated to {status}!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating order status: {str(e)}', 'danger')

    return redirect(url_for('admin.manage_orders'))
