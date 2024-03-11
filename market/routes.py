from market import app
from flask import render_template, redirect, url_for, flash
from market.models import Item, User
from market.forms import RegisterForm
from market import db
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')
  
@app.route('/about')
def about_page():
    return 'About Page'
  
@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)


@app.route('/register', methods=["GET", "POST"])

def register_page():
    form = RegisterForm()
    
    if form.validate_on_submit():
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    password_hash=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are errors in the form fields
        for err_message in form.errors.values():
            flash(f'There was an error in creating a user: {err_message}')
            
    return render_template('register.html', form=form)