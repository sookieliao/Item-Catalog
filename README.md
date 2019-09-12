# Item-Catalog
project for section " Database with SQL and python" in Udacity full-stack nano degree course.

# Introduction
This is a simple version of web api, which utilizes sqlAlchemy for database operations and flask for web operations. Local database authentication is adopted. The content is a camera selling platform where user can browse all cameras available, or specify a specific brand/category of camera that they wanna have a look at. After loggin in, they can also view cameras of their own, add new camera, edit and delete existing one. This server also allow users to retrieve the JSON files for cameras/camera. Here's a quick look of how it is.
### Examples
User can specifies what brand of cameras to browse with url _localhost:5000/sookiesusedcameras/brand/<__specific the brand id that you wanna look for__>'_

![GitHub Logo](/images/showcategory.png)

If there's currently no data for specific category/brand/user, or just in general, user shall see a message indicating that.

![GitHub Logo](/images/empty.png)

For browsing user's own page, add, edit or delete items, user will have to log in first by clicking the "Login" link, and page as follow will show up.

![GitHub Logo](/images/login.png)


After logging in, users will be redirect to his/her own page with url  _localhost:5000/sookiesusedcameras/user/<__user_id__>'_

![GitHub Logo](/images/showMyStore.png)


User can add an item by click the "AddItem", page will pop up with url _localhost:5000/sookiesusedcameras/user/<__user_id__>/newcamera'_

![GitHub Logo](/images/addItem.png)

edit an item with url localhost:5000/sookiesusedcameras/user/<__user_id__>/camera/<__id_for_camera_to_edit__>/edit'_
![GitHub Logo](/images/edit.png)

or delete an item with url _localhost:5000/sookiesusedcameras/user/<__user_id__>/camera/<__id_for_camera_to_delete__>/delete'_

Per request, user can also fetch the JSON files for specified/all cameras
fetch all cameras ->  _localhost:5000/sookiesusedcameras/JSON'_
fetch all cameras for a specific brand ->  _localhost:5000/sookiesusedcameras/brand/<__specify the brand_id__>/JSON'_
fetch all cameras under a specific user ->  _localhost:5000/sookiesusedcameras/user/<__specify the user_id__>/JSON'_
fetch a specific camera under a specific user ->  _localhost:5000/sookiesusedcameras/user/<__specify the user_id__>/camera/<__the_camera_id__>JSON'_

![GitHub Logo](/images/api.png)


# Database setup.
1. database_setup.py is required for defining all tables needed. You can define database by running `python database_setup.py`.If you need to define your own table or add extra tables, this is the file to go.

1. lotofcameras.py is helpful for generating a few instaces for each table. By running `python lotofcameras.py`, the computer will generate a few tables and contents for you. If you want to add some more initial data, this is the file to go.

# Execute
* You can simply run the server locally by executing `python server.py`. One thing to notice is that, in server.py, the local port is specified as _localhost:5000_. If you wanna use a different port, make sure to modify the code.

# Notes
* static folder contains basic styling for all templates.
* templates folder contains all templates 
