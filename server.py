from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# these imports are for utilizing sqlalchemy to build and access our database.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Brand, User, Camera
# this import is for managing user session
from flask import session as login_session

# Connect to database
# Future users should change the data base name('cameras.db') based on their own db names.
engine = create_engine('sqlite:///cameras.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

app = Flask(__name__)

# Create a global variable to keep the login state.
loggedIn = False

@app.route('/sookiesusedcameras/newuser/<messages>', methods=['GET','POST'])
def createUser(messages):
    """ Create new user.

    Parameters
    ----------
    messages: string, error message

    CreateUser() takes <messages> as parameter, and receives two types of requests.
    When it's a "GET" request, we pass on the error messages and render the template for creating user.
    However, with "DEFAULT" it means there's no error, and as a result, we set the error message to None.
    When it's a "POST" request, we perform checking for username, email, and password. If anything is wrong,
    we redirect user to the "createUser" page(with a GET request) with an error message indicating something
    is wrong and action needs to be taken.
    If everything goes well, we extrac all the data user filled out and create a user with them. Then we
    add user's information to login_session indicating current user, and redirect user to his/her page.(showMyStore)

    """
    inputs = {}
    if messages == "DEFAULT":
        messages = None

    if request.method == 'GET':
        inputs['messages']=messages
        return render_template('createUser.html', inputs=inputs)
    else:
        session = DBSession()
        if not request.form['name']:
            inputs['messages']= "Username is required. Please fill it up."
            return redirect(url_for('createUser', messages=inputs['messages']))
        elif not request.form['email']:
            inputs['messages']= "Email is required. Please fill it up."
            return redirect(url_for('createUser', messages=inputs['messages']))

        elif request.form['password1'] != request.form['password2']:
            inputs['messages']= "Password doesn't match. Please try again."
            return redirect(url_for('createUser', messages=inputs['messages']))
        else:
            user = User(name=request.form['name'],email=request.form['email'],password=request.form['password1'])
            session.add(user)
            session.commit()
            loggedIn = True
            login_session['username']=user.name
            login_session['id']=user.id
            login_session['email']=user.email
            login_session['currentUser'] = login_session['username']
            login_session['loggedIn'] = True
            flash("you are now logged in as %s" % login_session['username'])
            return redirect(url_for('showMyStore', user_id=user.id))

@app.route('/sookiesusedcameras/login/message/<messages>', methods=['GET','POST'])
def login(messages):
    """ Log in.

    Parameters
    ----------
    messages: string, error message

    login takes <messages> as parameter, and receives two types of requests.
    When it's a "GET" request, we pass on the error messages and render the template for logging in.
    However, with "GOOD" it means there's no error, and as a result, we set the error message to None.
    When it's a "POST" request, we first perform checking for username, email, and passwords. If anything is wrong,
    we redirect user back to the "login" page(with a GET request) with an error message indicating something
    is wrong and action needs to be taken.
    If everything goes well, we add user's information to login_session indicating current user, and redirect user
    to his/her page.(showMyStore)

    """
    inputs = {}
    if messages == "GOOD":
        messages = None
    print messages

    if request.method == 'GET':
        inputs['messages']=messages
        return render_template('login.html', inputs=inputs)
    else:
        session = DBSession()
        user = session.query(User).filter_by(email=request.form['email']).first()

        if not user :
            inputs['messages']= "There's no record for this email.Please try again."
            return redirect(url_for('login', messages=inputs['messages']))

        elif user.name != request.form['username']:
            inputs['messages']= "Name or email is incorrect.Please try again."
            return redirect(url_for('login', messages=inputs['messages']))

        elif request.form['password1'] != user.password:
            inputs['messages']= "Password is incorrect. Please try again."
            return redirect(url_for('login', messages=inputs['messages']))

        else:
            loggedIn = True
            login_session['username']=user.name
            login_session['id']=user.id
            login_session['email']=user.email
            login_session['currentUser']  = login_session['username']
            flash("you are now logged in as %s" % login_session['username'])
            return redirect(url_for('showMyStore', user_id=user.id))

@app.route('/sookiesusedcameras/logout')
def logout():
    """ Log out.

    logout takes no as parameter, and will always be a GET request.
    When "logout" is called, it'll wipe out currentUser, username, email and id from login_session,
    and switch loggedIn to off, indicating the user isn't autheticated. Then the user will be redirected
    back to homepage(showCameras).

    """
    loggedIn = False
    del login_session['currentUser']
    del login_session['username']
    del login_session['email']
    del login_session['id']
    login_session['loggedIn']=False
    flash("you are now logged out.")
    return redirect(url_for('showCameras'))


@app.route('/')
@app.route('/sookiesusedcameras')
def showCameras():
    """ Display all cameras stored in the database.

    showCameras takes no as parameter, and will always be a GET request.
    When "showCameras" is called, it'll grab all camera data from the data base and display them.
    At the same time, hyperlinks for login/logout, myStore, addItem will be render at the corner so
    that users can navigate themselves to wherever they want to do. (Links displayed are based on whether
    current is logged in.)
    Also, on the left side, there's a block showing links based on categories and brands, so that users
    have the option of view cameras for a certain category/brand.
    """
    inputs = {}
    inputs['loggedIn'] = False

    if "currentUser" in login_session :
        inputs['loggedIn'] = True
        inputs['user_id']=login_session['id']

    session = DBSession()
    cameras = session.query(Camera).all()
    inputs['cameras']=cameras
    inputs['camera length'] = len(cameras)
    if inputs['loggedIn']:
        inputs['user_id']= login_session['id']
    else:
        inputs['user_id']= 0

    brands = session.query(Brand).all()
    b_id_name_pair = {}
    for b in brands:
        b_id_name_pair[b.id]=b.name
    inputs['brands']=brands
    inputs['brand_id_name'] = b_id_name_pair

    categories = session.query(Category).all()
    for c in categories:
        c_id_name_pair = {}
        c_id_name_pair[c.id]=c.name
    inputs['categories']=categories

    return render_template('showCameras.html',inputs=inputs)


@app.route('/sookiesusedcameras/brand/<int:brand_id>')
def showCamerasWithBrand(brand_id):
    """ Display cameras of specified brand stored in the database.

    Parameters
    ----------
    brand_id: int, specified brand id for retriving.

    """
    inputs = {}
    inputs['loggedIn'] = False

    if "currentUser" in login_session :
        inputs['loggedIn'] = True
        #get user id

    session = DBSession()
    cameras = session.query(Camera).filter_by(brand_id=brand_id).all()
    inputs['cameras']=cameras
    inputs['camera length'] = len(cameras)

    if loggedIn:
        inputs['user_id']= login_session['id']
    else:
        inputs['user_id']= 0

    inputs['targetBrand'] = session.query(Brand).filter_by(id=brand_id).one()

    brands = session.query(Brand).all()
    b_id_name_pair = {}
    for b in brands:
        b_id_name_pair[b.id]=b.name
    inputs['brands']=brands
    inputs['brand_id_name'] = b_id_name_pair

    categories = session.query(Category).all()
    for c in categories:
        c_id_name_pair = {}
        c_id_name_pair[c.id]=c.name
    inputs['categories']=categories

    return render_template('showCamerasWithBrand.html', inputs=inputs)

@app.route('/sookiesusedcameras/category/<int:category_id>')
def showCamerasWithCategory(category_id):
    """ Display cameras of specified category stored in the database.

    Parameters
    ----------
    category_id: int, specified category id for retriving.

    """
    inputs = {}
    inputs['loggedIn'] = False

    if "currentUser" in login_session :
        inputs['loggedIn'] = True
        #get user id

    session = DBSession()
    cameras = session.query(Camera).filter_by(category_id=category_id).all()
    inputs['cameras']=cameras
    inputs['camera length'] = len(cameras)

    if loggedIn:
        inputs['user_id']= login_session['id']
    else:
        inputs['user_id']= 0

    inputs['targetCategory'] = session.query(Category).filter_by(id=category_id).one()

    brands = session.query(Brand).all()
    b_id_name_pair = {}
    for b in brands:
        b_id_name_pair[b.id]=b.name
    inputs['brands']=brands
    inputs['brand_id_name'] = b_id_name_pair

    categories = session.query(Category).all()
    for c in categories:
        c_id_name_pair = {}
        c_id_name_pair[c.id]=c.name
    inputs['categories']=categories
    inputs['cate_id_name'] = c_id_name_pair

    return render_template('showCamerasWithCategory.html', inputs=inputs)


@app.route('/sookiesusedcameras/use/<int:user_id>/newcamera', methods=['GET','POST'])
def addItem(user_id):
    """ Add item.

    Parameters
    ----------
    user_id: int, indicating which user owns the new item.

    """
    inputs = {}
    if "currentUser" in login_session :
        inputs['loggedIn'] = True
    else:
        return redirect(url_for('login',messages="You haven't logged in. Only users can add item. Please log in first."))

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
@app.route('/sookiesusedcameras/user/<int:user_id>')
def showMyStore(user_id):
    """ Display all cameras stored in the database for specified user.

    Parameters
    ----------
    user_id: int, indicating which user it is.

    """
    inputs = {}

    if "currentUser" in login_session :
        inputs['loggedIn'] = True
    else:
        return redirect(url_for('login',messages="You haven't logged in. Only specific users can view this store. Please log in first."))

    session = DBSession()
    cameras = session.query(Camera).filter_by(user_id=user_id).all()
    inputs['cameras']=cameras
    inputs['camera length'] = len(cameras)
    inputs['user_id']= user_id

    user = session.query(User).filter_by(id=user_id).one()
    inputs['user']=user

    brands = session.query(Brand).all()
    b_id_name_pair = {}
    for b in brands:
        b_id_name_pair[str(b.id)]=b.name
    inputs['brands']=brands
    inputs['brand_id_name'] = b_id_name_pair

    categories = session.query(Category).all()
    c_id_name_pair = {}
    for c in categories:
        c_id_name_pair[str(c.id)]=c.name
    inputs['categories']=categories
    inputs['c_id_name_pair']=c_id_name_pair

    return render_template('showMyStore.html',inputs=inputs)

@app.route('/sookiesusedcameras/user/<int:user_id>/camera/<int:camera_id>/edit', methods=['GET','POST'])
def editItem(user_id, camera_id):
    """ Edit item.

    Parameters
    ----------
    user_id: int, indicating which user this item belongs to.
    camera_id: int, specifying which camera to edit.

    """
    inputs = {}
    if "currentUser" in login_session :
        inputs['loggedIn'] = True
    else:
        return redirect(url_for('login',messages="You haven't logged in. Only specific users can modify this item. Please log in first."))

    session = DBSession()
    camEdit = session.query(Camera).filter_by(id=camera_id).one()

    if request.method == 'GET':
        return render_template('editItem.html', camera= camEdit, user_id=user_id)
    else:  # for a POST
        if request.form['name']:
            camEdit.name = request.form['name']
        if request.form['brand']:
            camEdit.brand_id=request.form['brand']
        if request.form['description']:
            camEdit.description=request.form['description']
        if request.form['price']:
            camEdit.price=request.form['price']
        if request.form['condition']:
            camEdit.condition=request.form['condition']
        session.add(camEdit)
        session.commit()

        cameras = session.query(Camera).filter_by(user_id=user_id).all()
    return redirect(url_for('showMyStore',user_id=user_id))


@app.route('/sookiesusedcameras/user/<int:user_id>/camera/<int:camera_id>/delete', methods=['GET','POST'])
def deleteItem(user_id, camera_id):
    """ Delete item.

    Parameters
    ----------
    user_id: int, indicating which user this item belongs to.
    camera_id: int, specifying which camera to delete.

    """
    inputs = {}
    if "currentUser" in login_session :
        inputs['loggedIn'] = True
    else:
        return redirect(url_for('login',messages="You haven't logged in. Only specific users can delete this item. Please log in first."))

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
    """ Retrieve JSON for all cameras. """
    session = DBSession()
    cams = session.query(Camera).all()
    return jsonify(cameras=[r.serialize for r in cams])

@app.route('/sookiesusedcameras/brand/<brand_id>/JSON')
def getCamerasWithBrand(brand_id):
    """ Retrieve JSON for all cameras with specific brand.

    Parameters
    ----------
    brand_id: int, specified brand id for retriving.

    """
    session = DBSession()
    cams = session.query(Camera).filter_by(brand_id=brand_id).all()
    return jsonify(cameras=[r.serialize for r in cams])

@app.route('/sookiesusedcameras/category/<category_id>/JSON')
def getCamerasWithCategory(category_id):
    """ Retrieve JSON for all cameras with specific category.

    Parameters
    ----------
    category_id: int, specified category id for retriving.

    """
    session = DBSession()
    cams = session.query(Camera).filter_by(category_id=category_id).all()
    return jsonify(cameras=[r.serialize for r in cams])

@app.route('/sookiesusedcameras/user/<int:user_id>/JSON')
def getMyStore(user_id):
    """ Retrieve JSON for all cameras belong to specific user.

    Parameters
    ----------
    user_id: int, indicating which user it is.

    """
    session = DBSession()
    cams = session.query(Camera).filter_by(user_id=user_id).all()
    return jsonify(cameras=[r.serialize for r in cams])

@app.route('/sookiesusedcameras/camera/<int:camera_id>/JSON')
def getMyCamera(camera_id):
    """ Retrieve JSON for a specific camera.

    Parameters
    ----------
    camera_id: int, indicate which camera it is.

    """
    session = DBSession()
    cam = session.query(Camera).filter_by(id=camera_id).all()
    return jsonify(cam[0].serialize)


if __name__ == '__main__':
    app.secret_key = "super secret key"
    app.debug = True  #rerun the code when it detects code change
    app.run(host = '0.0.0.0', port = 5000)