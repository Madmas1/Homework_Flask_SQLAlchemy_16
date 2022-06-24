with open("orders.json", 'r', encoding='utf-8') as file:
    data_users = file.read()

data_users = data_users.replace("\'", "\"")

with open("orders.json", 'w', encoding='utf-8') as file:
    file.write(data_users)

if __name__ == '__main__':
    pass
