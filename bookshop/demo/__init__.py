from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config.from_object('demo.setting')

db = SQLAlchemy(app)

from demo.model.models import book,customer,order_item,orders

from demo.controller import message
db.drop_all()
db.create_all()