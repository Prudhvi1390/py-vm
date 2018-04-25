from flask import Blueprint, Flask, render_template, redirect, url_for, request, g, json
from routes.database import *
from routes.HomePage import *

availablevms = Blueprint('availablevms', __name__, template_folder='templates')

@availablevms.route('/availablevms')
def available_vms():
    availableVMs = all_available_vms()
    context = {'availableVMs': availableVMs, 'admin': request.cookies.get('usertype')}
    if request.cookies.get('usertype') == 'Admin':
        return render_template("available_vms.html", **context)
    else:
        return redirect(url_for('homepage.user_login'))
