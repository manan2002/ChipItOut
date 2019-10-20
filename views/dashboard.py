from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user

dashboard = Blueprint('dashboard', __name__)



@dashboard.route('/dash')
@login_required
def dash():
    print(current_user)
    return render_template('user/dash.html')

@dashboard.route('/pickup', methods = ['POST', 'GET'])
@login_required
def pickups():
    if request.method == 'POST':
        pass

    return render_template('user/pickups.html')

