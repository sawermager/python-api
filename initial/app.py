"""Flask REST API"""

"""This is server app. Client used was Postman"""
import json
import jwt
import datetime
from flask import Flask, jsonify, request, Response
from settings import *
from BookModel import *
from usermodel import User
from functools import wraps

app.config['SECRET_KEY'] = 'scott'

def validBookObject(bookObject):
    """Check if valid add_book response"""
    return ("name" in bookObject and
            "price" in bookObject and
            "isbn" in bookObject)

def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return fn(*args, **kwargs)
        except:
            return jsonify({'error': "Need valid token"}), 401
    return wrapper
    
@app.route('/login', methods=['POST'])
def get_token():
    """Get jwt encoded token"""
    req = request.get_json()
    username = str(req['username'])
    password = str(req['password'])
    if User.username_password_match(username, password):
        expiration_date = datetime.datetime.utcnow() + \
            datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    return Response('', 401, mimetype='application/json')

@app.route('/books')
def get_books():
    """GET - Default route action"""
    return jsonify({'books': Book.get_all_books()})

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    """GET request by book dictionary entry by isbn"""
    return Book.get_book(isbn)
 
@app.route('/books', methods=['POST'])
@token_required
def add_book():
    """POST request"""
    req = request.get_json()
    if validBookObject(req):
        booktmp = {
            'name': req['name'],
            'price': req['price'],
            'isbn': req['isbn']
        }
        Book.add_book(req['name'], req['price'], req['isbn'])

        # See https://www.flaskapi.org/api-guide/status-codes/ for flask API
        # response codes
        response = Response("", 201, mimetype='application/json')

        # Set Header info for location (location of endpoint in request)
        response.headers['Location'] = "/books/"+str(req['isbn'])
        return response

    # Returning a string to a flask API response request gives
    # code of 200 and mimetype=html by default.
    # Create helpful response instead of default.
    invalid_book_object_error_msg = {
        "error": "Invalid book object passed in POST request",
        "helpString": "Valid data format is {'name': 'bookname', 'price': 7.9, 'isbn': 12345678}"
    }
    # Because invalidBookObjectErrorMsg is a dictionary, need to convert it into a json object.
    return Response(json.dumps(invalid_book_object_error_msg), status=400, mimetype='application/json')

@app.route('/books/<int:isbn>', methods=['PUT'])
@token_required
def update_book(isbn):
    """ PUT request to replace/update existing entries"""
    put_req = request.get_json()
    if not (Book.replace_book(isbn, put_req['name'], put_req['price'])):
        invalid_book_object_error_msg = {
            "error": "Invalid book object update passed in PUT request",
            "helpString": "Valid data format is {'name': 'bookname', 'price': 7.9, 'isbn': 12345678}"
        }
        # Because invalidBookObjectErrorMsg is a dictionary, need to convert it into a json object.
        # Set Header info for location (location of endpoint in request)
        return Response(json.dumps(invalid_book_object_error_msg), status=406, mimetype='application/json')
    # See https://www.flaskapi.org/api-guide/status-codes/ for flask API
    # response codes
    response = Response("", 204, mimetype='application/json')
    response.headers['Location'] = "/books/" + str(isbn)
    return response

@app.route('/books/<int:isbn>', methods=['PATCH'])
@token_required
def update_with_patch_method_book(isbn):
    """PATCH request"""
    return update_book(isbn)

@app.route('/books/<int:isbn>', methods=['DELETE'])
@token_required
def delete_book(isbn):
    """DELETE request"""
    if (Book.delete_book(isbn)):
        return Response("", status=204)
    invalid_book_isbn = {
        "error": "Invalid book isbn passed in DELETE request",
        "helpString": "Valid data format is http://<IP>:<port>/books/isbn"
    }
    # Because invalid_book_isbn is a dictionary, need to convert it into a json object.
    # Set Header info for location (location of endpoint in request)
    return Response(json.dumps(invalid_book_isbn), status=404, mimetype='application/json')
    
app.run(port=5000)
