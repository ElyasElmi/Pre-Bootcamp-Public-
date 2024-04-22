from Flask_app import app
from flask import session, render_template, redirect, request, flash
from Flask_app.models.user import User
from Flask_app.models.pizzaorder import PizzaOrder
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/user/account')
def account():
    if not session.get("user_id"):
        flash("You must be logged in to access the dashboard.")
        return redirect('/')
    id = session.get("user_id")
    return render_template('account_page.html', user=User.get_one({'id':id}), orders=PizzaOrder.get_all({'user_id':id}))


@app.route('/users', methods=['POST'])
def create():
    print(request.form)
    pw_hash = bcrypt.generate_password_hash(request.form['password'].encode('utf-8'))
    print(pw_hash)
    if not bcrypt.check_password_hash(pw_hash, request.form['confirm_password']):
        flash("passwords do not match")
        return redirect("/login")
    else:
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "address": request.form['address'],
            "city": request.form['city'],
            "state": request.form['state'],
            "password": pw_hash
        }
        user_id = User.save(data)
        start_session(user_id)

        return redirect("/home")


@app.route('/users/<int:id>/update', methods=['POST'])
def update_user():
    if 'user_id' not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect('/')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    address = request.form.get('address')
    city = request.form.get('city')
    state = request.form.get('state')
    user_id = session['user_id']
    existing_user = User.get_by_email(email)
    if existing_user and existing_user.id != user_id:
        flash("Email is already in use.")
        return redirect('/home')
    data = {
        "id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "address": address,
        "city": city,
        "state": state,
    }
    User.update(data)
    session['first_name'] = first_name
    return redirect('/home')


@app.route('/users/login', methods=['POST'])
def login():
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/login")
    pw_hash = bcrypt.generate_password_hash(request.form['password'].encode('utf-8'))
    print(pw_hash)
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/login')
    start_session(user_in_db.id)
    return redirect("/home")


@app.route('/user/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect("/login")


def start_session(id):
    session['user_id'] = id
