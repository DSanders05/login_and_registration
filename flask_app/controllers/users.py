from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def home_page():
    return render_template('index.html')
    
@app.route('/user/register', methods = ['POST'])
def create_user():
    
    if User.validate_user(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        new_user_data = {
            'first_name':request.form['first_name'],
            'last_name':request.form['last_name'],
            'email':request.form['email'],
            'password':pw_hash
        }
        User.create_new_user(new_user_data)
        flash("User has been created; log in now.")
        return redirect('/')

    else:
        flash("User validation unsuccessful.")
        return redirect('/')

@app.route('/success')
def successful_login():
    if 'user_id' not in session:
        flash("You must be logged in to access success page.")
        return redirect('/')
    
    else:
        return render_template('success.html')

@app.route('/user/login', methods = ['POST'])
def login_user():
    if 'user_id' in session:
        return redirect('/success')

    user = User.get_user_by_email(request.form)
    if user == None:
        flash("No user with that username found.")
        return redirect('/')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Incorrect password. Check password input and try again.")
        redirect ('/')

    print(user.id)
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['email'] = user.email
    return redirect('/success')

@app.route('/user/logout')
def logout_user():
    if 'user_id' not in session:
        flash("User must first be logged in to logout.")
        return redirect('/')

    else:
        session.clear()
        print(session)
        flash("You have now been logged out.")
        return redirect('/')