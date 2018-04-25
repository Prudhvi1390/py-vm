import os
from flask import Flask, render_template, redirect, url_for, request, g, json
from routes.HomePage import homepage
from routes.VMProcess import vmprocess
from routes.AvailableVMs import availablevms
from routes.AllocatedVMs import allocatedvms
from routes.DeAllocatedVMs import deallocatedvms
from routes.AllVMs import allvms
from routes.AccessControl import accesscontrol

app = Flask(__name__)
app.register_blueprint(homepage)
app.register_blueprint(vmprocess)
app.register_blueprint(availablevms)
app.register_blueprint(allocatedvms)
app.register_blueprint(deallocatedvms)
app.register_blueprint(allvms)
app.register_blueprint(accesscontrol)


if __name__ == "__main__":
    app.secret_key = '$uP3r$3cr3tk3y'
    #app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
