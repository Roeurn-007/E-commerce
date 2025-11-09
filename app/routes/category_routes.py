from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.category import Category

category_bp = Blueprint("categories", __name__)

@category_bp.route("/categories")
def get_all_categories():
    categories = Category.query.all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "description": c.description,
        "parent_id": c.parent_id
    } for c in categories])

@category_bp.route("/categories/create", methods=["POST"])
@login_required
def create_category():
    if not current_user.is_admin:
        flash("Admin access required!", "danger")
        return redirect(url_for('products.home'))
    
    name = request.form.get("name")
    description = request.form.get("description")
    
    if Category.query.filter_by(name=name).first():
        flash("Category already exists!", "danger")
        return redirect(url_for('admin.manage_categories'))
    
    new_cat = Category(name=name, description=description)
    db.session.add(new_cat)
    db.session.commit()
    
    flash("Category created successfully!", "success")
    return redirect(url_for('admin.manage_categories'))