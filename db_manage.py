# Модуль загрузки данных из JSON в базу
import json
from db_model import *
from datetime import date

with open("users.json", 'r', encoding='utf-8') as file:
    USERS = json.load(file)

with open("offers.json", 'r', encoding='utf-8') as file:
    OFFERS = json.load(file)

with open("orders.json", 'r', encoding='utf-8') as file:
    ORDERS = json.load(file)


# Получаем данные пользователей из JSON файла
for user in USERS:
    db.session.add(User(
        id=user['id'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        age=user['age'],
        email=user['email'],
        role=user['role'],
        phone=user['phone']
    ))
    db.create_all()
    db.session.commit()

# Получаем данные предложений из JSON файла
for offer in OFFERS:
    db.session.add(Offer(
        id=offer['id'],
        order_id=offer['order_id'],
        executor_id=offer['executor_id'],
    ))
    db.create_all()
    db.session.commit()


# Получаем данные заказов из JSON файла
for order in ORDERS:
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
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    pass
