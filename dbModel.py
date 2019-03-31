from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import datetime

SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class UserData(db.Model):
    __tablename__ = 'UserData'

    Id = db.Column(db.Integer, primary_key=True)
    DisplayName = db.Column(db.String(64))
    UserID = db.Column(db.String(64))
    PictureURL = db.Column(db.String(256))
    StatusMessage = db.Column(db.String(256))
    CreateDate = db.Column(db.DateTime
                         , default=datetime.datetime.now
                         , onupdate=datetime.datetime.now)

    def __init__(self
                 , DisplayName
                 , UserID
                 , PictureURL
                 , StatusMessage
                 ):
        self.DisplayName = DisplayName
        self.UserID = UserID
        self.PictureURL = PictureURL
        self.StatusMessage = StatusMessage

class OrderList(db.Model):
    __tablename__ = 'OrderList'

    Id = db.Column(db.Integer, primary_key=True)
    CreateDate = db.Column(db.DateTime
                         , default=datetime.datetime.now
                         , onupdate=datetime.datetime.now)
    Creator = db.Column(db.String(64))
    DrinkVender = db.Column(db.String(64))

    def __init__(self
                 , Creator
                 , DrinkVender
                 ):
        self.Creator = Creator
        self.DrinkVender = DrinkVender

class OrderDetail(db.Model):
    __tablename__ = 'OrderDetail'

    Id = db.Column(db.Integer, primary_key=True)
    Order_Index = db.Column(db.Integer, default=-1)
    Orderer = db.Column(db.String(64))
    Drink_Size = db.Column(db.String(64))
    Drink_Item = db.Column(db.String(64))
    Drink_Ice = db.Column(db.String(64))
    Drink_Sugar = db.Column(db.String(64))
    CreateDate = db.Column(db.DateTime
                         , default=datetime.datetime.now
                         , onupdate=datetime.datetime.now)

    def __init__(self
                 , Order_Index
                 , Orderer
                 , Drink_Size
                 , Drink_Item
                 , Drink_Ice
                 , Drink_Sugar
                 ):
        self.Order_Index = Order_Index
        self.Orderer = Orderer
        self.Drink_Size = Drink_Size
        self.Drink_Item = Drink_Item
        self.Drink_Ice = Drink_Ice
        self.Drink_Sugar = Drink_Sugar

if __name__ == '__main__':
    manager.run()
    print ("Manager run")
