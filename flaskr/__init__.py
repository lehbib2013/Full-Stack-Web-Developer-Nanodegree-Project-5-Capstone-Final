import os
import sys
import json
import dateutil.parser
import babel
import secrets
from werkzeug.exceptions import HTTPException
from flask_cors import CORS, cross_origin
from flask import (
  Flask,
  request,
  abort,
  jsonify,
  render_template,
  flash,
  session,
  Response,
  make_response
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import null
from sqlalchemy import or_
from .auth.auth import AuthError, requires_auth
import requests
from jose import jwt

from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException
import traceback
from dotenv import load_dotenv, find_dotenv
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from flask import redirect
from models import CaptainPaymentCashierTransaction, \
  ConsumableCashierTransaction, GeneralCashierTransaction, \
  SalaryCashierTransaction, SpartPartCashierTransaction, setup_db, Supplier, \
  Captain, Cashier, CashierJournal, CashierTransaction, InvoiceSupplier, \
  FishingTied, SupplyCashierTransaction, OrdinaryCashierTransaction, \
  SupplierCashierTransaction, AvanceCashierTransaction, Capture, Specie, \
  YieldDistributionPolicy, PricingSpecie, DetailsPricingSpecie, \
  TransactionType,  RequestError

from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flaskr.b_captains.blueprint_captains import captain_blueprint
from flaskr.b_others.blueprint_captures import captures_blueprint
from flaskr.b_others.blueprint_cashiers import cashier_blueprint
from flaskr.b_others.blueprint_detailspricings import detailspricing_blueprint
from flaskr.b_others.blueprint_invoices import invoices_blueprint
from flaskr.b_others.blueprint_journals import journals_blueprint
from flaskr.b_others.blueprint_policies import policies_blueprint
from flaskr.b_others.blueprint_pricings import pricings_blueprint
from flaskr.b_others.blueprint_species import species_blueprint
from flaskr.b_others.blueprint_suppliers import supplier_blueprint
from flaskr.b_others.blueprint_tieds import tieds_blueprint
from flaskr.b_others.blueprint_transactions import transactions_blueprint


def format_datetime(value, formatt='medium'):
    date = dateutil.parser.parse(value)
    if formatt == 'full':
        formatt = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        formatt = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, formatt, locale='en')


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, static_url_path='/static', static_folder='./static')
    setup_db(app)
    app.secret_key = 'thisIsSecrteKey'
    oauth = OAuth(app)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.register_blueprint(captain_blueprint)
    app.register_blueprint(captures_blueprint)
    app.register_blueprint(cashier_blueprint)
    app.register_blueprint(detailspricing_blueprint)
    app.register_blueprint(invoices_blueprint)
    app.register_blueprint(journals_blueprint)
    app.register_blueprint(policies_blueprint)
    app.register_blueprint(pricings_blueprint)
    app.register_blueprint(species_blueprint)
    app.register_blueprint(supplier_blueprint)
    app.register_blueprint(tieds_blueprint)
    app.register_blueprint(transactions_blueprint)
    app.debug = True
    auth0 = oauth.register(
        'auth0',
        client_id='xRUm9KcctNSUOTPZd4sKJvjeLj3uhJKf',
        client_secret='2EO3RqHIaz69Pagm1euUpxinrVVD84HnCb2uW__ywIPvfG_DgOULt7\
          gZce2lIQi4',
        api_base_url='https://dev-llz9tf-n.us.auth0.com',
        access_token_url='https://dev-llz9tf-n.us.auth0.com/oauth/token',
        authorize_url='https://dev-llz9tf-n.us.auth0.com/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )

    @app.route('/')
    @cross_origin()
    def welcome():
        return render_template('pages/home.html'), 200

    @app.route('/login', methods=['GET'])
    def login():
        try:
            return auth0.authorize_redirect(redirect_uri='https://127.0.0.1:\
                   5000/login-result', audience='mycapstone')
        except Exception as e:
            print('Error while doing something:', e)
            traceback.print_exc()

    @app.route('/login-result')
    def post_login():
        print("testttttt")
        try:
            # Handles response from token endpoint
            auth0.authorize_access_token()
            resp = auth0.get('userinfo')
            userinfo = resp.json()
            print("userinfo")
            print(userinfo)
            print("userinfo")

            session['jwt_payload'] = userinfo
            session['profile'] = {
                                              'user_id': userinfo['sub'],
                                              'name': userinfo['name'],
                                              'picture': userinfo['picture']
                                              }
            return redirect('/captains')
        except Exception as e:
            print('Error while doing something:', e)
            traceback.print_exc()

    @app.route('/logout')
    def logout():
        session.clear()
        params = {'returnTo': url_for('home', _external=True),
                  'client_id': 'xRUm9KcctNSUOTPZd4sKJvjeLj3uhJKf'}
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

    '''
    decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,\
          Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,PATCH,\
          POST,DELETE,OPTIONS")
        return response

    '''
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found_hand(error):
        return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessoblle_handler(error):
        return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable error"
        }), 422

    @app.errorhandler(400)
    def bad_request400_handler(error):
        return jsonify({
          'success': False,
          'error': 400,
          'message': 'Bad request'
        }), 400

    @app.errorhandler(405)
    def bad_request405_handler(error):
        return jsonify({
          'success': False,
          'error': 405,
          'message': 'Method not allowed'
        }), 405

    @app.errorhandler(500)
    def bad_request500_handler(error):
        return jsonify({
          'success': False,
          'error': 500,
          'message': 'Internal server error'
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response
    
    @app.errorhandler(Exception)
    def handle_auth_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code if isinstance(ex, HTTPException)
                                else 500)
        return response

    return app


app = create_app()
if __name__ == '__main__':
    # Set the secret key to some random bytes. Keep this really secret!
    app.run()
