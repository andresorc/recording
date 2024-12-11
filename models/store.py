from db import db

class StoreModel(db.Model):
    __tablename__= "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)  
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete") #lazy="dynamic" gives the client the chance to make a query or not in order to get the items