from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, SellItemForm, PurchaseItemForm
from market import db
from market import bcrypt
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')
  
@app.route('/about')
def about_page():
    return 'About Page'
  
@app.route('/market', methods=["GET", "POST"])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    
    if request.method == "POST":
        # purchasing item logic
       purchased_item = request.form.get('purchased_item')
       p_item_object = Item.query.filter_by(name=purchased_item).first()
       if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
            
                flash(f'Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$', category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')
       
       # selling item logic
       sold_item = request.form.get('sold_item')
       if not sold_item:
           return redirect(url_for('market_page'))
       s_item_object = Item.query.filter_by(name=sold_item).first()
       if s_item_object:
           if current_user.can_sell(s_item_object):
               s_item_object.sell(current_user)
               flash(f'Congratulations! You sold {s_item_object.name} for {s_item_object.price}$', category='success')
           else:
               flash(f"Something went wrong with selling {s_item_object.name}", category='danger')
       return redirect(url_for('market_page'))
        
    
    if request.method == "GET":
        items = Item.query.filter_by(owner=current_user.id)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, selling_form=selling_form, owned_items=owned_items)
    

@app.route('/register', methods=["GET", "POST"])

def register_page():
    form = RegisterForm()
    
    if form.validate_on_submit():
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f'Account created successfully! You are logged in as: {user.username}', category="success")
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are errors in the form fields
        for err_message in form.errors.values():
            flash(f'There was an error in creating a user: {err_message}', category='danger')
            
    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password_correction(attempted_password=form.password.data):
           login_user(user)
           flash(f'Success! You are logged in as: {user.username}', category="success")
           return redirect(url_for('market_page'))
        else:
           flash('Incorrect username or password', category="danger")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    
    flash("You have been logged out!", category="info")
    return redirect(url_for('home_page'))