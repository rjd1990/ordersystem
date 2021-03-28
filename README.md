## Running the Code
  
*The results below will be slighty different since the database has been modified following these steps.

- I use Python 3.6.5, SQLite version 3.22.0, and Flask 1.1.1, on Mac.
- The controller.py is used to run flask, and I used curl to test the endpoints from a separate terminal window.
- The createDB.py was used to create the database (contains the schema), and has methods used below to display the db's current state
- There are model classes used to represent the database tables and present the data
- I have included the sqlite database file so that all previously created products, orders, customers can be viewed

To show the current state of the database, I go to the containing folder and type:

`python3` then `from createDB import*`
I create a connection to the db and cursor by typing
`con = createDB()`
`cur = con.cursor()`
I select all customers currently in the database with:
`displayCustomers(con)` which displays:
_[(1, 'rohit', 'deshane'), (2, 'alok', 'deshane')]_
`displayProducts(con)` displays:
_[(1, 'pizza', '$2.50'), (2, 'frozen pretzel', '$3.50')]_
`displayCategories(con)` which displays:
_[(1, 'frozen'), (2, 'Late Night')]_
`displayProductsCategories(con)`
_[(1, 1), (2, 2), (2, 1), (1, 2)]_
`displayOrders(con)`
_[(3, 'ready', '2019-12-11 08:24:35.163227', 1), (4, 'ready', '2019-12-11 08:25:17.820206', 1), (5, 'ready', '2019-12-12 09:32:46.278772', 1)]_
`displayLineItems(con, 3)`
_[(4, 2.4, 1, 3)]_

There are two customers, two products, two categories, and three orders currently in the system. The first element of each tuple in the returned lists are the primary key ids for that table. Pizza and Frozen Pretzels both belong to the "Frozen" and "Late Night" categories, and the "Frozen" and "Late Night" categories, contain them likewise. This is a many-to-many relationship and is incorporated using the `PRODUCTS_CATEGORIES` bridge table.

To test the api endpoints I close the connection in the current terminal window:
`con.close()` and then `exit()`
in another terminal window (two total) I navigate to the enclosing folder and type `python3 controller.py` which starts flask

# Testing Endpoints

##### Product Breakdown

In the second terminal window (where flask isn't running) I want to get the product breakdown of all items sold between `2018-11-10` and `2019-12-13` with `week` criteria being the 49th week of the year.
`curl -i -H "Content-Type: application/json" -X GET -d '{"rangeStart": "2018-11-10", "rangeEnd": "2019-12-13", "date": "49", "choice": "week"}' http://localhost:5000/ordersystem/api/v1.0/search`

If I want the same range, but search by month, this time all in December:

`curl -i -H "Content-Type: application/json" -X GET -d '{"rangeStart": "2018-11-10", "rangeEnd": "2019-12-13", "date": "12", "choice": "month"}' http://localhost:5000/ordersystem/api/v1.0/search`

both of the above return the same results

_{"products": [{"categories": ["frozen", "Late Night"], "id": 1, "name": "pizza", "quantity": 4.699999999999999}, {"categories": ["frozen", "Late Night"], "id": 2, "name": "frozen pretzel", "quantity": 6.3}]}_
