from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import UserModel
from flask_login import login_user, logout_user, login_required, current_user
from exts import db
from helpers import check_email

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        pw = request.form.get('pw')
        email = request.form.get('email')
        print(email, pw)
        valid_email = check_email(email)
        if valid_email and len(pw) >= 8:
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
                
            #return jsonify({
            #    'status' : 'yo workin!'
            #})
        
        else:
            data = {'messages' : list()}
            if not valid_email: data['messages'].append('Please enter a valid email.')
            if len(pw) < 8: data['messages'].append('Password should be minimum 8 characters.')
            return jsonify(data)
                
    
    return render_template('auth/login.html')
"""
@auth.route('/register')
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        pw = request.form.get('pw')
        email = request.form.get('email')

        pw_hash = generate_password_hash(pw)
        u = UserModel(username=username, password=pw_hash)
        u.save()
        print('user added.', username, '|', pw)
        return redirect(url_for('.login'))
    return render_template('auth/register.html')
"""