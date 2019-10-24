from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models.address import AddressModel
from exts import db

dashboard = Blueprint('dashboard', __name__)



@dashboard.route('/dash')
@login_required
def dash():
    context = {
        'u' : current_user
    }
    print(len(current_user.addresses))
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
        zone = request.form.get('zone')
        default = request.form.get('default')
        u = current_user
        if default == 'on':
            for address in u.addresses:
                address.default = False
            db.session.commit()
            address = AddressModel(
                _address=addr, 
                zone=zone, 
                default = True,
                user=current_user)
        else:
            if len(u.addresses) == 0:
                address = AddressModel(
                    _address=addr,
                    zone=zone, 
                    user=current_user, 
                    default = True)
            else:
                address = AddressModel(
                    _address=addr,
                    zone=zone,
                    user=current_user)

        address.save()
        return redirect(url_for('dashboard.dash'))

    return render_template('user/add_address.html')


@dashboard.route('/delete_address/<int:addr_id>', methods=['GET'])
@login_required
def del_address(addr_id):
    addr = AddressModel.query.get(addr_id)
    if current_user == addr.user:
        db.session.delete(addr)
        db.session.commit()
        return redirect(url_for('dashboard.settings'))
    return redirect(url_for('index'))

