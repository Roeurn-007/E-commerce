from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.cart import Cart
from app.models.product import Product

cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/cart")
@login_required
def get_cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)


@cart_bp.route("/cart/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    if product.stock_quantity <= 0:
        flash("Sorry, this product is out of stock!", "danger")
        return redirect(request.referrer or url_for('products.get_products'))

    cart_item = Cart.query.filter_by(
        user_id=current_user.id, product_id=product.id).first()

    if cart_item:
        if cart_item.quantity + 1 > product.stock_quantity:
            flash(
                f"Only {product.stock_quantity} items available in stock!", "warning")
        else:
            cart_item.quantity += 1
            flash("Product quantity updated in cart!", "success")
    else:
        cart_item = Cart(user_id=current_user.id,
                         product_id=product.id, quantity=1)
        db.session.add(cart_item)
        flash("Product added to cart!", "success")

    db.session.commit()
    return redirect(request.referrer or url_for('products.get_products'))


@cart_bp.route("/cart/update/<int:cart_id>", methods=["POST"])
@login_required
def update_cart_item(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)
    if cart_item.user_id != current_user.id:
        flash("Unauthorized action!", "danger")
        return redirect(url_for('cart.get_cart'))

    quantity = request.form.get('quantity', type=int)
    if quantity and quantity > 0:
        if quantity > cart_item.product.stock_quantity + cart_item.quantity:
            flash(
                f"Only {cart_item.product.stock_quantity} items available in stock!", "warning")
        else:
            cart_item.quantity = quantity
            db.session.commit()
            flash("Cart updated!", "success")
    else:
        flash("Invalid quantity!", "danger")

    return redirect(url_for('cart.get_cart'))


@cart_bp.route("/cart/remove/<int:cart_id>", methods=["POST"])
@login_required
def remove_cart_item(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)
    if cart_item.user_id != current_user.id:
        flash("Unauthorized action!", "danger")
        return redirect(url_for('cart.get_cart'))

    db.session.delete(cart_item)
    db.session.commit()
    flash("Item removed from cart!", "success")
    return redirect(url_for('cart.get_cart'))
