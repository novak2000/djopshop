import os
import secrets
from PIL import Image
from flask import url_for, render_template, redirect, flash, request
from djop.forms import RegistrationForm, LoginForm, UpdatePhoto , UpdateProfile
from djop import db,app,bcript, login_manager,admin
from djop.models import Product, User, Category
from flask_login import login_user,logout_user, login_required, current_user
from flask_admin.contrib.sqla import ModelView


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Category, db.session))

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/contact')
def contactUs():
    return render_template('contactUs.html', title='Contact Us')

def findCategories(product):
    temp=[]
    now = Category.query.filter_by(id=product.category).first()
    while now:
        temp.insert(0,now.name)
        now = Category.query.filter_by(id=now.parentCategory).first()
    return temp

@app.route('/store', methods=['GET','POST'])
@login_required
def store():
    page = request.args.get('page', 1, type=int)
    products= Product.query.order_by(Product.name.asc()).paginate(page=page, per_page = 6)
    categories = []
    x= len(Product.query.all())
    total_pages = x//6 + (x%6 > 0)
    for product in products.items:
        productCategories = findCategories(product)
        productCategories.pop()
        categories.append(productCategories)
    return render_template('store.html', title='Store', articles=enumerate(products.items), total_pages=total_pages, page=page, products=products, categories=categories)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        passwordhash = bcript.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=passwordhash, email=form.email.data,firm_name=form.firm_name.data,address=form.address.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account is created,now you can log in.', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', title='Signup', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcript.check_password_hash(user.password,form.password.data):
            login_user(user, remember = form.rememberMe.data, force=True)
            flash(f'You are now loged in!', 'success')
            nextpage = request.args.get('next')
            if nextpage:
                return redirect(nextpage)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'incorect email or password', 'danger')
    return render_template('login.html', title='Log in', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

def savePhoto(photo_file):
    photoHex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(photo_file.filename)
    picture_fn = photoHex + f_ext
    picture_path = os.path.join(app.root_path,'static/images/profile/',picture_fn)
    
    output_size = (250,250)
    i = Image.open(photo_file)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route('/account', methods  =['POST','GET'])
@login_required
def account():
    formPhoto = UpdatePhoto()
    formProfile = UpdateProfile()
    if formProfile.validate_on_submit():
        current_user.username = formProfile.username.data
        current_user.email = formProfile.email.data
        current_user.address = formProfile.address.data
        current_user.firm_name = formProfile.firm_name.data
        db.session.commit()
        flash('Your account has been updated successfuly!', 'success')
        return redirect(url_for('account'))
    elif formPhoto.validate_on_submit():
        current_user.image = savePhoto(formPhoto.photo.data)
        db.session.commit()
        flash('Your photo has been updated successfuly!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        formProfile.username.data = current_user.username
        formProfile.email.data = current_user.email
        formProfile.address.data = current_user.address
        formProfile.firm_name.data = current_user.firm_name

    return render_template('account.html', title = 'Account', formPhoto = formPhoto, form=formProfile)

@app.route('/product/<int:product_id>')
@login_required
def product(product_id):
    p = Product.query.get_or_404(product_id)
    productCategories = findCategories(p)
    productCategories.pop()
    return render_template('product.html', title= p.name, product=p, productCategories=productCategories)