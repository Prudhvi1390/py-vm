from flask import Blueprint, Flask, flash, render_template, redirect, url_for, request, g, json, make_response, session
from datetime import date, timedelta, datetime
from routes.database import *
from routes.HomePage import *
import win32api, win32net, win32security, win32con
import base64

vmprocess = Blueprint('vmprocess', __name__, template_folder='templates')

#@vmprocess.route('/homepage')
#def __init__():
    #user = user_login.user
    #allocatedVMs = vm_by_user(user)
    #count = len(allocatedVMs)
    #context = {'requester': user, 'allocatedVMs': allocatedVMs, 'admin': user_login.admin, 'count': count}
    #resp = make_response()
    #resp.set_cookie('username', user)
    #resp.set_cookie('admin', uservalidation[1])
    #return render_template('homepage.html', **context)

@vmprocess.route('/redirecthomepage', methods=['POST'])
def assign_vm():
    #user = request.cookies.get('username')
    user = request.form['requester']
    #uservalidation = user_validation(user)
    startdate = (date.today()).strftime("%m/%d/%Y")
    maxenddate = (datetime.strptime(startdate, '%m/%d/%Y') + timedelta(days=21)).strftime("%m/%d/%Y")
    enddate = request.form['date-input']
    if enddate == '' or enddate > maxenddate:
        enddate = (datetime.strptime(startdate, '%m/%d/%Y') + timedelta(days=14)).strftime("%m/%d/%Y")
    purpose = request.form['purpose']
    osversion = request.form['osversion']
    admins = [trustee.strip() for trustee in (request.form['adminslist']).split(',')]
    admins.insert(0, user)
    RDUsers = [trustee.strip() for trustee in (request.form['RDUserslist']).split(',')]
    #f = open("C:\\test\\admins.txt", "a+")
    #f.write(str(user))
    #f.close()
    #print(trustees)
    #if len(vm_by_user(user)) < 2:
    machinename = assign_VM(osversion, user, purpose, startdate, enddate)
    try:
        #a = user_rights()
        #a = str(a)[2:-5] str(user_rights())[2:-5]
        #a = str(user_rights())[2:-5]
        th=win32security.LogonUser('pkeertip',None,str(base64.b64decode(b'MzVBU1BpdWU4'))[2:-1],win32con.LOGON32_LOGON_INTERACTIVE, win32con.LOGON32_PROVIDER_DEFAULT)
        win32security.ImpersonateLoggedOnUser(th)
        for uname in admins:
            #f=open("C:\\test\\admins.txt", "a+")
            #f.write(uname + machinename)
            #f.close()
            win32net.NetLocalGroupAddMembers(machinename, 'Administrators', 3, [{'domainandname': uname}])
        for uname in RDUsers:
            #f=open("C:\\test\\admins.txt", "a+")
            #f.write(uname + machinename)
            #f.close()
            win32net.NetLocalGroupAddMembers(machinename, 'Remote Desktop Users', 3, [{'domainandname': uname}])
        win32security.RevertToSelf()
        th.Close()
    except Exception:
        pass
    #allocatedVMs = vm_by_user(user)
    #count = len(allocatedVMs)
    #context = {'requester': user, 'allocatedVMs': allocatedVMs, 'count': count}
    #return render_template('modal.html', **context)
    #return redirect(url_for('vmprocess.__init__'))
    return redirect(url_for('homepage.user_login'))
    #return 'OK'

@vmprocess.route('/vm/<vmname>')
def vm_page(vmname):
    #user = getpass.getuser()
    #uservalidation = user_validation(user)
    #session['vmname'] = vmname
    vminfo = vm_by_vmname( vmname )
    context = {'vminfo': vminfo, 'admin': request.cookies.get('usertype')}
    return render_template('vmpage.html', **context)

@vmprocess.route('/vmstatus/<vmname>', methods=['GET', 'POST'])
def update_vmstatus(vmname):
    user = request.cookies.get('username')
    #values = [session['vmname']]
    values = [vmname]
    if request.method == 'POST':
        if request.form['submit'] == 'Extend VM':
            try:
                vminfo = vm_by_vmname(vmname)
                currentenddate = vminfo[7]
                values.insert(0, (datetime.strptime(currentenddate, '%m/%d/%Y') + timedelta(days=7)).strftime("%m/%d/%Y"))
                extendVM = ("UPDATE VirtualMachines SET End_Date = ? WHERE Machine_Name = ?")
                cursor.execute(extendVM, values)
                connection.commit()
                return redirect(url_for('vmprocess.vm_page', vmname = vmname))
            except:
                #return redirect(url_for('vmprocess.__init__'))
                return redirect(url_for('homepage.user_login'))
        elif request.form['submit'] == 'Remove VM':
            removeVM = ("UPDATE VirtualMachines SET Assigned_To = '', Purpose = '', Start_Date = '', End_Date = '', Require_Rebuilt = 'Yes' WHERE Machine_Name = ?")
            cursor.execute(removeVM, values)
            connection.commit()
            #return redirect(url_for('vmprocess.__init__'))
            return redirect(url_for('homepage.user_login'))
