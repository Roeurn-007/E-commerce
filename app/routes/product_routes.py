from flask import Blueprint, jsonify, request, render_template
from app import db
from app.models.product import Product
from app.models.category import Category
from sqlalchemy import or_

product_bp = Blueprint("products", __name__)


@product_bp.route("/")
def home():
    featured_products = Product.query.filter_by(is_active=True).limit(8).all()
    return render_template('index.html', products=featured_products)


@product_bp.route("/products")
def get_products():
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', '')

    query = Product.query.filter_by(is_active=True)

    if category_id:
        query = query.filter_by(category_id=category_id)
    if search:
        query = query.filter(or_(
            Product.name.ilike(f'%{search}%'),
            Product.description.ilike(f'%{search}%')
        ))

    products = query.all()
    categories = Category.query.all()

    return render_template('product_list.html', products=products, categories=categories,
                           search=search, category_id=category_id)


@product_bp.route("/products/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.is_active == True
    ).limit(4).all()
    return render_template('product_detail.html', product=product, related_products=related_products)


@product_bp.route("/products/search")
def search_products():
    query = request.args.get('q', '')
    if query:
        products = Product.query.filter(
            or_(
                Product.name.ilike(f'%{query}%'),
                Product.description.ilike(f'%{query}%')
            )
        ).filter_by(is_active=True).all()
    else:
        products = []

    return render_template('search_results.html', products=products, query=query)
