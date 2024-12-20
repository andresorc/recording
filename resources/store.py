from sqlite3 import IntegrityError
import uuid
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError
from db import db

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
       store = StoreModel.query.get_or_404(store_id)
       db.session.delete(store)
       db.session.commit()
       return {"message": "Store deleted"}, 200



@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store) # it prepares the item to be added to the database
            db.session.commit()  # it actually adds the item to the database
        except IntegrityError:
            abort(400, message="A store with that name already exists.") 
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.") 

        return store