from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user

dashboard = Blueprint('dashboard', __name__)



@dashboard.route('/home')
@login_required
def home():
    print(current_user)
    return render_template('user/dash.html')
