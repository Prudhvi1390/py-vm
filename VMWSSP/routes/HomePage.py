from flask import Blueprint, Flask, flash, render_template, redirect, url_for, request, g, json, make_response, session
import getpass
from datetime import date, timedelta, datetime
from routes.database import *
import os

homepage = Blueprint('homepage', __name__, template_folder='templates')

#mindate = (date.today()).strftime("%m/%d/%Y")
#maxdate = (datetime.strptime(mindate, '%m/%d/%Y') + timedelta(days=21)).strftime("%Y/%m/%d")
#defaultenddate = (datetime.strptime(mindate, '%m/%d/%Y') + timedelta(days=14)).strftime("%Y/%m/%d")
#print(maxdate)
#global user
#username = None

#@homepage.route('/')
#def index():
    #user = request.environ["REMOTE_USER"]
    #user = "r1-core\pkeertip"
    #context = {'user': user}
    #resp = make_response()
    #resp = make_response(render_template('login.html', **context))
    #resp.set_cookie('username', expires=0)
    #resp.set_cookie('admin', expires=0)
    #flash('You were successfully logged in')
#   return render_template('login.html', **context)
    #return redirect(url_for('homepage.index'))
    #return render_template('login.html')

#@homepage.route('/userlogin', methods=['GET','POST'])
@homepage.route('/')
def user_login():
    #user = 'pkeertip'
    #useru = request.form['requester']
    #user_login.user = request.cookies.get('username')
    #user_login.admin = request.cookies.get('usertype')
    #user_login.user = 'r1-core\pkeertip'
    user = request.environ["REMOTE_USER"]
    #useru = request.cookies.get('username')
    #if useru:
        #user = useru
    #else:
        #user = None
    try:
        uservalidation = user_validation(user)
        isadmin = uservalidation[1]
    except:
        isadmin = 'User'
    #user = request.cookies.get('username')
    #if user is None:
        #user = request.form['requester']
    #else:
    #    user = request.cookies.get('username')
    #try:
        #uservalidation = user_validation(user)
        #user_login.admin = uservalidation[1]
        #admin = user_login.admin
    #except:
        #user_login.admin = 'User'
        #admin = user_login.admin
    #if user != uservalidation[0]:
        #return redirect(url_for('homepage.index'))
    #elif user in uservalidation[0] and uservalidation[1] == 'Admin':
    #    return render_template('homepage.html', **context)
    #else:
    #return redirect(url_for('vmprocess.__init__'))
    #return render_template('warning.html', user = user)
    allocatedVMs = vm_by_user(user)
    count = len(allocatedVMs)
    context = {'requester': user, 'allocatedVMs': allocatedVMs, 'admin': isadmin, 'count': count}
    resp = make_response(render_template('homepage.html', **context))
    resp.set_cookie('usertype', isadmin)
        #resp = make_response()
        #resp.set_cookie('username', user)
        #resp.set_cookie('admin', uservalidation[1])
    #return render_template('homepage.html', **context)
    return resp
