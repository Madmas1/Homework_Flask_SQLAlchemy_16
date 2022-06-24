# Run модуль приложения

import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from db_model import *
from datetime import date

app = Flask(__name__)

# Конфиги для фласка
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newbase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

app.url_map.strict_slashes = False

db = SQLAlchemy(app)


# Роуты пользовательских данных
@app.route("/users", methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        # Выдаем данные по всем пользователям в базе
        data = db.session.query(User).all()
        result = [user.to_dict() for user in data]
        return jsonify(result)
    elif request.method == 'POST':
        # Добавляем нового пользователя из запроса
        try:
            user = json.loads(request.data.decode('utf8'))
            db.session.add(User(
                id=user['id'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                age=user['age'],
                email=user['email'],
                role=user['role'],
                phone=user['phone']
            ))
            db.session.commit()
            db.session.close()
            return "New user successful add"
        except Exception as e:
            return e


@app.route("/users/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def get_user_by_id(id):
    if request.method == 'GET':
        # Выдаем данные пользователя по его Id
        user_data = db.session.query(User).filter(User.id == id).one()
        result = user_data.to_dict
        return jsonify(result)
    elif request.method == 'PUT':
        # Редактируем данные пользователя по его Id
        user = db.session.query(User).filter(User.id == id).one()
        user_data = json.loads(request.data.decode('utf8'))
        if not user:
            return "User not found"
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.age = user_data['age']
        user.email = user_data['email']
        user.role = user_data['role']
        user.phone = user_data['phone']
        db.session.add(user)
        db.session.commit()
        db.session.close()
        return f"User № {id} successful changed"
    elif request.method == 'DELETE':
        # Удаляем данные пользователя по его Id
        try:
            db.session.query(User).filter(User.id == id).delete()
            db.session.commit()
            db.session.close()
            return f"User № {id} successful deleted"
        except Exception as e:
            return e


# Роуты данных по заказам
@app.route("/orders", methods=['GET', 'POST'])
def get_orders():
    if request.method == 'GET':
        # Выдаем данные по всем заказам в базе
        data = db.session.query(Order).all()
        result = [order.to_dict() for order in data]
        return jsonify(result)
    elif request.method == 'POST':
        # Добавляем новый заказ в базу
        try:
            order = json.loads(request.data.decode('utf-8'))
            start_moth, start_day, start_year = [int(i) for i in order['start_date'].split("/")]
            end_moth, end_day, end_year = [int(i) for i in order['end_date'].split("/")]
            db.session.add(Order(
                id=order['id'],
                name=order['name'],
                description=order['description'],
                start_date=date(year=start_year, month=start_moth, day=start_day),
                end_date=date(year=end_year, month=end_moth, day=end_day),
                address=order['address'],
                price=order['price'],
                customer_id=order['customer_id'],
                executor_id=order['executor_id']
            ))
            db.session.commit()
            db.session.close()
            return "New order successful add"
        except Exception as e:
            return e


@app.route("/orders/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def get_order_by_id(id):
    if request.method == 'GET':
        # Выдаем данные заказа по его Id
        order = db.session.query(Order).filter(Order.id == id).one()
        result = order.to_dict()
        return jsonify(result)
    elif request.method == 'PUT':
        # Редактируем данные заказа по его Id
        order = db.session.query(Order).filter(Order.id == id).one()
        order_data = json.loads(request.data.decode('utf8'))
        start_moth, start_day, start_year = [int(i) for i in order_data['start_date'].split("/")]
        end_moth, end_day, end_year = [int(i) for i in order_data['end_date'].split("/")]
        if not order:
            return "Order not found"
        order.name = order_data['name']
        order.description = order_data['description']
        order.start_date = date(year=start_year, month=start_moth, day=start_day)
        order.end_date = date(year=end_year, month=end_moth, day=end_day)
        order.address = order_data['address']
        order.price = order_data['price']
        order.customer_id = order_data['customer_id']
        order.executor_id = order_data['executor_id']
        db.session.add(order)
        db.session.commit()
        db.session.close()
        return f"Order № {id} successful changed"
    elif request.method == 'DELETE':
        # Удаляем данные заказа по его Id
        try:
            db.session.query(Order).filter(Order.id == id).delete()
            db.session.commit()
            db.session.close()
            return f"Order № {id} successful deleted"
        except Exception as e:
            return e


# Роуты данных предложений
@app.route("/offers", methods=['GET', 'POST'])
def get_offers():
    if request.method == 'GET':
        # Выдаем данные по всем предложениям
        data = db.session.query(Offer).all()
        result = [offer.to_dict() for offer in data]
        return jsonify(result)
    elif request.method == 'POST':
        # Добавляем новое предложение в базу
        try:
            offer = json.loads(request.data.decode('utf-8'))
            db.session.add(Offer(
                id=offer['id'],
                executor_id=offer['executor_id'],
                order_id=offer['order_id']
            ))
            db.session.commit()
            db.session.close()
            return "New offer successful add"
        except Exception as e:
            return e


@app.route("/offers/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def get_offer_by_id(id):
    if request.method == 'GET':
        # Выдаем данные предложения по его Id
        offer = db.session.query(Offer).filter(Offer.id == id).one()
        result = offer.to_dict()
        return jsonify(result)
    elif request.method == 'PUT':
        # Изменяем данные предложения по его Id
        offer = db.session.query(Offer).filter(Offer.id == id).one()
        offer_data = json.loads(request.data.decode('utf8'))
        if not offer:
            return "Offer not found"
        offer.executor_id = offer_data['executor_id']
        offer.order_id = offer_data['order_id']
        db.session.add(offer)
        db.session.commit()
        db.session.close()
        return f"Offer № {id} successful changed"
    elif request.method == 'DELETE':
        # Удаляем данные предложения по его Id
        try:
            db.session.query(Offer).filter(Offer.id == id).delete()
            db.session.commit()
            db.session.close()
            return f"Offer № {id} successful deleted"
        except Exception as e:
            return e


if __name__ == '__main__':
    app.run()
