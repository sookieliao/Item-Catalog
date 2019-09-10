from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Brand, User, Camera

engine = create_engine('sqlite:///cameras.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Category
mirrorless = Category(name='Mirrorless Camera')
camcoder = Category(name='Camcoder')
dslr = Category(name='DSLR')
session.add(mirrorless)
session.add(camcoder)
session.add(dslr)
session.commit()

# Brand
canon = Brand(name='Canon')
nikon = Brand(name='Nikon')
sony = Brand(name='Sony')
sigma = Brand(name='Sigma')
leica = Brand(name='Leica')
fujifilm = Brand(name='Fujifilm')
session.add(canon)
session.add(nikon)
session.add(sony)
session.add(sigma)
session.add(leica)
session.add(fujifilm)
session.commit()

# User1 and her cameras
user1 = User(name="Sookie Sookie",email='abc@gmail.com',password='smartsookie')
session.add(user1)
session.commit()

cam1 = Camera(name="EOS Rebel SL3 DSLR Camera with EF-S 18-55mm IS STM Lens", brand_id=1,
       description="This Canon EF-S 18-55mm f/4-5.6 lens features a non-retracting design and lightweight body that's easy to carry around.",
       price='$500,00', condition='excellent',category_id=3, user_id=1)
session.add(cam1)

cam2 = Camera(name="Handycam CX405 Flash Memory Camcorder - Black", brand_id=3,
       description="This Sony Handycam HDRCX405/B camcorder enables you to capture video footage with 1920 x 1080 resolution and sharp still images.",
       price='$100,00', condition='not so well',category_id=2, user_id=1)
session.add(cam2)

cam3 = Camera(name="VIXIA HF R800 HD Flash Memory Camcorder - Black", brand_id=1,
       description="This Canon Vixia HF R800 camcorder has an onboard DIGIC DV 4 image processor, which captures extra light and removes noise for an enhanced image.",
       price='$300,00', condition='moderate',category_id=2, user_id=1)
session.add(cam3)

session.commit()


# User2 and his cameras
user2 = User(name="Kevin kevin",email='kkvin@happy.com',password='kkvin')
session.add(user2)
session.commit()

cam1 = Camera(name="EOS RP Mirrorless Camera with EF 24-105mm f/3.5-5.6 IS STM Lens", brand_id=1,
       description="This Canon mirrorless camera lets you capture 4K videos for added versatility, and the 24-105mm adjustable lens is ideal for wide-angle shots.",
       price='$999,00', condition='excellent',category_id=1, user_id=2)
session.add(cam1)

cam2 = Camera(name="Alpha a6400 Mirrorless Camera with E 18-135mm f/3.5-5.6 OSS Lens - Black", brand_id=3,
       description="This Sony Alpha a6400 mirrorless camera comes with an E 18-135mm lens, which works as both a wide-angle and medium telephoto lens for added versatility.",
       price='$899,00', condition='moderate',category_id=1, user_id=2)
session.add(cam2)

cam3 = Camera(name="D750 DSLR Camera with AF-S NIKKOR 24-120mm f/4G ED VR Lens - Black", brand_id=2,
       description="This Nikon D750 DSLR camera features a 24.3-megapixel FX-format CMOS sensor and comes with an AF-S NIKKOR 24-120mm f/4G ED VR lens, so you can easily capture sharp images and high-definition video footage.",
       price='$1,200,00',condition='moderate',category_id=2, user_id=2)
session.add(cam3)

session.commit()



print "added menu items!"