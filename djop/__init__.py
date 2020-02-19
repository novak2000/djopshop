from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DIFAULT'] = 0

app.config['SECRET_KEY'] = 'tvarTLNrgiAtmgeEdcgdzQ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\novak\\Desktop\\programiranje\\projekti\\vezbanje\\djop\\data.db'
db = SQLAlchemy(app)

bcript = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='Djop')

from djop import routes