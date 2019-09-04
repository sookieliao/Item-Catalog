from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Brand, User, Camera

# Connect to database
engine = create_engine('sqlite:///cameras.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


# Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


# Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}
cameras = []
camera = {'name':'canon 650d', 'id':3, 'brand_name':'canon','description':'nice','condition':'moderate','price':'$700'}


@app.route('/')
@app.route('/sookiesusedcameras')
def showCameras():
    session = DBSession()
    cameras = session.query(Camera).all()
    return render_template('showCameras.html',cameras = cameras, length=len(cameras))

@app.route('/sookiesusedcameras/brand=<int:brand_id>')
def showCamerasWithBrand(brand_id):
    session = DBSession()
    cameras = session.query(Camera).filter_by(brand_id=brand_id).all()
    brand = session.query(Brand).filter_by(id=brand_id).one()
    return render_template('showCamerasWithBrand.html',cameras = cameras, length=len(cameras), brand=brand.name)

@app.route('/sookiesusedcameras/condition=<condition>')
def showCamerasWithCondition(condition):
    session = DBSession()
    cameras = session.query(Camera).filter_by(condition=condition).all()
    return render_template('showCamerasWithCondition.html',cameras = cameras, length=len(cameras), condition=condition)

@app.route('/sookiesusedcameras/login')
def authendicate():
    return 'perform authendicattion.'

@app.route('/sookiesusedcameras/new')
def checkUserWhenAddItem():
    # if user is not log in, redirect to log in page
    # else render addItem()
    return "show login/additem page depends on whether user logs in."

@app.route('/sookiesusedcameras/user=<int:user_id>/new', methods=['GET','POST'])
def addItem(user_id):
    # ideally, when user cancel craeting, it should be back to whever they were.
    if request.method == 'GET':
        return render_template('addItem.html', user_id=user_id)
    else:  # for a POST
        session = DBSession()
        newItem = Camera(name=request.form['name'],brand_id=request.form['brand'],
            description=request.form['description'],price=request.form['price'],condition=request.form['condition'])
        session.add(newItem)
        session.commit()

        cameras = session.query(Camera).filter_by(user_id=user_id)
    return redirect(url_for('showMyStore.html', cameras = cameras, length=len(cameras), user_id=user_id))

#try @app.route('/sookiesusedcameras/mystore=<int:user_id>', methods=['GET','POST'])
@app.route('/sookiesusedcameras/mystore/user=<int:user_id>')
def showMyStore(user_id):
    session = DBSession()
    cameras = session.query(Camera).filter_by(user_id=user_id).all()
    return render_template('showMyStore.html',cameras = cameras, length=len(cameras), user_id=user_id)

@app.route('/sookiesusedcameras/user=<int:user_id>/camera=<int:camera_id>/edit', methods=['GET','POST'])
def editItem(user_id, camera_id):
    if request.method == 'GET':
        return render_template('editItem.html', camera= camera, user_id=user_id)
    else:  # for a POST
        session = DBSession()
        camEdit = session.query(Camera).filter_by(id=camera_id).one()
        camEdit.name = request.form['name']
        camEdit.brand_id=request.form['brand']
        camEdit.description=request.form['description']
        camEdit.price=request.form['price']
        camEdit.condition=request.form['condition']
        session.add(camEdit)
        session.commit()

        cameras = session.query(Camera).filter_by(user_id=user_id)
    return redirect(url_for('showMyStore.html', cameras = cameras, length=len(cameras), user_id=user_id))


@app.route('/sookiesusedcameras/user=<int:user_id>/camera=<int:camera_id>/delete', methods=['GET','POST'])
def deleteItem(user_id, camera_id):
    if request.method == 'GET':
        return render_template('deleteItem.html', camera= camera, user_id=user_id)
    else:  # for a POST
        session = DBSession()
        camDelete = session.query(Camera).filter_by(id=camera_id).one()
        session.delete(camDelete)
        session.commit()
        cameras = session.query(Camera).filter_by(user_id=user_id)
    return redirect(url_for('showMyStore.html', cameras = cameras, length=len(cameras), user_id=user_id))


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