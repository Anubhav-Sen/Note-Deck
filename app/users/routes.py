from flask import Blueprint, render_template, request, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

blueprint = Blueprint('users', __name__)

@blueprint.get('/sign-up')
def get_signUp(): 
  return render_template('sign-up.html')

@blueprint.post('/sign-up')
def post_signUp():

  email = request.form['email'] or None
  username = request.form['username'] or None
  password = request.form['password'] or None
  confirm_password = request.form['confirm-password'] or None

  if password != confirm_password:
    return render_template('sign-up.html', error = "Please make sure your passwords match.")

  elif email == User.query.filter_by(email = email):
    return render_template('sign-up.html', error = "This email is aldready registered.")

  user = User(username = username, email = email.lower(), password = generate_password_hash(password))
  user.save()

  return redirect(url_for('users.get_login'))

@blueprint.get('/login')
def get_login():
  return render_template('log-in.html')

@blueprint.post('/login')
def post_login():

  email = request.form.get('email')
  password = request.form.get('password')
  destination = request.args.get('next')

  try:
    user = User.query.filter_by(email = email).first()

    if not user:
      raise Exception('No user with this email was found.')
    elif not check_password_hash(user.password, password):
      raise Exception('The password you entered is incorrect.')
    
    login_user(user)
    if destination:
      return redirect(destination)

    else:
      return redirect(url_for('deck_pages.index'))
    
  except Exception as error_message:
    error = error_message or 'An error occurred while logging in. Please verify your email and password.'
    return render_template('log-in.html', error = error)

@blueprint.get('/logout')
def logout():
  logout_user()
  return redirect(url_for('users.get_login'))