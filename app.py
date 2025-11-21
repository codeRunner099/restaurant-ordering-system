from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "change_this_secret_key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "restaurant.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_menu_data():
    conn = get_db_connection()
    categories = conn.execute("SELECT id, name FROM category ORDER BY name").fetchall()
    items = conn.execute("SELECT id, name, description, price, category_id FROM menu_item WHERE is_available = 1 ORDER BY category_id, name").fetchall()
    conn.close()
    items_by_category = {}
    for c in categories:
        items_by_category[c["id"]] = {
            "id": c["id"],
            "name": c["name"],
            "items": []
        }
    for i in items:
        if i["category_id"] in items_by_category:
            items_by_category[i["category_id"]]["items"].append(i)
    return list(items_by_category.values())


def get_cart():
    if "cart" not in session:
        session["cart"] = {"items": []}
    return session["cart"]


def save_cart(cart):
    session["cart"] = cart
    session.modified = True


def add_to_cart(menu_item_id, quantity):
    conn = get_db_connection()
    item = conn.execute("SELECT id, name, price FROM menu_item WHERE id = ? AND is_available = 1", (menu_item_id,)).fetchone()
    conn.close()
    if not item:
        return
    cart = get_cart()
    found = False
    for entry in cart["items"]:
        if entry["menu_item_id"] == item["id"]:
            entry["quantity"] += quantity
            found = True
            break
    if not found:
        cart["items"].append({
            "menu_item_id": item["id"],
            "name": item["name"],
            "price": float(item["price"]),
            "quantity": quantity
        })
    save_cart(cart)


def clear_cart():
    session["cart"] = {"items": []}
    session.modified = True


def cart_totals(cart):
    total_quantity = 0
    total_price = 0.0
    for entry in cart["items"]:
        total_quantity += entry["quantity"]
        total_price += entry["quantity"] * float(entry["price"])
    return total_quantity, round(total_price, 2)


@app.route("/")
def index():
    categories = get_menu_data()
    cart = get_cart()
    total_quantity, total_price = cart_totals(cart)
    return render_template("index.html", categories=categories, cart_quantity=total_quantity, cart_total=total_price)


@app.route("/menu")
def menu():
    categories = get_menu_data()
    cart = get_cart()
    total_quantity, total_price = cart_totals(cart)
    return render_template("menu.html", categories=categories, cart_quantity=total_quantity, cart_total=total_price)


@app.route("/cart")
def cart_view():
    cart = get_cart()
    total_quantity, total_price = cart_totals(cart)
    return render_template("cart.html", cart=cart, cart_quantity=total_quantity, cart_total=total_price)


@app.route("/cart/add", methods=["POST"])
def cart_add():
    menu_item_id = int(request.form.get("menu_item_id", "0"))
    quantity = int(request.form.get("quantity", "1"))
    if quantity < 1:
        quantity = 1
    add_to_cart(menu_item_id, quantity)
    return redirect(url_for("cart_view"))


@app.route("/cart/update", methods=["POST"])
def cart_update():
    cart = get_cart()
    updated_items = []
    for entry in cart["items"]:
        key = f"quantity_{entry['menu_item_id']}"
        if key in request.form:
            try:
                quantity = int(request.form.get(key, "1"))
            except ValueError:
                quantity = 1
            if quantity > 0:
                entry["quantity"] = quantity
                updated_items.append(entry)
    cart["items"] = updated_items
    save_cart(cart)
    return redirect(url_for("cart_view"))


@app.route("/cart/clear", methods=["POST"])
def cart_clear():
    clear_cart()
    return redirect(url_for("cart_view"))


@app.route("/order/submit", methods=["POST"])
def order_submit():
    cart = get_cart()
    total_quantity, total_price = cart_totals(cart)
    if total_quantity == 0:
        return redirect(url_for("menu"))
    customer_name = request.form.get("customer_name", "").strip()
    table_number = request.form.get("table_number", "").strip()
    if not customer_name:
        customer_name = "Gast"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customer_order (created_at, table_number, customer_name, status, total_amount) VALUES (?, ?, ?, ?, ?)",
        (datetime.utcnow().isoformat(), table_number, customer_name, "offen", total_price)
    )
    order_id = cursor.lastrowid
    for entry in cart["items"]:
        cursor.execute(
            "INSERT INTO order_item (order_id, menu_item_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
            (order_id, entry["menu_item_id"], entry["quantity"], entry["price"])
        )
    conn.commit()
    conn.close()
    clear_cart()
    return redirect(url_for("order_success", order_id=order_id))


@app.route("/order/success/<int:order_id>")
def order_success(order_id):
    return render_template("order_success.html", order_id=order_id)


@app.route("/admin/orders")
def admin_orders():
    conn = get_db_connection()
    orders = conn.execute(
        "SELECT id, created_at, table_number, customer_name, status, total_amount FROM customer_order ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return render_template("admin_orders.html", orders=orders)


if __name__ == "__main__":
    app.run(debug=True)