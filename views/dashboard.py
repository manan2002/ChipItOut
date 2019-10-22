from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models.address import AddressModel

dashboard = Blueprint('dashboard', __name__)



@dashboard.route('/dash')
@login_required
def dash():
    context = {
        'user' : current_user
    }
    return render_template('user/dash.html', **context)

@dashboard.route('/pickup', methods = ['POST', 'GET'])
@login_required
def pickups():
    if request.method == 'POST':
        print(dict(request.form))

    return render_template('user/pickups.html')

@dashboard.route('/settings', methods = ['GET', 'POST'])
@login_required
def settings():
    
    if request.method == 'POST':
        pass
    context = {
        'u' : current_user
    }
    return render_template('user/settings.html', **context)


@dashboard.route('/add_address', methods=['GET', 'POST'])
@login_required
def add_address():
  
    if request.method == 'POST':
        addr = request.form.get('addr')
        zone = addr = request.form.get('zone')
        u = current_user
        print(addr, zone)
        #address = AddressModel(_address=addr, zone=zone, user=current_user)
        #address.save()
        #
        # return redirect(url_for('dashboard.dash'))

    return render_template('user/add_address.html')
