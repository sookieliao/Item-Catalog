from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Brand, User, Camera

# Connect to database
#engine = create_engine('sqlite:///restaurantmenu.db')
#Base.metadata.bind = engine
#DBSession = sessionmaker(bind=engine)


# Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


# Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}
# items = []


@app.route('/')
@app.route('/sookiesusedcameras')
def showCameras():
    return "this page will show all products."

@app.route('/sookiesusedcameras/brand=<brand_name>')
def showCamerasWithBrand(brand_name):
    return "this page will show all products with brand %s" % brand_name

@app.route('/sookiesusedcameras/condition=<condition>')
def showCamerasWithCondition(condition):
    return "this page will show all products that are %s" % condition

@app.route('/sookiesusedcameras/new')
def checkUserWhenAddItem():
    return "show login/additem page depends on whether user logs in."

@app.route('/sookiesusedcameras/user=<int:user_id>/new', methods=['GET','POST'])
def addItem(user_id):
    return "show additem page."

#try @app.route('/sookiesusedcameras/mystore=<int:user_id>', methods=['GET','POST'])
@app.route('/sookiesusedcameras/mystore/user=<int:user_id>')
def showMyStore(user_id):
    return 'This is the page displaying my store'

@app.route('/sookiesusedcameras/user=<int:user_id>/camera=<int:camera_id>/edit', methods=['GET','POST'])
def editItem(user_id, camera_id):
    return 'this is the page for editing selling camera'


@app.route('/sookiesusedcameras/use=<int:user_id>/camera=<int:camera_id>/delete', methods=['GET','POST'])
def deleteItem(user_id, camera_id):
    return 'this is the page for deleting selling camera'



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

#try @app.route('/sookiesusedcameras/mystore=<int:user_id>', methods=['GET','POST'])
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