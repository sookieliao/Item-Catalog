from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Brand, User, Camera

# Connect to database
engine = create_engine('sqlite:///cameras.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

# create user session with flask.
from flask import session as login_session
import random, string

loggedIn = False
user_id = 1

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase+string.digits) for x in xrange(32))
    login_session['state']=state

def getUserId(email):
    session = DBSession()
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

def getUserInfo(user_id):
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).one
    return user

@app.route('/sookiesusedcameras/newuser', methods=['GET','POST'])
def createUser():
    if request.method == 'GET':
        return render_template('createUser.html')
    else:
        session = DBSession()
        if request.form['password1'] == request.form['password2']:
            print "passwords are the same. now adding user..."
            user = User(name=request.form['name'],email=request.form['email'],password=request.form['password1'])
            session.add(user)
            session.commit()
            print "User created successfully with user_id %s!"% user.id
            loggedIn = True
            login_session['username']=user.name
            login_session['id']=user.id
            login_session['email']=user.email
            login_session['currentUser'] = login_session['username']
            flash("you are now logged in as %s" % login_session['username'])

            print "Redirecting to my store..."
            return redirect(url_for('showMyStore', user_id=user.id))
        else:
            print "Password doesn't match. Please try again."


@app.route('/sookiesusedcameras/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        print 'authendicating user...'
        session = DBSession()
        user = session.query(User).filter_by(email=request.form['email']).first()


        if not user:
            print "There's no record for this email.Please try again."

        elif user.name != request.form['name']:
            print "Name or email is incorrect.Please try again."
        elif request.form['password1'] != request.form['password2']:
            print "Passwords repeated doesn't match. Please try again."
        elif request.form['password1'] != user.password:
            print "Password is incorrect. Please try again."
        else:
            print "Login success. Redirecting to my store..."
            loggedIn = True
            login_session['username']=user.name
            login_session['id']=user.user_id
            login_session['email']=user.email
            login_session['currentUser']  = login_session['username']
            flash("you are now logged in as %s" % login_session['username'])
            print "done!"
            return redirect(url_for('showMyStore', user_id=user.id))


@app.route('/sookiesusedcameras/new')
def checkUserWhenAddItem():
    # if user is not log in, redirect to log in page
    if not loggedIn:
        redirect(url_for('login'))
    else:
        return render_template('addItem.html', user_id=user_id)


@app.route('/')
@app.route('/sookiesusedcameras')
def showCameras():
    loggedIn = False
    print loggedIn
    print 'login_session: %s' % login_session
    print loggedIn
    if login_session != None:
        loggedIn = True
        #get user id
    print loggedIn
    session = DBSession()
    cameras = session.query(Camera).all()
    #brands = session.query(Brand).all()
    #conditions = session.query(Condition).all()
    return render_template('showCameras.html',cameras = cameras, length=len(cameras), login=loggedIn, user_id=user_id)

@app.route('/sookiesusedcameras/brand=<int:brand_id>')
def showCamerasWithBrand(brand_id):
    if currentUser == login_session['username']:
        loggedIn = True
    session = DBSession()
    cameras = session.query(Camera).filter_by(brand_id=brand_id).all()
    brand = session.query(Brand).filter_by(id=brand_id).one()
    return render_template('showCamerasWithBrand.html',cameras = cameras, length=len(cameras), brand=brand.name, login=loggedIn, user_id=user_id)

@app.route('/sookiesusedcameras/condition=<condition>')
def showCamerasWithCondition(condition):
    if currentUser == login_session['username']:
        loggedIn = True
    session = DBSession()
    cameras = session.query(Camera).filter_by(condition=condition).all()
    return render_template('showCamerasWithCondition.html',cameras = cameras, length=len(cameras), condition=condition, login=loggedIn, user_id=user_id)



@app.route('/sookiesusedcameras/user=<int:user_id>/new', methods=['GET','POST'])
def addItem(user_id):
    # ideally, when user cancel craeting, it should be back to whever they were.
    if request.method == 'GET':
        return render_template('addItem.html', user_id=user_id)
    else:  # for a POST
        session = DBSession()
        newItem = Camera(name=request.form['name'],brand_id=request.form['brand'],user_id=user_id,
            description=request.form['description'],price=request.form['price'],condition=request.form['condition'])
        session.add(newItem)
        session.commit()
    return redirect(url_for('showMyStore', user_id=user_id))

#try @app.route('/sookiesusedcameras/mystore=<int:user_id>', methods=['GET','POST'])
@app.route('/sookiesusedcameras/mystore/user=<int:user_id>')
def showMyStore(user_id):
    session = DBSession()
    cameras = session.query(Camera).filter_by(user_id=user_id).all()
    return render_template('showMyStore.html',cameras = cameras, length=len(cameras), user_id=user_id)

@app.route('/sookiesusedcameras/user=<int:user_id>/camera=<int:camera_id>/edit', methods=['GET','POST'])
def editItem(user_id, camera_id):
    session = DBSession()
    camEdit = session.query(Camera).filter_by(id=camera_id).one()

    if request.method == 'GET':
        return render_template('editItem.html', camera= camEdit, user_id=user_id)
    else:  # for a POST
        camEdit.name = request.form['name']
        camEdit.brand_id=request.form['brand']
        camEdit.description=request.form['description']
        camEdit.price=request.form['price']
        camEdit.condition=request.form['condition']
        session.add(camEdit)
        session.commit()

        cameras = session.query(Camera).filter_by(user_id=user_id).all()
    return redirect(url_for('showMyStore',user_id=user_id))


@app.route('/sookiesusedcameras/user=<int:user_id>/camera=<int:camera_id>/delete', methods=['GET','POST'])
def deleteItem(user_id, camera_id):
    session = DBSession()
    camDelete = session.query(Camera).filter_by(id=camera_id).one()
    if request.method == 'GET':
        return render_template('deleteItem.html', camera= camDelete, user_id=user_id)
    else:  # for a POST
        session.delete(camDelete)
        session.commit()
    return redirect(url_for('showMyStore', user_id=user_id))


# These are for API calls that returns JSON file
@app.route('/sookiesusedcameras/JSON')
def getCameras():
    return "this page will show json for all products."

@app.route('/sookiesusedcameras/brand=<brand_name>/JSON')
def getCamerasWithBrand(brand_name):
    return "this page will show json for all products for a specific brand."

@app.route('/sookiesusedcameras/condition=<condition>/JSON')
def getCamerasWithCondition(condition):
    return "this page will show json for all products for a condition."

@app.route('/sookiesusedcameras/mystore/user=<int:user_id>/JSON')
def getMyStore(user_id):
    return 'This is the page return JSON for my store'

@app.route('/sookiesusedcameras/user=<int:user_id>/camera=<int:camera_id>/JSON')
def getMyCamera(user_id, camera_id):
    return 'This is the page return JSON for a camera'


if __name__ == '__main__':
    app.secret_key = "super secret key"
    app.debug = True  #rerun the code when it detects code change
    app.run(host = '0.0.0.0', port = 5000)