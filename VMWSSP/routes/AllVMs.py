from flask import Blueprint, Flask, render_template, redirect, url_for, request, g, json
from routes.database import *
from routes.HomePage import *

allvms = Blueprint('allvms', __name__, template_folder='templates')

@allvms.route('/allvms')
def all_vms():
    getVM = ("SELECT Machine_Name, IP_Address, OS_Version, HostName, Assigned_To, Purpose, Start_Date, End_Date, Require_Rebuilt from VirtualMachines")
    cursor.execute(getVM)
    allVMs = cursor.fetchall()
    context = {'allVMs': allVMs, 'admin': request.cookies.get('usertype')}
    if request.cookies.get('usertype') == 'Admin':
        return render_template("all_vms.html", **context)
    else:
        return redirect(url_for('homepage.user_login'))

@allvms.route('/addvms', methods=['GET', 'POST'])
def add_vms():
    machinename = request.form['machinename']
    ipaddress = request.form['ipaddress']
    osversion = request.form['osversion']
    hostname = request.form['hostname']
    values = [machinename, ipaddress, osversion, hostname, '', '', '', '', '']
    addVM = ("INSERT INTO VirtualMachines (Machine_Name, IP_Address, OS_Version, HostName, Assigned_To , Purpose, Start_Date, End_Date, Require_Rebuilt) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)")
    cursor.execute(addVM, values)
    connection.commit()
    return redirect(url_for('allvms.all_vms'))
