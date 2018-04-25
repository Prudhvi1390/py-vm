from flask import Blueprint, Flask, render_template, redirect, url_for, request, g, json
from routes.database import *
from routes.HomePage import *

deallocatedvms = Blueprint('deallocatedvms', __name__, template_folder='templates')

@deallocatedvms.route('/deallocatedvms', methods=['GET', 'POST'])
def deallocated_vms():
    deallocatedVMs = all_deallocated_vms()
    context = {'deallocatedVMs': deallocatedVMs, 'admin': request.cookies.get('usertype')}
    if request.cookies.get('usertype') == 'Admin':
        return render_template("deallocated_vms.html", **context)
    else:
        return redirect(url_for('homepage.user_login'))
@deallocatedvms.route('/movetoavailable', methods=['GET', 'POST'])
def move_to_available():
    for value in request.form.getlist('check'):
        values = [value]
        movetoavailable = ("UPDATE VirtualMachines SET Require_Rebuilt = '' WHERE Machine_Name = ?")
        cursor.execute(movetoavailable, values)
        connection.commit()
    return redirect(url_for('deallocatedvms.deallocated_vms'))
