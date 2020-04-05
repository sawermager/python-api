from flask import Flask, jsonify, request, Response

"""
The name of the package is used to resolve resources from inside the
package or the folder the module is contained in depending on if the
package parameter resolves to an actual python package (a folder with
an :file:`__init__.py` file inside) or a standard module (just a ``.py`` file).
"""
APP = Flask(__name__)

books = [
    { 
     'name': 'Green Eggs and Ham',
     'price': 7.99,
     'isbn': 12345678
     },
    { 
     'name': 'Cat in the Hat',
     'price': 6.99,
     'isbn': 87654321
     }
]

# Check if valid add_book response
def validBookObject(bookObject):
    return ("name" in bookObject and
            "price" in bookObject and
            "isbn" in bookObject)

# Default route action is GET
@APP.route('/books')
def get_books():
    return jsonify({'books': books})

# POST method
@APP.route('/books', methods=['POST'])
def add_book():
    req = request.get_json()
    if validBookObject(req):
        booktmp = {
            'name': req['name'],
            'price': req['price'],
            'isbn': req['isbn']
        }
        books.append(req)
        # See https://www.flaskapi.org/api-guide/status-codes/ for flask API
        # response codes
        response = Response("", 201, mimetype='application/json')

        # Set Header info for location (location of endpoint in request)
        response.headers['Location'] = "/books/"+str(booktmp['isbn'])
        return response
    # Returning a string to a flask API response request gives
    # code of 200 and mimetype=html by default.
    return "False"


# GET by book dictionary entry by isbn
@APP.route('/books/<int:isbn>') 
def get_book_by_isbn(isbn):
    return jsonify([book for book in books if book["isbn"] == isbn])
    

APP.run(port=5000)
