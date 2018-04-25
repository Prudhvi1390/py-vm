from flask import Blueprint, Flask, render_template, redirect, url_for, request, g, json
from routes.database import *
from routes.HomePage import *

accesscontrol = Blueprint('accesscontrol', __name__, template_folder='templates')

@accesscontrol.route('/accesscontrol')
def access_control():
    allusers = all_users()
    context = {'allusers': allusers, 'admin': request.cookies.get('usertype')}
    if request.cookies.get('usertype') == 'Admin':
        return render_template("access_control.html", **context)
    else:
        return redirect(url_for('homepage.user_login'))

@accesscontrol.route('/updatuser', methods=['GET', 'POST'])
def update_user():
    #values = [request.form['LanID'], request.form.getlist('check')]
    userID = request.form['LanID']
    userType = request.form['options']
    #if userType == '':
        #userType = 'User'
    addvalues = [userID, userType]
    removevalues = [userID]
    if request.method == 'POST':
        if request.form['submit'] == 'Add User':
            addUser = ("INSERT INTO Users (Name, User_Type) VALUES (?, ?)")
            cursor.execute(addUser, addvalues)
            connection.commit()
            return redirect(url_for('accesscontrol.access_control'))
        elif request.form['submit'] == 'Remove User':
            removeUser = ("DELETE FROM Users WHERE NAME = ?")
            cursor.execute(removeUser, removevalues)
            connection.commit()
            return redirect(url_for('accesscontrol.access_control'))
