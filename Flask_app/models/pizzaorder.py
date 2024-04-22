from Flask_app.config.mysqlconnect import connectToMySQL
from flask import flash

DB_SCHEMA = 'northwest_pizza_schema'
STATUS_PENDING = 'Pending'
STATUS_PURCHASED = 'Complete'
STATUS_CANCELED = 'Cancelled'


class PizzaOrder:
    def __init__(self, data):
        self.id = data['id']
        self.method = data['method']
        self.size = data['size']
        self.crust = data['crust']
        self.quantity = data['quantity']
        self.sauces = data['sauces']
        self.cheese = data['cheese']
        self.toppings = data['toppings']
        self.deserts = data['deserts']
        self.drinks = data['drinks']
        self.price = data['price']
        self.status = data['status']
        self.created_at = data['created_at']

    @staticmethod
    def size_price(size):
        if size == 'Large':
            return 9.99
        elif size == 'Medium':
            return 7.99
        elif size == 'Small':
            return 5.99
        return 0.00

    @staticmethod
    def crust_price(crust):
        if crust == 'Italy Style':
            return 5.50
        elif crust == 'New York Style':
            return 4.50
        elif crust == 'Hand Tossed':
            return 3.50
        return 0.00

    @staticmethod
    def sauces_price(sauce):
        if sauce == 'Marinara' or sauce == 'BBQ':
            return 6.00
        elif sauce == 'Alfredo' or sauce == 'Garlic Parmesan':
            return 4.50
        elif sauce == 'Tomato':
            return 2.50
        return 0.00

    @staticmethod
    def cheese_price(cheese):
        if cheese == 'Normal':
            return 3.00
        elif cheese == 'Extra' or cheese == 'Light':
            return 3.50
        elif cheese == 'Half':
            return 2.00
        return 0.00

    @staticmethod
    def meat_price(meat):
        if meat == 'Chicken' or meat == 'Sausage':
            return 4.50
        elif meat == 'Ham' or meat == 'Salami':
            return 5.50
        elif meat == 'Bacon':
            return 6.00
        elif meat == 'Beef':
            return 5.00
        return 0.00

    @staticmethod
    def vegetable_price(vegetable):
        if vegetable == 'Onions' or vegetable == 'Olives' or vegetable == 'Spinach':
            return 3.00
        if vegetable == 'Tomatoes' or vegetable == 'Pineapple' or vegetable == 'Mushrooms':
            return 2.50
        if vegetable == 'Green Peppers' or vegetable == 'Jalapeno Peppers':
            return 2.99
        return 0.00

    @staticmethod
    def deserts_price(desert_name, desert_quantity):
        desert_price = 0.00
        if desert_name == 'Cinnamon Rolls':
            desert_price.__add__(3.00)
        elif desert_name == 'Chocolate Chip Cookies':
            desert_price.__add__(2.50)
        elif desert_name == 'Chocolate Brownies':
            desert_price.__add__(2.00)

        return desert_price.__mul__(desert_quantity)

    @staticmethod
    def drinks_price(drink_name, drink_size, drink_quantity):
        drinks_price = 0.00
        if drink_name == 'Coke':
            if drink_size == '20oz':
                drinks_price.__add__(5.00)
            else:
                drinks_price.__add__(3.00)
            return drinks_price.__mul__(drink_quantity)
        return 0.00



    @classmethod
    def calculate_price(cls, order):
        price = 0.00
        price.__add__(PizzaOrder.size_price(order['size']))
        price.__add__(PizzaOrder.crust_price(order['crust']))
        price.__add__(PizzaOrder.sauces_price(order['sauces']))
        price.__add__(PizzaOrder.cheese_price(order['cheese']))
        price.__add__(PizzaOrder.meat_price(order['meat']))
        price.__add__(PizzaOrder.vegetable_price(order['vegetables']))
        price.__mul__(order['quantity'])

        price.__add__(PizzaOrder.deserts_price(order['desert_name'], order['desert_quantity']))
        price.__add__(PizzaOrder.drinks_price(order['drink_name'], order['drink_size'], order['drink_quantity']))

        return price

    @classmethod
    def format_toppings(cls, meat, vegetables):
        return meat + ", " + vegetables
    
    @classmethod
    def format_deserts(cls, name, quantity):
        return name + "(" + quantity + ")"

    @classmethod
    def format_drinks(cls, name, size, quantity):
        return name + "(" + size + ")" + "(" + quantity + ")"

    @classmethod
    def save(cls, data):
        data['price'] = PizzaOrder.calculate_price(data)
        data['formatted_toppings'] = PizzaOrder.format_toppings(data['meat'], data['vegetables'])
        data['formatted_deserts'] = PizzaOrder.format_deserts(data['desert_name'], data['desert_quantity'])
        data['formatted_drinks'] = PizzaOrder.format_drinks(data['drink_name'], data['drink_size'], data['drink_quantity'])
        data['status'] = STATUS_PENDING
        print(data)
        query = ("INSERT INTO PizzaOrder(method,size,crust,quantity,toppings,deserts,drinks,price,status,created_at,User_id)"
                 " VALUES (%(method)s,%(size)s,%(crust)s,%(quantity)s,%(formatted_toppings)s,%(formatted_deserts)s,%(formatted_drinks)s,%(price)s,%(status)s,NOW(),%(user_id)s);")
        result = connectToMySQL(DB_SCHEMA).query_db(query, data)
        return result
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM PizzaOrder WHERE id = %(id)s ;"
        result = connectToMySQL(DB_SCHEMA).query_db(query, data)
        return cls(result[0])

    @classmethod
    def pending_orders(cls, data):
        query = "SELECT * FROM PizzaOrder WHERE status = " + STATUS_PENDING + " LEFT JOIN User ON PizzaOrder.User_id=User.id;"
        result = connectToMySQL(DB_SCHEMA).query_db(query, data)
        if len(result) < 1:
            return True
        return False

    @classmethod
    def purchase(cls, data):
        query = "UPDATE PizzaOrder SET status=%(" + STATUS_PURCHASED + ")s WHERE id = %(id)s;"
        return connectToMySQL(DB_SCHEMA).query_db(query, data)

    @classmethod
    def cancel(cls, data):
        query = "UPDATE PizzaOrder SET status=%(" + STATUS_CANCELED + ")s WHERE id = %(id)s;"
        return connectToMySQL(DB_SCHEMA).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM PizzaOrder WHERE id = %(id)s;"
        return connectToMySQL(DB_SCHEMA).query_db(query, data)

    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM PizzaOrder LEFT JOIN User ON PizzaOrder.User_id=User.id WHERE user_id = %(user_id)s;"
        results = connectToMySQL(DB_SCHEMA).query_db(query, data)
        orders = []
        print(results)
        if not results.__sizeof__() == 0:
            for row_from_db in results:
                print(row_from_db)
                data = {
                    "id": row_from_db["id"],
                    "method": row_from_db["method"],
                    "size": row_from_db["size"],
                    "crust": row_from_db["crust"],
                    "quantity": row_from_db["quantity"],
                    "sauces": row_from_db["sauces"],
                    "cheese": row_from_db["cheese"],
                    "toppings": row_from_db["toppings"],
                    "deserts": row_from_db["deserts"],
                    "drinks": row_from_db["drinks"],
                    "price": row_from_db["price"],
                    "status": row_from_db["status"],
                    "created_at": row_from_db["created_at"],
                    "user_id": row_from_db["User.id"]
                }
                orders.append(data)
        return orders
    
    # @classmethod
    # def update(cls, data):
    #     query = "UPDATE Magazine SET title=%(title)s,network=%(description)s,updated_at=NOW() WHERE id = %(id)s;"
    #     return connectToMySQL(DB_SCHEMA).query_db(query, data)
