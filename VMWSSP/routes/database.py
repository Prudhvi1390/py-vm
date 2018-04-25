import pyodbc

connection = pyodbc.connect(
    r'DRIVER={ODBC Driver 13 for SQL Server};'
    r'SERVER=US97R1562311;'
    r'DATABASE=LABSSP;'
    r'UID=sa;'
    r'PWD=P@ssw0rd;'
    r'Trusted_Connection=No')

cursor = connection.cursor()

def user_validation( name ):
    values = [name]
    getUser = ("SELECT Name, User_Type from Users WHERE Name = ?")
    cursor.execute(getUser, values)
    try:
        uservalidation = list(cursor.fetchone())
    except:
        uservalidation = [None]
    return uservalidation

def vm_by_user( name ):
    values = [name]
    getVM = ("SELECT Machine_Name, IP_Address, OS_Version, Purpose, End_Date from VirtualMachines WHERE Assigned_To = ? ORDER BY Start_Date DESC")
    cursor.execute(getVM, values)
    try:
        allocatedVMs = cursor.fetchall()
    except:
        allocatedVMs = []
    return allocatedVMs

def vm_by_vmname( vmname ):
    values = [vmname]
    getVM = ("SELECT Machine_Name, IP_Address, OS_Version, HostName, Assigned_To, Purpose, Start_Date, End_Date from VirtualMachines WHERE Machine_Name = ?")
    cursor.execute(getVM, values)
    allocatedVMs = cursor.fetchone()
    return allocatedVMs

def all_available_vms():
    getVM = ("SELECT Machine_Name, IP_Address, OS_Version, HostName from VirtualMachines WHERE Assigned_To = '' and Require_Rebuilt = ''")
    cursor.execute(getVM)
    availableVMs = cursor.fetchall()
    return availableVMs

def available_w7_vms():
    getVM = ("SELECT Machine_Name, IP_Address, OS_Version, HostName from VirtualMachines WHERE Assigned_To = '' and Require_Rebuilt = '' and OS_Version = 'Windows 7'")
    cursor.execute(getVM)
    availableVMs = cursor.fetchall()
    return availableVMs

def available_w10_vms():
    getVM = ("SELECT Machine_Name, IP_Address, OS_Version, HostName from VirtualMachines WHERE Assigned_To = '' and Require_Rebuilt = '' and OS_Version = 'Windows 10'")
    cursor.execute(getVM)
    availableVMs = cursor.fetchall()
    return availableVMs

def assign_VM( osversion, assignedto, purpose, startdate, enddate ):
    if osversion == 'Windows 7':
        availableVMs = available_w7_vms()
    else:
        availableVMs = available_w10_vms()
    if len(availableVMs) != 0:
        availableVM = availableVMs[0]
        machinename = availableVM[0]
        #ipaddress = availableVM[1]
        #hostname = availableVM[2]
        assignVM = ("UPDATE VirtualMachines SET Assigned_To = ?, Purpose = ?, Start_Date = ?, End_Date = ? WHERE Machine_Name = ?")
        values = [assignedto, purpose, startdate, enddate, machinename]
        cursor.execute(assignVM, values)
    #removeVM = ("DELETE FROM AvailableVMs WHERE Machine_Name= ?")
    #values = [machinename]
    #cursor.execute(removeVM, values)
        connection.commit()
        return machinename

def all_allocated_vms():
    getVM = ("SELECT Machine_Name, IP_Address, OS_Version, HostName, Assigned_To, Purpose, Start_Date, End_Date from VirtualMachines WHERE Assigned_To != ''")
    cursor.execute(getVM)
    allocatedVMs = cursor.fetchall()
    return allocatedVMs

def all_users():
    getUser = ("SELECT Name, User_Type from Users")
    cursor.execute(getUser)
    allusers = cursor.fetchall()
    return allusers

def user_by_name(name):
    values = [name]
    getUser = ("SELECT Name, User_Type from Users Where Name = ?")
    cursor.execute(getUser, values)
    user = cursor.fetchall()
    userid = str(user[0])
    return userid

def all_deallocated_vms():
    getVM = ("SELECT Machine_Name, IP_Address, OS_Version, HostName, Require_Rebuilt from VirtualMachines WHERE Require_Rebuilt = 'Yes'")
    cursor.execute(getVM)
    deallocatedVMs = cursor.fetchall()
    return deallocatedVMs

#def remove_vm(vmname):
    #removeVM = ("UPDATE VirtualMachines SET Assigned_To = "", Purpose = "", End_Date = "" WHERE Machine_Name = ?")
    #cursor.execute(removeVM, vmname)
    #connection.commit()
