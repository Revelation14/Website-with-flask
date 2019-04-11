from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import os


app=Flask(__name__)



app.config['SECRET_KEY']='d6c9149e1731e8183665f72f2895eb35'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

db=SQLAlchemy(app)

login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USERNAME']=os.environ.get('EMAIL_USERNAME')
app.config['MAIL_PASSWORD']=os.environ.get('EMAIL_PASSWORD')
mail=Mail(app)



from app import routes