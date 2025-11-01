from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.order import Order, OrderItem
from app.models.cart import Cart
from app.models.product import Product
import uuid
from sqlalchemy.orm import joinedload

order_bp = Blueprint("orders", __name__)


@order_bp.route("/orders/place", methods=["GET", "POST"])
@login_required
def place_order():
    if request.method == "POST":
        shipping_address = request.form.get("shipping_address")
        payment_method = request.form.get("payment_method", "Cash on Delivery")

        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        if not cart_items:
            flash("Your cart is empty!", "warning")
            return redirect(url_for('cart.get_cart'))

        total_amount = sum(item.product.price *
                           item.quantity for item in cart_items)
        order_number = str(uuid.uuid4())[:8].upper()

        new_order = Order(
            user_id=current_user.id,
            order_number=order_number,
            total_amount=total_amount,
            shipping_address=shipping_address,
            payment_method=payment_method,
            payment_status="pending"
        )
        db.session.add(new_order)
        db.session.commit()

        for item in cart_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.product.price,
                total_price=item.product.price * item.quantity
            )
            db.session.add(order_item)

            product = Product.query.get(item.product_id)
            product.stock_quantity -= item.quantity
            db.session.delete(item)

        db.session.commit()
        flash(f"Order placed successfully! Order #: {order_number}", "success")
        return render_template('checkout.html', order_number=order_number)

    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash("Your cart is empty!", "warning")
        return redirect(url_for('cart.get_cart'))

    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('place_order.html', cart_items=cart_items, total=total)


@order_bp.route("/orders")
@login_required
def get_user_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(
        Order.created_at.desc()).all()
    return render_template('order_history.html', orders=orders)


@order_bp.route("/orders/<int:order_id>")
@login_required
def get_order_details(order_id):
    # FIXED: Eager load order items and products
    order = Order.query.options(
        joinedload(Order.items).joinedload(OrderItem.product)
    ).filter_by(id=order_id, user_id=current_user.id).first_or_404()

    return render_template('order_details.html', order=order)
