


# Importing the Flask Framework

from modules import *
from flask import *
import database
import configparser


page = {}
session = {}

# Initialise the FLASK application
app = Flask(__name__)
app.secret_key = 'SoMeSeCrEtKeYhErE'


# Debug = true if you want debug output on error ; change to false if you dont
app.debug = True


# Read my unikey to show me a personalised app
config = configparser.ConfigParser()
config.read('config.ini')
unikey = config['DATABASE']['user']
portchoice = config['FLASK']['port']

#####################################################
##  INDEX
#####################################################

# What happens when we go to our website
@app.route('/')
def index():
    # If the user is not logged in, then make them go to the login page
    if( 'logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))
    page['unikey'] = unikey
    page['title'] = 'Welcome'
    return render_template('welcome.html', session=session, page=page)

################################################################################
# Login Page
################################################################################

# This is for the login
# Look at the methods [post, get] that corresponds with form actions etc.
@app.route('/login', methods=['POST', 'GET'])
def login():
    page = {'title' : 'Login', 'unikey' : unikey}
    # If it's a post method handle it nicely
    if(request.method == 'POST'):
        # Get our login value
        val = database.check_login(request.form['sid'], request.form['password'])

        # If our database connection gave back an error
        if(val == None):
            flash("""Error with the database connection. Please check your terminal
            and make sure you updated your INI files.""")
            return redirect(url_for('login'))

        # If it's null, or nothing came up, flash a message saying error
        # And make them go back to the login screen
        if(val is None or len(val) < 1):
            flash('There was an error logging you in')
            return redirect(url_for('login'))
        # If it was successful, then we can log them in :)
        session['name'] = val[1]
        session['sid'] = request.form['sid']
        session['logged_in'] = True
        return redirect(url_for('index'))
    else:
        # Else, they're just looking at the page :)
        if('logged_in' in session and session['logged_in'] == True):
            return redirect(url_for('index'))
        return render_template('index.html', page=page)


################################################################################
# Logout Endpoint
################################################################################

@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('You have been logged out')
    return redirect(url_for('index'))


################################################################################
# List Units page
################################################################################

# List the units of study
@app.route('/list-units')
def list_units():
    # Go into the database file and get the list_units() function
    units = database.list_units()

    # What happens if units are null?
    if (units is None):
        # Set it to an empty list and show error message
        units = []
        flash('Error, there are no units of study')
    page['title'] = 'Units of Study'
    return render_template('units.html', page=page, session=session, units=units)


################################################################################
# List Staff page
################################################################################

@app.route('/list-staff')
def list_staff():
    # Go into the database file and get the list_units() function
    staff = database.list_staff()
    print(staff)
    # What happens if units are null?
    if (staff is None):
        # Set it to an empty list and show error message
        staff = []
        flash('Error, there are no units of study')
    page['title'] = 'Staff List'
    return render_template('staff.html', page=page, session=session, staff=staff)

################################################################################
# Get Staff page
################################################################################

@app.route('/get-staff', methods=['POST', 'GET'])
def get_staff():
    eachStaff = []
    if request.method == "POST":
        eachStaff = database.get_staff(request.form['deptID'])
        page['title'] = 'Get Staff By Department'
        print(eachStaff)
        if eachStaff == None or len(eachStaff) == 0:
            flash('There is no staff in this department')
            return render_template('getStaff.html', page=page, session=session, eachStaff=[])    
        else:
            flash(str(len(eachStaff)) + ' staff allocated to this department')
            return render_template('getStaff.html', page=page, session=session, eachStaff=eachStaff)    
    else:
        page['title'] = 'Get Staff By Department'
        return render_template('getStaff.html', page=page, session=session, eachStaff=eachStaff)

    


################################################################################
# Get Staff page
################################################################################

@app.route('/staff-per-dept')
def staff_per_dept():
    # Go into the database file and get the list_units() function
    spd = database.staff_per_dept()
    print(spd)
    # What happens if units are null?
    if (spd is None):
        # Set it to an empty list and show error message
        spd = []
        flash('There is no staff allocated to any department.')
    page['title'] = 'Get Staff By Department'
    return render_template('staffPerDept.html', page=page, session=session, spd=spd)


################################################################################
# Insert Staff
################################################################################

@app.route('/insert-staff', methods=['POST', 'GET'])
def insert_staff():
    before = True
    toInsert = None
    print("yes1")
    if request.method == "POST":
        print("yes2")
        staffID = request.form['staffID']
        staff_name = request.form['staff_name']
        departmentID = request.form['departmentID']
        staff_password = request.form['staff_password']
        staff_address = request.form['staff_address']
        staff_salary = request.form['staff_salary']
        toInsert = database.insert_staff(staffID, staff_name, departmentID, staff_password, staff_address, staff_salary)
        before = False
        print(toInsert)
    if toInsert:
        print("4")
        flash('Staff has been added to the database')
    else:
        if before == False:
            toInsert = []
            flash('No Staff found for this department')
    
    page['title'] = 'Add New Staff'
    return render_template('addNewStaff.html', page=page, session=session, toInsert=toInsert)
        