from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required

dashboard = Blueprint('dashboard', __name__)


@login_required
@dashboard.route('/home')
def home():
    return render_template('user/dash.html')