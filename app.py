import os
from flask_cors import CORS
import json
from flask import Flask, render_template, request, Response, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import backref
from models import setup_db, db, Drink, Donut, Combo
from auth.auth import AuthError, requires_auth
from sqlalchemy.exc import SQLAlchemyError


def create_app(test_config=None):
    ENV = 'prod'
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app)
    migrate = Migrate(app, db)

    @app.after_request
    def after_request(response):
        response.headers.add
        ('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add
        ('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE')
        return response

    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/menu', methods=['GET'])
    @requires_auth('get:menu')
    def get_menu(token):

        drinks = Drink.query.all()
        if len(drinks) == 0:
            drinks_list = {}
        else:
            drinks_list = []
            for drink in drinks:
                drinks_list.append({
                    "id": drink.id,
                    "title": drink.title,
                })
       
        donuts = Donut.query.all()
        if len(donuts) == 0:
            donuts_list = {}
        else:
            donuts_list = []
            for donut in donuts:
                donuts_list.append({
                        "id": donut.id,
                        "title": donut.title,
                    })
       

        combos = Combo.query.all()
        if len(combos) == 0:
            combos_list = {}
        else:
            combos_list = []
            for combo in combos:
                combos_list.append({
                    "drink_id": combo.drink_id,
                    "donut_id": combo.donut_id,
                })

        return jsonify({
            'drinks_list': drinks_list,
            'donuts_list': donuts_list,
            'combos_list': combos_list,
            'status': 200,
            'success': True,
        })

    @app.route('/combo', methods=['GET'])
    @requires_auth('get:combo')
    def get_combos(token):
        combos = Combo.query.all()

        if len(combos) == 0:
            return jsonify({
                'message': "There is no combos..",
                'status': 200,
                'success': True,
            })

        return jsonify({
            'combos_list': json.dumps(combos),
            'status': 200,
            'success': True,
        })

    @app.route('/drink', methods=['POST'])
    @requires_auth('post:drink')
    def add_drink(token):
        body = request.get_json()
        drink_title = body.get('drink_title', None)
        if drink_title is None:
            abort(422)
        try:
            drink = Drink(title=drink_title)
            drink.insert()
            return jsonify({
                'status': 200,
                'success': True,
            })
        except:
            abort(422)
    
    @app.route('/donut', methods=['POST'])
    @requires_auth('post:donut')
    def add_donut(token):
        body = request.get_json()
        donut_title = body.get('donut_title', None)
        if donut_title is None:
            abort(422)
        try:
            donut = Donut(title=donut_title)
            donut.insert()
            return jsonify({
                'status': 200,
                'success': True,
            })
        except:
            abort(422)
    
    
    @app.route('/combo', methods=['POST'])
    @requires_auth('post:combo')
    def add_combo(token):
        body = request.get_json()
        drink_id = body.get('drink_id', None)
        donut_id = body.get('donut_id', None)
        if drink_id is None or donut_id is None: 
            abort(422)
        try:
            combo = Combo(drink_id=drink_id, donut_id=donut_id)
            combo.insert()
            return jsonify({
                'status': 200,
                'success': True,
            })
        except:
            abort(422)


    @app.route('/combo/<int:combo_id>', methods=['PATCH'])
    @requires_auth('patch:combo')
    def update_combo(token, combo_id):
        combo = Combo.query.filter(
            Combo.id == combo_id).one_or_none()
        if combo is None:
            abort(422)
        body = request.get_json()

        try:
            if 'drink_id' in body:
                combo.drink_id = body.get('drink_id')
            if 'donut_id' in body:
                combo.donut_id = body.get('donut_id')
            combo.update()
            return jsonify({
                'status': 200,
                'success': True
            })
        except:
            abort(422)

    @app.route('/combo/<int:combo_id>', methods=['DELETE'])
    @requires_auth('delete:combo')
    def delete_combo(token, combo_id):
        combo = Combo.query.filter(
            Combo.id == combo_id).one_or_none()
        if combo is None:
            abort(404)

        try:
            combo.delete()
            return jsonify({
                'status': 200,
                'success': True,
            })
        except:
            abort(422)

    '''
    Error Handling
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(exciption):
        response = jsonify(exciption.error)
        response.status_code = exciption.status_code
        return response
    print(__name__, flush=True)
    if __name__ == '__main__':
        if ENV == 'dev':
            app.run(host='127.0.0.1', port=5000, debug=True)
        else:
            app.run(debug=False)

    return app
