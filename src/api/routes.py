"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.models import db, Users, Posts
import requests

api = Blueprint('api', __name__)
CORS(api)  


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {}
    response_body['message'] = "Hello! I'm a message that came from the backend"
    return response_body, 200


@api.route('/users', methods=['GET'])
def users():
    response_body = {}
    if request.method == 'GET':
        rows = db.session.execute(db.select(Users)).scalars()
        result = [ row.serialize() for row in rows ]
        response_body['message'] = 'Listado de Usuarios'
        response_body['results'] = result
        return response_body, 200



@api.route('/posts', methods=['GET', 'POST'])
def posts():
    response_body = {}
    if request.method == 'GET':
        rows = db.session.execute(db.select(Posts)).scalars()

        result = [ row.serialize() for row in rows ]
        response_body['message'] = f'Listado de todas las publicaciones (de todos los usuarios)'
        response_body['results'] = result
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        row = Posts(title=data.get('title'),
                    description=data.get('description'),
                    body=data.get('body', 'body por defecto cuando hay un error'),
                    image_url=data['image_url'],
                    user_id=data['user_id'])
        db.session.add(row)
        db.session.commit()
        response_body['message'] = f'El post ha sido publicado correctamente'
        response_body['results'] = row.serialize()
        return response_body, 200


@api.route('/posts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def post(id):
    response_body = {}
    row = db.session.execute(db.select(Posts).where(Posts.id == id)).scalar()
    
    if not row:
        response_body['message'] =  f'La publicación con id: {id} no existe en nuestro registos'
        return response_body, 400
    if request.method == 'GET':
        response_body['results'] = row.serialize()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        return response_body, 200
    if request.method == 'PUT':
        data = request.json
        row.title = data['title']
        row.description = data['description']
        row.body = data['body']
        row.image_url = data['image_url']
        row.user_id = data['user_id']
        db.session.commit()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        response_body['results'] = row.serialize()
        return response_body, 200
    if request.method == 'DELETE':
        db.session.delete(row)
        db.session.commit()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        return response_body, 200


@api.route('/users/<int:user_id>/posts', methods=['GET'])
def users_posts(user_id):
    response_body = {}
   
    response_body['message'] = 'todos las publicaciones de un usuario'
    return response_body, 200


@api.route('/posts/<int:post_id>/comments', methods=['GET'])
def post_comments(post_id):
    response_body = {}

    response_body['message'] = 'todos los comenarios de una publicación'
    return response_body, 200


@api.route('/users/<int:user_id>/comments', methods=['GET'])
def user_comments():
    response_body = {}
    response_body['message'] = 'todos los comenarios de una usuario'
    return response_body, 200


@api.route('/jph-users', methods=['GET'])
def jph_users():
    response_body = {}
    url = 'https://jsonplaceholder.typicode.com/users'
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        response_body['results'] = data
        return response_body, 200
    response_body['message'] = 'Algún error'
    return response_body, 400


@api.route('/temp')
def temp():
    response_body = {}
    url = 'https://swapi.tech/api/people/'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        response_body['results'] = data
        return response_body, 200