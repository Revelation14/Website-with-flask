from flask import Flask,flash,render_template,url_for,redirect,request
from app.forms import LoginForm,ResetPasswordForm,RequestResetForm,RegistrationForm,ContentForm,UpdateAccountForm,ChangePasswordForm
from app import app,db,mail
from app.models import User,Post
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
import bcrypt,os,secrets
from flask_mail import Message

#posts=[{"Fest":"Accolade","Data":"The college of technology presents to you our cultural fest Accolade 2019 where we organize our events","image":"background.jpg"},
#{"Fest":"Fest 2","Data":"The college of technology presents to you our cultural fest 2019 where we organize our events","image":"etc.jpg"}]

#members_log=[{"Name":"Member 1","Contact":"9999999999","image":"1.jpg"},{"Name":"Member 2","Contact":"9999999999","image":"2.jpg"},{"Name":"Member 3","Contact":"9999999999","image":"3.jpg"}]
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(403)
def update_error(e):
    return render_template("403.html")

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html")



def delete_picture(image):
	image_path=os.path.join(app.root_path,'static/images',image)
	if os.path.exists(image_path):
		os.remove(image_path)
		print('deleted')


def save_picture(form_picture):
	random_hex=secrets.token_hex(8)
	_,f_ext=os.path.splitext(form_picture.filename)
	picture_fn=random_hex+f_ext
	picture_path=os.path.join(app.root_path,'static/images',picture_fn)
	form_picture.save(picture_path)

	return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='dreamoutloud014@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route("/")
def home():
	posts=Post.query.all()
	return render_template('home.html',posts=posts,title='Home')

@app.route('/about/')
def about():
	return render_template('about.html',title='About Us')

@app.route('/gallery/')
def gallery():
	return render_template('gallery.html',title='Gallery')

@app.route('/members/', methods=['GET','POST'])
def members():
	form=LoginForm()
	if request.method=='POST':
		login()
	members_log=User.query.all()
	return render_template('members.html',title='Members',member=members_log,form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
	print(current_user.is_authenticated)
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.checkpw(form.password.data.encode(),user.password.encode()):
			flash('Login Successful','success')
			#return redirect(url_for('home'))
			login_user(user, remember=form.remember.data)
			next_page=request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password','danger')
	return render_template('login.html',title='Login',form=form)

@app.route('/write_content/', methods=['GET','POST'])
@login_required
def content():
	form=ContentForm()
	if form.validate_on_submit():
		print(form.fest.data)
		print(form.picture.data)
		picture_file=save_picture(form.picture.data)
		post=Post(fest=form.fest.data,content=form.content.data,image_file=picture_file)
		db.session.add(post)
		db.session.commit()
		flash('Content Posted','success')
		return redirect(url_for('home'))
	return render_template('content.html',title='Content',form=form)

@app.route('/change_password/',methods=['GET','POST'])
@login_required
def change_password():
	form=ChangePasswordForm()
	if current_user.is_authenticated:
		if form.validate_on_submit():
			if bcrypt.checkpw(form.password.data.encode(),current_user.password.encode()):
				hashed_password=bcrypt.hashpw(form.new_password.data.encode(),bcrypt.gensalt()).decode('utf-8')
				current_user.password=hashed_password
				db.session.commit()
				flash('Your Password is changed','success')
				return redirect(url_for('update_info'))
			else:
				flash('Wrong current password! Try again!!!','danger')
	return render_template('change_password.html',title='Change Password',form=form)

@app.route('/update/content/<int:post_id>',methods=['GET','POST'])
@login_required
def update_content(post_id):
	post=Post.query.get_or_404(post_id)
	form=ContentForm()
		
	if form.validate_on_submit():
		post.fest=form.fest.data
		post.content=form.content.data
		if form.picture.data:
			delete_picture(post.image_file)
			picture_file=save_picture(form.picture.data)
			post.image_file=picture_file
		db.session.commit()
		flash('Your Content Has been updated','success')
		return redirect(url_for('home'))
	elif request.method=='GET':
		form.fest.data=post.fest
		form.content.data=post.content
	return render_template('content.html',title='Update Content',form=form)

@app.route('/delete/post/<int:post_id>',methods=['GET','POST'])
@login_required
def delete_post(post_id):
	post=Post.query.get_or_404(post_id)
	delete_picture(post.image_file)
	db.session.delete(post)
	db.session.commit()
	flash('Post has been deleted','success')
	return redirect(url_for('home'))

@app.route('/account/',methods=['GET','POST'])
@login_required
def update_info():
	form=UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			delete_picture(current_user.image_file)
			picture_file=save_picture(form.picture.data)
			current_user.image_file=picture_file
		current_user.username=form.username.data
		current_user.email=form.email.data
		db.session.commit()
		return redirect(url_for('update_info'))
	elif request.method=='GET':
		form.username.data=current_user.username
		form.email.data=current_user.email
	return render_template('account.html',title='Account',form=form)

@app.route('/register/', methods=['GET', 'POST'])
def register():
	form=RegistrationForm()
	print(form.username.data)
	print(form.email.data)
	print(form.password.data)
	print(form.validate_on_submit())
	if form.validate_on_submit():
		print(form.username.data)
		print(form.email.data)
		print(form.password.data)
		hashed_password=bcrypt.hashpw(form.password.data.encode(),bcrypt.gensalt()).decode('utf-8')
		user=User(username=form.username.data,email=form.email.data,password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created!','success')
		return redirect(url_for('login'))
	print(form.errors)
	return render_template('register.html',title='Register',form=form)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.hashpw(form.password.data.encode(),bcrypt.gensalt()).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)