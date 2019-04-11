from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,SubmitField,PasswordField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo
from app.models import User

class LoginForm(FlaskForm):
	email=StringField('Email',validators=[DataRequired(),Email()])
	password=PasswordField('Password',validators=[DataRequired()])
	remember=BooleanField('Remember Me')
	submit=SubmitField('Login')


class RegistrationForm(FlaskForm):
	username=StringField('Username',validators=[DataRequired()])
	email=StringField('Email',validators=[DataRequired(),Email()])
	password=PasswordField('Password',validators=[DataRequired()])
	confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	submit=SubmitField('Register')

	def validate_username(self,username):
		user=User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already taken')

	def validate_email(self,email):
		user=User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email already taken')
	
class ContentForm(FlaskForm):
	fest=StringField('Event Name',validators=[DataRequired()])
	content=TextAreaField('Content',validators=[DataRequired()])
	picture=FileField('Content Image',validators=[FileAllowed(['jpg','png'])])
	post=SubmitField('Post')

class UpdateAccountForm(FlaskForm):
	username=StringField('Username',validators=[DataRequired()])
	email=StringField('Email',validators=[DataRequired(),Email()])
	picture=FileField('Display Picture',validators=[FileAllowed(['jpg','png'])])
	submit=SubmitField('Change')

class ChangePasswordForm(FlaskForm):
	password=PasswordField('Current Password',validators=[DataRequired()])
	new_password=PasswordField('New Password',validators=[DataRequired()])
	confirm_new_password=PasswordField('Confirm New Password',validators=[DataRequired(),EqualTo('new_password')])
	submit=SubmitField('Confirm')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

