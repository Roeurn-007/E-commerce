from flask import Blueprint, send_file, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from functools import wraps
from flask_login import login_required, current_user

file_bp = Blueprint('files', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in current_app.config['ALLOWED_EXTENSIONS']


def save_uploaded_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to make filename unique
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename

        upload_folder = current_app.config['UPLOAD_FOLDER']
        filepath = os.path.join(current_app.root_path, upload_folder, filename)
        file.save(filepath)

        return f"uploads/{filename}"  # Return relative path
    return None


@file_bp.route('/download/order/<int:order_id>')
@login_required
def download_order(order_id):
    from app.models.order import Order, OrderItem  # Added OrderItem import
    from app import db
    from sqlalchemy.orm import joinedload
    import csv
    import io

    # Check if user has permission to view this order
    order = Order.query.options(
        joinedload(Order.items).joinedload(OrderItem.product)
    ).filter_by(id=order_id).first_or_404()

    if not current_user.is_admin and order.user_id != current_user.id:
        return "Unauthorized", 403

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(['Order Details'])
    writer.writerow(['Order Number', order.order_number])
    writer.writerow(
        ['Order Date', order.created_at.strftime('%Y-%m-%d %H:%M')])
    writer.writerow(['Total Amount', f"${order.total_amount:.2f}"])
    writer.writerow(['Status', order.status])
    writer.writerow(['Payment Status', order.payment_status])
    writer.writerow(['Shipping Address', order.shipping_address])
    writer.writerow([])

    # Write items header
    writer.writerow(['Order Items'])
    writer.writerow(['Product', 'Quantity', 'Unit Price', 'Total Price'])

    # Write items
    for item in order.items:
        product_name = item.product.name if item.product else f"Product #{item.product_id}"
        writer.writerow([
            product_name,
            item.quantity,
            f"${item.unit_price:.2f}",
            f"${item.total_price:.2f}"
        ])

    writer.writerow([])
    writer.writerow(['Grand Total', '', '', f"${order.total_amount:.2f}"])

    # Create response
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        as_attachment=True,
        download_name=f"order_{order.order_number}.csv",
        mimetype='text/csv'
    )


@file_bp.route('/download/users')
@login_required
def download_users():
    if not current_user.is_admin:
        return "Admin access required", 403

    from app.models.user import User
    import csv
    import io

    users = User.query.all()

    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(['ID', 'Username', 'Email', 'Full Name',
                    'Role', 'Registration Date', 'Order Count'])

    # Write data
    for user in users:
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        role = "Admin" if user.is_admin else "Customer"
        order_count = len(user.orders) if user.orders else 0

        writer.writerow([
            user.id,
            user.username,
            user.email,
            full_name,
            role,
            user.created_at.strftime('%Y-%m-%d'),
            order_count
        ])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        as_attachment=True,
        download_name="users_list.csv",
        mimetype='text/csv'
    )


@file_bp.route('/download/orders')
@login_required
def download_orders():
    if not current_user.is_admin:
        return "Admin access required", 403

    from app.models.order import Order
    import csv
    import io

    orders = Order.query.all()

    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(['Order ID', 'Order Number', 'Customer',
                    'Date', 'Total Amount', 'Status', 'Payment Status'])

    # Write data
    for order in orders:
        customer_name = order.user.username if order.user else 'Guest'

        writer.writerow([
            order.id,
            order.order_number,
            customer_name,
            order.created_at.strftime('%Y-%m-%d %H:%M'),
            f"${order.total_amount:.2f}",
            order.status,
            order.payment_status
        ])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        as_attachment=True,
        download_name="orders_list.csv",
        mimetype='text/csv'
    )
