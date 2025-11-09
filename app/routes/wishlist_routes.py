
from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.wishlist import Wishlist
from app.models.product import Product

wishlist_bp = Blueprint("wishlist", __name__)


@wishlist_bp.route("/wishlist")
@login_required
def get_wishlist():
    # Use join to get product data efficiently
    wishlist_items = (Wishlist.query
                      .filter_by(user_id=current_user.id)
                      .join(Product)
                      .all())
    return render_template('wishlist.html', wishlist_items=wishlist_items)


@wishlist_bp.route("/wishlist/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_wishlist(product_id):
    product = Product.query.get_or_404(product_id)

    existing = Wishlist.query.filter_by(
        user_id=current_user.id, product_id=product_id).first()
    if existing:
        flash('Product is already in your wishlist!', 'info')
        return redirect(request.referrer or url_for('products.get_products'))

    wishlist_item = Wishlist(user_id=current_user.id, product_id=product_id)
    db.session.add(wishlist_item)
    db.session.commit()

    flash('Product added to your wishlist!', 'success')
    return redirect(request.referrer or url_for('products.get_products'))


@wishlist_bp.route("/wishlist/remove/<int:product_id>", methods=["POST"])
@login_required
def remove_from_wishlist(product_id):
    wishlist_item = Wishlist.query.filter_by(
        user_id=current_user.id, product_id=product_id).first()
    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()
        flash('Product removed from your wishlist!', 'success')
    else:
        flash('Product not found in your wishlist!', 'error')

    return redirect(url_for('wishlist.get_wishlist'))
