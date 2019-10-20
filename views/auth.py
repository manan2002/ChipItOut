from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import UserModel
from flask_login import login_user, logout_user, login_required, current_user
from exts import db
from helpers import check_email
from collections import defaultdict
    

auth = Blueprint('auth', __name__)


    
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
                    return redirect(url_for('dashboard.home'))
                else:
                    return render_template('auth/login.html', errors = {'pw':'wrong password!'})
            else:
                return render_template('auth/login.html', errors={'email': 'No user with this email address exists.'})
                
        else:
            return render_template('auth/login.html', errors={'email': 'Email you entered is invalid.'})
    
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

            data = defaultdict(lambda : '')
            if not valid_email: data['email'] = 'Please enter a valid email.'
            if ' ' in pw: data['pw'] = ('Password can\'t have spaces')
            if len(pw) < 8: data['pw'] = ('Password should be minimum 8 characters.')
            if len(name.strip()) < 1: data['name'] = ('Please enter a name.')
            return render_template('auth/register.html', errors = data)
    return render_template('auth/register.html')
