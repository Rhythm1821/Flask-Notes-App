from flask import Blueprint,render_template,request,flash,redirect,url_for
from website import db
from website.models import User
from flask_bcrypt import generate_password_hash,check_password_hash
from flask_login import login_user,login_required,logout_user,current_user


auth= Blueprint('auth',__name__)

@auth.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password,password):
                flash('You are now logged in','success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password. Please enter correct password','error')
        else:
            flash('Incorrect Email','error')

    return render_template("login.html",title='Login')


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up",methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists','error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters','error')
        elif len(firstName) < 2:
            flash('Name is too  short','error')
        elif len(password1) < 3:
            flash('Password is too short','error') 
        elif password1 != password2:
            flash('Password does not match confirm password','error')
        else:
            hashed_pw = generate_password_hash(password1).decode('utf-8')
            user = User(email=email,firstName=firstName,password= hashed_pw)
            db.session.add(user)
            db.session.commit()
            login_user(user,remember=True)
            flash('Account created','success')
            redirect(url_for('views.home'))

    return render_template("sign_up.html",title='Sign Up')