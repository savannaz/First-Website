from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.product import Product

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
            "id":session['user_id']
    }
    return render_template('cart.html', my_cart=Product.items_in_cart(data),  user=User.get_by_id(data))

@app.route('/remove/cart/item', methods=['POST'])
def remove_product_from_cart():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "user_id":session['user_id'],
        "product_id": request.form['id']
    }
    Product.remove_product_from_cart(data)
    return redirect('/cart')

@app.route('/cart/item/add_to_db', methods=['POST'])
def add_item_to_cart():
    data ={
        "user_id":session['user_id'],
        "product_id": request.form['id']
    }
    Product.add_to_cart(data)
    return redirect('/cart')

@app.route('/shop')
def index():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('shop.html', all_products=Product.all_products(), user=User.get_by_id(data))

@app.route('/product/new')
def new_product():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_product.html', user=User.get_by_id(data))

@app.route('/product/add_to_db',methods=['POST'])
def add_product_to_db():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Product.validate_product(request.form):
        return redirect('/product/new')
    data ={ 
        "label": request.form['label'],
        "price": request.form['price'],
        "description": request.form['description'],
        "category": request.form['category'],
        "quantity": request.form['quantity'],
        "user_id": session['user_id']
    }
    Product.save_product(data)

    return redirect('/dashboard')

@app.route('/edit/product/<int:id>')
def edit_product_in_db(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_product.html",edit=Product.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/product',methods=['POST'])
def update_product():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Product.validate_product(request.form):
        return redirect('/new/recipe')
    data = {
        "label": request.form['label'],
        "price": request.form['price'],
        "description": request.form['description'],
        "category": request.form['category'],
        "quantity": request.form['quantity'],
        "id": request.form['id']
    }
    Product.update(data)
    return redirect('/dashboard')

@app.route('/view/product/<int:id>')
def view_product_in_db (id):
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("view_product.html",product=Product.get_one(data),user=User.get_by_id(user_data))

@app.route('/delete/product/<int:id>')
def delete_product_from_db(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Product.destroy(data)
    return redirect('/dashboard')

