import requests
from flask import Flask, render_template ,redirect , url_for ,request ,flash
import sqlite3
from poll import poll_data


from flask_wtf import FlaskForm
from wtforms import StringField , BooleanField , SubmitField



f_n = 'dataData.txt'

app = Flask(__name__)
app.config["SECRET_KEY"] = "oinqq_solo_ruster52_2009"


class Vote(FlaskForm):
    vote = BooleanField("Good_or_Bad")
    text = StringField("Text")
    submit = SubmitField("Submit")

@app.get('/votes/')
def votes():
    ans = [['cool',True],['bad',False],['ok',True]]

    return render_template("VOTES.html",vote=ans)

@app.get('/vote/')
def vote():
    form = Vote()

    return render_template("VOTE.html",form=form)
@app.post('/vote/')
def post():
    vote = request.form.get("vote")
    if vote == None:
        vote = False
    else:
        vote= True
    return (f"text = {request.form.get("text")} "
            f"vote = {vote}")

@app.get("/test")
def test():
    return render_template("poll.html", data=poll_data)


@app.get('/poll')
def poll():
    answer = request.args.get("field")
    with open(f_n,"a") as file:
        file.write(answer + "\n")

    return answer
@app.get('/results')
def results():
    new_votes = {}
    with open(f_n,"r") as file:
        votes = file.read().split()

    for vote in votes:
        new_votes[vote] = votes.count(vote)


    keys = list(new_votes.keys())


    return render_template("results.html",data=new_votes , keys=keys)
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
def main():
    return render_template("main.html")


def get_weather() -> int:
    info = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat=50.4500336&lon=30.5241361&appid=f11d3ee10670aac00294ac8ae927cde4")
    info_text = info.json()
    info_main = info_text["main"]
    info_temp = info_main["temp"]
    return (int(info_temp) - 273)


def get_pizza():
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


@app.get("/pizzas/")
def get_pizzas():
    pizzas = get_pizza().get("pizzas")
    return render_template("pizzas.html",pizzas=pizzas)


@app.get("/add/")
def add_pizza():
    return render_template("add.html")

@app.post('/add/')
def add_post_pizza():
    print('add')

    name = request.form["name"]
    description = request.form["description"]
    connection = sqlite3.connect('pizza.db')

    if not name or not description:
        flash("Title or Content are not exist")
        return render_template("add.html")

    connection.execute("INSERT INTO pizzas"
                       "(name,description)"
                       "VALUES"
                       "(?,?)", (name, description,))
    connection.commit()
    connection.close()
    return redirect(url_for("main"))
@app.get("/<int:id>/edit")
def get_edit(id):
    pizza = get_pizza_po_id(id)
    return render_template("edit.html",pizza=pizza)
@app.post('/<int:id>/edit/')
def edit_pizza(id):
    print('fafsfs')
    pizza = get_pizza_po_id(id)
    name = request.form["name"]
    description = request.form["description"]
    connection = sqlite3.connect('pizza.db')

    if not name or not description:
        flash("Title or Content are not exist")
        return render_template("edit.html",pizza=pizza)

    connection.execute("UPDATE pizzas SET name = ? , description = ? WHERE id = ?", (name, description,id,))
    connection.commit()
    connection.close()
    return redirect(url_for("main"))




@app.get("/pizzas/<int:id>/")
def get_pizza_id(id):
    pizza = get_pizza_po_id(id)
    return render_template("pizza.html",pizza=pizza)

def get_pizza_po_id(id):
    conection = sqlite3.connect('pizza.db')
    pizza = conection.execute("SELECT * FROM pizzas WHERE id=?", (id,)).fetchone()
    conection.close()

    return pizza


@app.post("/<int:id>/delete/")
def delete_pizza(id):
    conection = sqlite3.connect('pizza.db')
    conection.execute("DELETE FROM pizzas WHERE id=?", (id,))
    conection.commit()
    conection.close()
    return redirect(url_for("main"))

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