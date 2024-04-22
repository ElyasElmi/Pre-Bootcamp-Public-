from flask import render_template, redirect, request, session, flash
from Flask_app import app
from Flask_app.models.pizzaorder import PizzaOrder
from Flask_app.models.user import User


# Render templates
@app.route('/orders/new')
def order_creation():
    if not session.get("user_id"):
        flash("You must be logged in to access the dashboard.")
        return redirect('/')
    return render_template('neworder_page.html')


@app.route('/orders/<int:id>/checkout')
def order_checkout(id):
    if not session.get("user_id"):
        flash("You must be logged in to access the dashboard.")
        return redirect('/')
    return render_template('checkout_page.html', order=PizzaOrder.get_one({'id':id}))
# @app.route('/magazines/edit/<int:magazine_id>')
# def update_magazine(magazine_id):
#     print("in edit page: ", magazine_id)
#     if not session.get("user_id"):
#         flash("You must be logged in to access the dashboard.")
#         return redirect('/')
#     data = {
#         "id": magazine_id
#     }
#     return render_template('edit_page.html', magazine=Order.get_one(data))
#
# @app.route('/magazine/details/<int:magazine_id>')
# def magazine_details(magazine_id):
#     if not session.get("user_id"):
#         flash("You must be logged in to access the dashboard.")
#         return redirect('/')
#     print("in details:" , magazine_id)
#     user_data = {
#         "id": session.get("user_id")
#     }
#     magazine_data = {
#         "id": magazine_id
#     }
#     return render_template('details_page.html', user=User.get_one(user_data), magazine=Order.get_one(magazine_data))


# @app.route('/orders/<int:id>/edit', methods=['POST'])
# def edit_magazine(id):
#     if not session.get("user_id"):
#         flash("You must be logged in to access the dashboard.")
#         return redirect('/')
#     print(request.form)
#     data = {
#         "id": id,
#         "title": request.form['title'],
#         "description": request.form['description'],
#     }
#     Order.update(data)
#     return redirect('/home')


##
@app.route('/orders', methods=['POST'])
def create_order():
    print(request.form)
    data = {
        "method": request.form['method'],
        "size": request.form['size'],
        "crust": request.form['crust'],
        "quantity": request.form['quantity'],
        "sauces": request.form['sauces'],
        "cheese": request.form['cheese'],
        "meat": request.form['meat'],
        "vegetables": request.form['vegetable'],
        "desert_name": request.form['desert_name'],
        "desert_quantity": request.form['desert_quantity'],
        "drink_name": request.form['drink_name'],
        "drink_size": request.form['drink_size'],
        "drink_quantity": request.form['drink_quantity'],
        "user_id": session.get("user_id")
    }
    id = PizzaOrder.save(data)
    return redirect("/orders/"+str(id)+"/checkout")


@app.route('/orders/<int:id>/purchase', methods=['POST'])
def purchase_order(id):
    if not session.get("user_id"):
        flash("You must be logged in to access the dashboard.")
        return redirect('/home')
    data = {"id": id}
    PizzaOrder.purchase(data)
    return redirect('/home')


@app.route('/orders/<int:id>/cancel', methods=['POST'])
def cancel_order(id):
    if not session.get("user_id"):
        flash("You must be logged in to access the dashboard.")
        return redirect('/home')
    data = {"id": id}
    PizzaOrder.cancel(data)
    return redirect('/home')


@app.route('/orders/<int:id>/delete', methods=['POST'])
def delete_order(id):
    if not session.get("user_id"):
        flash("You must be logged in to access the dashboard.")
        return redirect('/home')
    data = {"id": id}
    PizzaOrder.destroy(data)
    return redirect('/home')


if __name__ == "__main__":
    app.run(debug=True)
