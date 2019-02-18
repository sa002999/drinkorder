from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:T100408103@localhost/DB'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pamngufmlbjoux:b0ddc1ecac0c0ddf507cd42eee8fb2d8cb17a348108e6bfa74187bfd6469e522@ec2-54-243-128-95.compute-1.amazonaws.com:5432/d2jfemfq5lgr0h'
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
                           , server_default=db.func.current_timestamp()
                           , server_onupdate=db.func.current_timestamp())

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


if __name__ == '__main__':
    manager.run()
    print ("Manager run")
