from db import db

#This creates a mapping between a row in a table to a python class and is therefore a python object
class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True) #id column will pre-populate incrementally starting at 1 and going up from there
    name = db.Column(db.String(80), unique=True, nullable=False) #Column name is a string with max 80 characters, string must be unique and nullable=False means you can't make an item with no name
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic") #lazy=dynamic means the items won't be fetched from the databas until we tell it to
    #cascade="all, delete, delete-orphan" means that when a store is deleted, all of its items will be deleted as well. delete-orphan means that if an item is deleted, it's store will be deleted as well
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")