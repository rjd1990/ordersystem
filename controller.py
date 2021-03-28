#!flask/bin/python
from flask import Flask, jsonify, request, abort, make_response, json
import os, sqlite3
from order import*
from lineItem import*
from productDisplay import*
import itertools
import datetime

app = Flask(__name__)

# this endpoint is used to return all orders for a customer sorted by date

@app.route('/ordersystem/api/v1.0/orders/<int:customer_id>', methods=['GET']) 
def get_all_orders(customer_id):
    DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'shopDatabase.sqlite3')
    orders_display = []
    with(sqlite3.connect(DEFAULT_PATH, timeout=10)) as con:
        orders = displayOrders(con, customer_id)
        for order in orders:
            orderJSON = {
                'id': order.id,
                'status': order.status,
                'dateCreated': order.dateCreated,
                'customerID': order.customerID
            }
            orders_display.append(orderJSON)
        return json.dumps({'orders': orders_display})

# this endpoint is used to return a breakdown of products sold by quantity

@app.route('/ordersystem/api/v1.0/search', methods=['GET'])
def get_order_by_choice():
    DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'shopDatabase.sqlite3')
    products_and_amounts = []
    productDisplayObjects = []
    with(sqlite3.connect(DEFAULT_PATH, timeout=10)) as con:
        rangeStart = request.json['rangeStart'] 
        rangeEnd = request.json['rangeEnd']
        date = request.json['date']
        choice = request.json['choice']
        # get all orders that fall into range
        orders_by_choice = getOrdersByCriteria(con, rangeStart, rangeEnd, date, choice)
        for order in orders_by_choice:
            # get each line item which details quantites (amounts) and product ids
            products_and_amounts.append(getLineItems(con, order.id))
        paDict = {}
        products_and_amounts = list((itertools.chain.from_iterable(products_and_amounts)))
        # Use a dictionary with key product id, value summed quantity
        for element in products_and_amounts:
            if element[0] in paDict:
                paDict[element[0]] += element[1]
            else:
                paDict[element[0]] = element[1]   
        # get product name and categories it belongs to for each productID
        for key, value in paDict.items():
            productAndCategoriesInfo = getProductInfoAndCategories(con, key)
            pdisplay = ProductDisplay(key, productAndCategoriesInfo[0][0][1], value, productAndCategoriesInfo[1])
            forJSON = {
                'id': pdisplay.id,
                'name': pdisplay.name,
                'quantity': pdisplay.quantity,
                'categories': list((itertools.chain.from_iterable(pdisplay.categories)))
            }
            productDisplayObjects.append(forJSON)

        return json.dumps({'products': productDisplayObjects})



# this endpoint is to update an order's status

@app.route('/ordersystem/api/v1.0/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id): 
    DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'shopDatabase.sqlite3')
    with(sqlite3.connect(DEFAULT_PATH, timeout=10)) as con:
        if (orderExists(con, str(order_id)) == False):
            abort(404)
        else: 
            newStatus = request.json['status']
            updateStatus(con, newStatus, str(order_id))
            con.commit()
            updatedOrder = selectOrder(con, str(order_id))
            return jsonify({'new order id': updatedOrder})

# this endpoint is used to delete an order

@app.route('/ordersystem/api/v1.0/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'shopDatabase.sqlite3')
    with(sqlite3.connect(DEFAULT_PATH, timeout=10)) as con:
        if (orderExists(con, str(order_id)) == False):
            abort(404) # not found
        else: 
            deleteOrder(con, order_id)
            con.commit()
            return jsonify({'delete': "successful"})

# this endpoint is used to add a new order 

@app.route('/ordersystem/api/v1.0/orders', methods=['POST']) 
def create_order():
    DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'shopDatabase.sqlite3')
    with(sqlite3.connect(DEFAULT_PATH, timeout=10)) as con:
        insertOrder(con, request.json['customer'], request.json['status'], request.json['products'])
        return jsonify({'insertOrder': "successful"})

def insertOrder(con, customerID, status, productsList):
    cur = con.cursor()
    dateCreated = datetime.datetime.now()
    order_sql = "INSERT INTO orders (id, customer_id, status, dateCreated) VALUES (?, ?, ?, ?)";
    cur.execute(order_sql, (None, customerID, status, dateCreated))
    orderID = getLastOrderAdded(con)
    for product in productsList:
        insertLineItem(con, product[0], product[1], orderID)
    con.commit()

