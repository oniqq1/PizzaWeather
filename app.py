import requests
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "oinqq_solo_ruster52_2009"




def create_connect_bd():

    sql_conection = sqlite3.connect('pizza.db')
    cursor = sql_conection.cursor()
    try:
        sqlite_create_table_query = """CREATE TABLE pizzas
                                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            name TEXT UNIQUE,
                                            description TEXT NOT NULL,
                                            cost INTEGER NOT NULL)"""


        try:
            cursor.execute(sqlite_create_table_query)
            sql_conection.commit()
            print(f'DB created')
        except sqlite3.Error as error:
            print(f'DB connected but error - {error}')


    except sqlite3.Error as error:
        print(f'In DB error - {error}')
    finally:
        if (sql_conection):
            cursor.close()
            sql_conection.close()


@app.get('/')
def index():
    return render_template("index.html")


def get_weather() -> int:
    info = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat=50.4500336&lon=30.5241361&appid=f11d3ee10670aac00294ac8ae927cde4")
    info_text = info.json()
    info_main = info_text["main"]
    info_temp = info_main["temp"]
    return (int(info_temp) - 273)


def get_pizza() -> dict:
    data_pizza = {}

    sql_conection = sqlite3.connect('pizza.db')
    cursor = sql_conection.cursor()

    try:
        sqlite_values_query = 'SELECT * FROM pizzas'
        cursor.execute(sqlite_values_query)
        data_pizza['pizzas'] = cursor.fetchall()

    finally:
        if (sql_conection):
            cursor.close()
            sql_conection.close()

    print(data_pizza.get("pizzas"))
    return data_pizza


@app.get('/weather')
def weather_pizza():
    data = {}
    data_pizza = get_pizza().get("pizzas")
    pizza = ''
    photo = ''
    temperature = get_weather()

    if temperature <= -30:
        pizza = data_pizza[0]
        photo = 'https://gudwork.com.ua/storage/uploads/menu_images/WMFqAHnL0kt5WGOg9SyDVn0hLO125yvO8zZcMa0q.jpg'
    elif temperature <= -15:
        pizza = data_pizza[1]
        photo = 'https://gudwork.com.ua/storage/uploads/menu_images/uK3wEm8x0UrlOZBK25J5BJGUEJqaYWNfewtCqllj.jpg'
    elif temperature >= 20:
        pizza = data_pizza[3]
        photo = 'https://images.silpo.ua/products/1600x1600/webp/de261e76-1f81-48f2-9008-32dc61da16c8.png'
    elif temperature > -15:
        pizza = data_pizza[2]
        photo = 'https://gudwork.com.ua/storage/uploads/menu_images/aruNm56ARvYumVT7KPvOVzlfRWvJYqLH31Fe5QJv.jpg'

    data['temp'] = temperature
    data["pizza"] = pizza



    return render_template("weather.html",data=data,photo=photo)

app.run(port=9091, debug=True)