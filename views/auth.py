from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import UserModel
from flask_login import login_user, logout_user, login_required, current_user
from exts import db
from helpers import check_email

auth = Blueprint('auth', __name__)

@auth.route('/auth', methods = ['GET'])
def authTemplate():
    return render_template('auth/auth.html')
    
@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        pw = request.form.get('pw')
        email = request.form.get('email')
        print(email, pw)
        valid_email = check_email(email)
        if valid_email:
            u = UserModel.query.filter_by(email=email).first()
            if u:
                if check_password_hash(u.password, pw):
                    login_user(u)
                    print('user logged in.')
                    return jsonify({'message':'Yay you\'re logged in'})
                else:
                    return jsonify({'message':'wrong password!'})
            else:
                return jsonify({'message':'no user with this email address exists.'})
        else:
            return jsonify({'message': 'email you entered is invalid'}) 

            #return jsonify({
            #    'status' : 'yo workin!'
            #})
        
    
    return render_template('auth/login.html')

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        pw = request.form.get('pw')
        email = request.form.get('email')
        u = UserModel.query.filter_by(email = email).first()
        
        valid_email = check_email(email)
        #If user data passes our validation, we proceed.
        if valid_email and (len(pw) >= 8) and (len(name.strip()) >= 1) and not(' ' in pw):
            if u:
                return jsonify({'message': 'user already exists.'})
            pw_hash = generate_password_hash(pw)
            u = UserModel(email=email,name=name, password=pw_hash)
            u.save()
            return redirect(url_for('.login'))
        else:

            data = {'messages' : list()}
            if not valid_email: data['messages'].append('Please enter a valid email.')
            if ' ' in pw: data['messages'].append('Password can\'t have spaces')
            if len(pw) < 8: data['messages'].append('Password should be minimum 8 characters.')
            if len(name.strip()) < 1: data['messages'].append('Please enter a name.')
            return jsonify(data)
    return render_template('auth/register.html')
