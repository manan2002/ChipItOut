from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models.address import AddressModel
from models.pickup import PickupModel
from exts import db
from datetime import datetime
from helpers import find_pickup_date
dashboard = Blueprint('dashboard', __name__)



@dashboard.route('/dash')
@login_required
def dash(): 
    user_addresses = current_user.addresses
    need_addr = (len(user_addresses) == 0)
    def_addr = list(filter(lambda x: x.default == True, user_addresses))
    if len(def_addr) >= 1:
        def_addr = def_addr[0]
    rest_addrs = list(filter(lambda x: x.default != True, user_addresses))
    user_pickups = current_user.pickups
    active_pickup = list(filter(lambda x: x.active == True, user_pickups))
    previous_pickups = list(filter(lambda x: x.active == False, user_pickups))
    print(active_pickup)    
    context = {
        'u': current_user,
        'need_address': need_addr,
        'def_addr': def_addr,
        'rest_addrs': rest_addrs,
        'active_pickup' : active_pickup,
        'previous_pickups': previous_pickups
        }
    
    return render_template('user/dash.html', **context)


@dashboard.route('/pickup', methods = ['POST', 'GET'])
@login_required
def pickups():
    if request.method == 'POST':
        addr_id = request.form.get('address')
        description = request.form.get('description')
        if description == '':
            return redirect(url_for('dashboard.dash'))
        addr = AddressModel.query.get(addr_id)
        zone = addr.zone
        current_active_pickups = len(tuple(filter(lambda x: x.active == True, current_user.pickups)))
        if current_active_pickups > 0:
            return redirect(url_for('dashboard.dash'))
        """
        n --> Sunday 
        s --> Saturday
        e --> Friday 
        w --> Thursday
        """
        if zone == 'n':
            p_date = find_pickup_date('n')
        if zone == 's':
            p_date = find_pickup_date('s')
        if zone == 'e':
            p_date = find_pickup_date('e')
        if zone == 'w':
            p_date = find_pickup_date('w')
        pickup = PickupModel(scheduled_date = p_date,
                             user = current_user,
                             description = description
                             )
        pickup.save()
        current_user.can_schedule = False
        db.session.commit()
        return redirect(url_for('dashboard.dash'))


    user_addresses = current_user.addresses
    need_addr = (len(user_addresses) == 0)
    def_addr = list(filter(lambda x: x.default == True, user_addresses))
    if len(def_addr) >= 1:
        def_addr = def_addr[0]
    rest_addrs = list(filter(lambda x : x.default != True, user_addresses))
    context = {
        'u': current_user,
        'need_address': need_addr,
        'def_addr': def_addr,
        'rest_addrs' : rest_addrs
    }

    return render_template('user/pickups.html', **context)


@dashboard.route('/settings', methods = ['GET', 'POST'])
@login_required
def settings():
    
    if request.method == 'POST':
        pass
    
    user_addresses = current_user.addresses
    need_addr = (len(user_addresses) == 0)
    def_addr = list(filter(lambda x: x.default == True, user_addresses))
    if len(def_addr) >= 1:
        def_addr = def_addr[0]
    rest_addrs = list(filter(lambda x: x.default != True, user_addresses))
    context = {
        'u': current_user,
        'need_address': need_addr,
        'def_addr': def_addr,
        'rest_addrs': rest_addrs
    }
    return render_template('user/settings.html', **context)


@dashboard.route('/add_address', methods=['GET', 'POST'])
@login_required
def add_address():
  
    if request.method == 'POST':
        addr = request.form.get('addr')
        zone = request.form.get('zone')
        default = request.form.get('default')
        label = request.form.get('label')

        if addr == '' or 'zone' not in request.form or label == '':
            return redirect(url_for('dashboard.dash'))
        u = current_user
        if default == 'on':
            for address in u.addresses:
                address.default = False
            db.session.commit()
            address = AddressModel(
                label = label, 
                _address=addr, 
                zone=zone, 
                default = True,
                user=current_user)
        else:
            if len(u.addresses) == 0:
                address = AddressModel(
                    label = label,
                    _address=addr,
                    zone=zone, 
                    user=current_user, 
                    default = True)
            else:
                address = AddressModel(
                    label = label,
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


@dashboard.route('/delete_pickup/<int:pickup_id>', methods=['GET'])
@login_required
def del_pickup(pickup_id):
    p = PickupModel.query.get(pickup_id)
    if current_user == p.user:
        db.session.delete(p)
        current_user.can_schedule = True
        db.session.commit()
        return redirect(url_for('dashboard.dash'))
    return redirect(url_for('index'))
