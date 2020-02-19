from datetime import datetime
from djop import db,login_manager
from flask_login import UserMixin,current_user
from flask_admin.contrib.sqla import ModelView

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable = False, unique=True)
    email = db.Column(db.String(100), nullable = False, unique=True)
    password = db.Column(db.String(25), nullable = False)
    firm_name = db.Column(db.String(60), nullable = False)
    address = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    image = db.Column(db.String(30), nullable=False, default = 'default.jpg')

    def __repr__(self):
        return f'user-{self.name}'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    parentCategory = db.Column(db.Integer, nullable=False, default = 0)
    products = db.relationship('Product', backref='category_all' , lazy=True)

    def __repr__(self):
        return f'Category-{self.name}'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    description = db.Column(db.String(300), nullable=False, unique=True)
    category = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(20), nullable=False, default='default.png')