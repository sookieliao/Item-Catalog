# Item-Catalog
project for section " Database with SQL and python" in Udacity full-stack nano degree course.

# Introduction
This is a simple version of web api, which utilizes sqlAlchemy for database operations and flask for web operations. Local database authentication is adopted. The content is a camera selling platform where user can browse all cameras available, or specify a specific brand/category of camera that they wanna have a look at. After loggin in, they can also view cameras of their own, add new camera, edit and delete existing one. This server also allow users to retrieve the JSON files for cameras/camera.

# Database setup.
1. database_setup.py is required for defining all tables needed. You can define database by running `python database_setup.py`.If you need to define your own table or add extra tables, this is the file to go.

1. lotofcameras.py is helpful for generating a few instaces for each table. By running `python lotofcameras.py`, the computer will generate a few tables and contents for you. If you want to add some more initial data, this is the file to go.

# Execute
* You can simply run the server locally by executing `python server.py`. One thing to notice is that, in server.py, the local port is specified as _localhost:5000_. If you wanna use a different port, make sure to modify the code.

# Notes
* static folder contains basic styling for all templates.
* templates folder contains all templates 
