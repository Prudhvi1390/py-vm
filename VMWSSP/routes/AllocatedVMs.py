from flask import Blueprint, Flask, render_template, redirect, url_for, request, g, json
from routes.database import *
from routes.HomePage import *

allocatedvms = Blueprint('allocatedvms', __name__, template_folder='templates')

@allocatedvms.route('/allocatedvms', methods=['GET', 'POST'])
def allocated_vms():
    allocatedVMs = all_allocated_vms()
    context = {'allocatedVMs': allocatedVMs, 'admin': request.cookies.get('usertype')}
    if request.cookies.get('usertype') == 'Admin':
        return render_template("allocated_vms.html", **context)
    else:
        return redirect(url_for('homepage.user_login'))

@allocatedvms.route('/removevms', methods=['GET', 'POST'])
def remove_vms():
    for value in request.form.getlist('check'):
        values = [value]
        removeVM = ("UPDATE VirtualMachines SET Assigned_To = '', Purpose = '', Start_Date = '', End_Date = '', Require_Rebuilt = 'Yes' WHERE Machine_Name = ?")
        cursor.execute(removeVM, values)
        connection.commit()
    return redirect(url_for('allocatedvms.allocated_vms'))
