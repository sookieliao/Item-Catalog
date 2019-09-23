# Item-Catalog (Local Authentication)
project for section " Database with SQL and python" in Udacity full-stack nano degree course.

# Introduction
This is a simple version of web api, which utilizes sqlAlchemy for database operations and flask for web operations. **Local database authentication** is adopted. The content is a camera selling platform where user can browse all cameras available, or specify a specific brand/category of camera that they wanna have a look at. After loggin in, they can also view cameras of their own, add new camera, edit and delete existing one. This server also allow users to retrieve the JSON files for cameras/camera. Here's a quick look of how it is.

# Database setup.
1. database_setup.py is required for defining all tables needed. You can define database by running `python database_setup.py`.If you need to define your own table or add extra tables, this is the file to go.

1. lotofcameras.py is helpful for generating a few instaces for each table. By running `python lotofcameras.py`, the computer will generate a few tables and contents for you. If you want to add some more initial data, this is the file to go.

# Execute
* You can simply run the server locally by executing `python server.py`. One thing to notice is that, in server.py, the local port is specified as _localhost:5000_. If you wanna use a different port, make sure to modify the code.

### Examples
* Just to make it easier, I'll refer `localhost<<specify your port number>>/sookiesusedcameras` as __base__.

User can specifies what brand of cameras to browse with url `base/brand/<brand_id_ you_look_for>'`

![GitHub Logo](/images/showcategory.png)

If there's currently no data for specific category/brand/user, or just in general, user shall see a message indicating that.

![GitHub Logo](/images/empty.png)

For browsing user's own page, add, edit or delete items, user will have to log in first by clicking the "Login" link, and page as follow will show up.

![GitHub Logo](/images/userlogin.png)


After logging in, users will be redirect to his/her own page with url  `base/user/<__user_id__>'`

![GitHub Logo](/images/showMyStore.png)

User can add an item by click the "AddItem", page will pop up with url `base/user/<__user_id__>/newcamera'`

![GitHub Logo](/images/addItem.png)

edit an item with url `base/user/<user_id>/camera/<id_for_camera_to_edit__>/edit'`
![GitHub Logo](/images/edit.png)

or delete an item with url `base/user/<__user_id__>/camera/<__id_for_camera_to_delete__>/delete'`
![GitHub Logo](/images/delete.png)

Per request, user can also fetch the JSON files for specified/all cameras
*fetch all cameras ->  `base/JSON'`
*fetch all cameras for a specific brand -> `base/brand/<__specify the brand_id__>/JSON'`
*fetch all cameras under a specific user ->  `base/user/<__specify the user_id__>/JSON'`
*fetch a specific camera under a specific user -> `base/user/<__specify the user_id__>/camera/<__the_camera_id__>JSON'`

![GitHub Logo](/images/api.png)




# Notes
* static folder contains basic styling for all templates.
* templates folder contains all templates 