def insertLineItem(con, product_id, amount, order_id): 
    cur = con.cursor()
    line_sql = """INSERT INTO line_items VALUES (?, ?, ?, ?)""";
    cur.execute(line_sql, (None, amount, product_id, order_id))
    
def displayOrders(con, customerID):
    cur = con.cursor()
    order_sql = "SELECT* from ORDERS WHERE CUSTOMER_ID = ? ORDER BY dateCreated DESC";
    cur.execute(order_sql, str(customerID))
    orderRows = cur.fetchall()
    orderObjects = []
    for order in orderRows:
        orderObject = Order(order[0], order[1], order[2], order[3])
        orderObjects.append(orderObject)

    return orderObjects

def getOrdersByCriteria(con, rangeStart, rangeEnd, date, choice):
    cur = con.cursor()
    # search by day of the year, week of the year, or month of the year
    day_sql = "SELECT * from orders WHERE STRFTIME('%j', dateCreated) = ? AND dateCreated > ? AND dateCreated < ?"
    week_sql = "SELECT * from orders WHERE STRFTIME('%W', dateCreated) = ? AND dateCreated > ? AND dateCreated < ?"
    month_sql = "SELECT * from orders WHERE STRFTIME('%m', dateCreated) = ? AND dateCreated > ? AND dateCreated < ?"
    
    if (choice == 'day'):
        cur.execute(day_sql, (date, rangeStart, rangeEnd))
    elif (choice == 'week'):
        cur.execute(week_sql, (date, rangeStart, rangeEnd))
    else: 
        cur.execute(month_sql, (date, rangeStart, rangeEnd))
    orderRows = cur.fetchall()
    orders_by_choice = []
    for order in orderRows:
        order_by_choice = Order(order[0], order[1], order[2], order[3])
        orders_by_choice.append(order_by_choice)
    return orders_by_choice


def selectOrder(con, order):
    cur = con.cursor()
    order_sql = """SELECT * from orders where id = ?"""
    cur.execute(order_sql, (order))
    order = cur.fetchall()
    return order[0][0]

def orderExists(con, id):
    cur = con.cursor()
    order_sql = "SELECT * FROM ORDERS WHERE ID = ?";
    cur.execute(order_sql, (id))
    id = cur.fetchall()
    if id == []:
        return False
    else:
        return True

def updateStatus(con, status, id):
     cur = con.cursor()
     status_sql = """UPDATE ORDERS SET STATUS = ? WHERE ID = ?"""
     cur.execute(status_sql, (status, id))

def deleteOrder(con, id):
    cur = con.cursor()
    delete_sql = """DELETE FROM ORDERS WHERE ID = ?"""
    cur.execute(delete_sql, str(id))

def getLastOrderAdded(con):
    cur = con.cursor()
    order_sql = "SELECT id from ORDERS where ID = (SELECT MAX(ID) FROM ORDERS)"
    cur.execute(order_sql)
    id = cur.fetchall()
    return id[0][0]

def getLineItems(con, orderID):
    cur = con.cursor()
    lineitems_sql = """SELECT PRODUCT_ID, AMOUNT FROM LINE_ITEMS WHERE ORDER_ID = ?"""
    cur.execute(lineitems_sql, str(orderID))
    lineItemRows = cur.fetchall()
    listOfProductsAndAmounts = []
    for line in lineItemRows:
        listOfProductsAndAmounts.append((line[0], line[1]))
    return listOfProductsAndAmounts


def getProductInfoAndCategories(con, id):
    cur = con.cursor()
    prodCat_sql = "SELECT * FROM PRODUCTS WHERE ID = ?"
    productInfo = []
    categories = []
    cur.execute(prodCat_sql,str(id))
    productInfo = cur.fetchall()
    # get categories of products for display
    cat_sql = "SELECT NAME FROM CATEGORIES WHERE ID IN (SELECT CATEGORY_ID FROM PRODUCTS_CATEGORIES WHERE PRODUCT_ID = ? )"
    cur.execute(cat_sql, str(id))
    categories = cur.fetchall()
    return (productInfo, categories)


if __name__ == '__main__':

    app.run(debug=True)
