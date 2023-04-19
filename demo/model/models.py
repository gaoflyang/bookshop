from datetime import datetime
from marshmallow import Schema, fields
from demo import app, db


class book(db.Model):
    '''书籍模型'''
    isbn = db.Column(db.String(20), primary_key=True)
    bookname = db.Column(db.String(40))
    author = db.Column(db.String(40))
    price = db.Column(db.Float)
    number = db.Column(db.Integer)

    __tablename___ ='book'

    def save(self):
        db.session.add(self)
        db.session.commit()

class customer(db.Model):
    '''顾客模型'''
    customer_id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(40))
    address = db.Column(db.String(40))
    city = db.Column(db.String(20))

    __tablename__ = 'customer'


    def save(self):
        db.session.add(self)
        db.session.commit()

class orders(db.Model):
    '''顾客购买-订单'''
    order_id = db.Column(db.String(20), primary_key=True)
    customer_id = db.Column(db.String(20))
    amount = db.Column(db.String(20))
    date = db.Column(db.DateTime)

    __tablename__ = 'orders'

    def save(self):
        db.session.add(self)
        db.session.commit()

class order_item(db.Model):
    '''书籍-订单'''
    oi_id = db.Column(db.String(20), primary_key=True)
    order_id = db.Column(db.String(20))
    isbn = db.Column(db.String(20))
    quantity = db.Column(db.Integer)

    __tablename__ = 'order_item'

    def save(self):
        db.session.add(self)
        db.session.commit()

class book_Schema(Schema):
    isbn = fields.String(data_key='isbn')
    bookname = fields.String(data_key='bookname')
    author = fields.String(data_key='author')
    price = fields.Float(data_key='price')
    number = fields.Integer(data_key='number')

class customer_Schema(Schema):
    customerid = fields.String(data_key='customerid')
    name = fields.String(data_key='name')
    address = fields.String(data_key='address')
    city = fields.String(data_key='city')

class order_Schema(Schema):
    orderid = fields.String(data_key='orderid')
    customerid = fields.String(data_key='customerid')
    amount = fields.Float(data_key='amount')
    date = fields.DateTime(data_key='date')

class orderItem_Schema(Schema):
    orderid = fields.String(data_key='orderid')
    isbn = fields.String(data_key='isbn')
    quantity = fields.Integer(data_key='quantity')

class bookname_cname_Schema(Schema):
    bookname = fields.String(data_key='bookname')
    name = fields.String(data_key='name')