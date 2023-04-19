from flask import render_template
from flask import request 
from flask import jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json

from demo.model.models import book,customer,order_item,orders,book_Schema,customer_Schema,order_Schema,orderItem_Schema,bookname_cname_Schema

from demo import db, app


@app.route('/init/')
def main_page():
    book1 = book(isbn='0002', bookname='论语', author='孔子', price=10.0, number=5)
    book2 = book(isbn='0003', bookname='几何', author='欧几里得', price=25.0, number=3)
    book3 = book(isbn='0004', bookname='哈姆雷特', author='莎士比亚', price=15.0, number=4)
    db.session.add_all([book1,book2,book3])

    customer1 = customer(customer_id='0002', name='王五', address='东兴路', city='苏州')
    db.session.add(customer1)

    orders1 = orders(order_id='0002', customer_id='0002', amount=60, date=datetime.now())
    db.session.add(orders1)

    order_item1 = order_item(oi_id='0001', order_id='0002', isbn='0002', quantity=1)
    order_item2 = order_item(oi_id='0002', order_id='0002', isbn='0003', quantity=2)
    db.session.add_all([order_item1,order_item2])

    db.session.commit()
    return '初始化成功'

@app.route('/hello/',methods=["GET","POST"])
def hello_name():
    name = request.args.get('name')
    return 'Hello! %s' %name

@app.route('/book/add/',methods=["POST"])
def add_book():
	#1. 添加数据
    the_book = request.form
    new_book = book(isbn=the_book['isbn'], 
                    bookname=the_book['bookname'],
                    author=the_book['author'], 
                    price=the_book['price'], 
                    number=the_book['number'])

    db.session.add(new_book) 
    db.session.commit()
	
    return "数据添加成功"

@app.route('/book/select/',methods=["POST"])
def select_book():
	#2.查询数据
    bn = request.form['bookname']
    the_book = book.query.filter_by(bookname = bn)[0]
    schema = book_Schema()    
    data_dict = schema.dump(the_book).data

    return jsonify(data_dict)

@app.route('/book/update/',methods=["PUT"])
def update_book():
    #3.修改数据
    if request.method == "POST":
        isbn = request.form['isbn']
        the_book = book.query.filter_by(isbn=isbn)[0]
        if the_book != None:
            the_book.bookname =request.form['bookname']
            db.session.commit()
        
            return '数据修改成功'
    return '数据修改失败'

@app.route('/book/del/',methods=["DELETE"])
def del_book():
    #4.删除数据
    isbn = request.form["isbn"]
    res = book.query.filter_by(isbn=isbn).delete()
    db.session.commit()
    print(res)
    return '数据删除成功'

@app.route('/customer/')
def customer_list():
    return 'customer list'

@app.route('/customer/add/', methods=['POST'])
def add_customer():
    #1. 添加数据
    the_customer = request.form
    new_customer = customer(customer_id = the_customer['customer_id'], 
                    name = the_customer['name'],
                    address = the_customer['address'], 
                    city = the_customer['city'])

    db.session.add(new_customer)
    db.session.commit()
        
    return "数据添加成功"

@app.route('/customer/select/', methods=["POST"])
def select_customer():
    #2. 查询数据
    if request.method == "POST":
        id = request.form["customer_id"]
        the_customer = customer.query.filter_by(customer_id= id)[0]
        schema = customer_Schema()
        data_dict = schema.dump(the_customer)
        return jsonify(data_dict)

@app.route('/customer/update/', methods=["PUT"])
def update_customer():
    #3.修改数据
    id = request.form["customer_id"]
    the_customer = customer.query.filter_by(customer_id= id)[0]
    if the_customer != None:
        the_customer.name = request.form["name"]
        db.session.commit()

        return '数据修改成功'
    return '数据修改失败'

@app.route('/customer/del/', methods=["DELETE"])
def del_customer():
    #4.删除数据
    
    id = request.form["customer_id"]
    res = book.query.filter_by(customer_id= id).delete()
    db.session.commit()

    return '数据删除失败'

@app.route('/order/list')
def order_list():
    data = order_item.query.all()
    for item in data:
        print(item.order_id)
    return '查询成功'


@app.route('/order/select/')
def select_order():
    data = db.session.query(orders).join(
        (order_item, orders.order_id == order_item.order_id),
        (customer, customer.customer_id == orders.customer_id),
    ).join(book, book.isbn == order_item.isbn).\
    with_entities(book.bookname, customer.name).\
    all()
    schema = bookname_cname_Schema()
    for item in data:
        item_dict = schema.dump(item).data
        print(type(item_dict))
        item_json = json.dumps(item_dict)
        print(type(item_json))
    

    return '数据查询成功'

@app.route('/buybook/')
def buybook():
    #模拟传入参数
    oi_id = '0003'
    order_id = '0001'
    isbn = '0002'
    customer_id = '0002'
    quantity = 1

    new_orderItem = order_item(oi_id = oi_id, order_id=order_id, isbn=isbn, quantity=quantity)#
    db.session.add(new_orderItem)#创建新书籍-订单
    print("order_item 创建成功")
    
    the_book = book.query.filter_by(isbn=isbn)[0]
    tmp = the_book.number
    the_book.number = tmp - quantity#书籍数量减去购买数量
    print("书籍出库成功")
    
    the_order = orders.query.filter_by(order_id=order_id)#查询用户订单
    if the_order == None:#如果没有用户订单则为用户本次购物第一单
        new_orders = orders(order_id=order_id, customer_id=customer_id, 
                            amount=the_book.price * quantity, date=datetime.now())
        db.session.add(new_orders)#添加新订单

    db.session.commit()#提交
    return '买书成功'