from Flask_app import app
from flask import render_template, session, redirect
from flask import flash


from Flask_app.models.pizzaorder import PizzaOrder
from Flask_app.models.user import User
from Flask_app.controllers import users, orders

@app.route('/')
def index():
    return 'Hello World!'


@app.route('/login')
def login_page():
    return render_template('regis_login_page.html')


@app.route('/home')
def home():
    if not session.get("user_id"):
        flash("You must be logged in to access the page.")
        return redirect('/login')
    else:
        return render_template('home_page.html')


if __name__=="__main__":
    app.run(debug=True, host="localhost", port=8080)