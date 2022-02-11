from flask import Blueprint
import os
import sys
import json
import dateutil.parser
import babel
from flask import (
  Flask,
  request,
  abort,
  jsonify
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import null
from sqlalchemy import or_
from flaskr.auth.auth import AuthError, requires_auth
from jose import jwt


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

cashier_blueprint = Blueprint('cashier_blueprint', __name__)

'''
            GET cashier, return paginated results for cashiers
              http:127.0.0.1/cashier
              This endpoint should return a list of cashiers
'''


@cashier_blueprint.route("/cashiers")
@requires_auth("get:everything")
def get_all_cahiers(jwt):
    print("test")
    try:
        current_page_suppliers = Cashier.query.all()
        formatted_page_response = [cap.format() for cap in
                                   current_page_suppliers]
        return jsonify({
                  'success': True,
                  'content': formatted_page_response,
                  'total': len(formatted_page_response)
              })
    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)

    except Exception as error:
        print(sys.exc_info())
        print(error)
        abort(422)


'''
  POST Cashier
  Create new Cashier by providing Body object with needed information:
    {
    "code_cashier":"Ahmed","name_cashier":"Bateau Ely",
    "last_solde_opening":"","last_solde_closing":"","state":"",
    "date_open":"","date_close":""
    }
'''


@cashier_blueprint.route("/cashiers", methods=['POST'])
@requires_auth("post:everything")
def cashier_post_request(jwt):
    body = request.get_json()
    try:
        code_cashier_text = body.get('code_cashier', None)
        name_cashier_text = body.get('name_cashier', None)
        last_solde_openi = body.get('last_solde_opening', None)
        last_solde_closi = body.get('last_solde_closing', None)
        state = body.get('state', None)
        date_open = body.get('date_open', None)
        date_close = body.get('date_close', None)
        print("date_close")
        print(date_close)
        if len(date_close) == 0:
            date_close = None

        if (state is not None) and (date_open is not None) and \
            (code_cashier_text is not None) and \
            (name_cashier_text is not None) and \
                (last_solde_openi is not None):
            if date_close is None:
                to_be_added = Cashier(code_cashier=code_cashier_text,
                                      name_cashier=name_cashier_text,
                                      last_solde_opening=last_solde_openi,
                                      last_solde_closing=last_solde_closi,
                                      state=state,  date_open=date_open,
                                      date_close=None)
            else:
                to_be_added = Cashier(code_cashier=code_cashier_text,
                                      name_cashier=name_cashier_text,
                                      last_solde_opening=last_solde_openi,
                                      last_solde_closing=last_solde_closi,
                                      state=state, date_open=date_open,
                                      date_close=date_close)
                to_be_added.insert()
                fetched_page = Cashier.query.paginate(1, per_page=20,
                                                      error_out=True,
                                                      max_per_page=20)
                formatted_page = [fetchp.format() for
                                  fetchp in fetched_page.items]
                return jsonify({
                              'success': True,
                              'created': to_be_added.id,
                              'cashiers': formatted_page,
                              'totalQuestions': fetched_page.pages
                          })
        else:
            raise RequestError(400)

    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)

    except Exception as error:
        print(sys.exc_info())
        print(error)


'''
          PATCH Cashier
          Create new Cashier by providing Body object with needed information:
            {"id":"1",
            "code_cashier":"Ahmed","name_cashier":"Bateau Ely",
            "last_solde_opening":"","last_solde_closing":"","state":"",
            "date_open":"","date_close":""
            }
'''


@cashier_blueprint.route("/cashiers", methods=['PATCH'])
@requires_auth("patch:everything")
def cashier_patch_request(jwt):
    body = request.get_json()
    try:
        id_text = body.get('id', 1)
        code_cashier_text = body.get('code_cashier', None)
        name_cashier_text = body.get('name_cashier', None)
        last_solde_opening = body.get('last_solde', None)
        last_solde_closing = body.get('last_solde', None)
        state_text = body.get('state', None)
        date_open_text = body.get('date_open', None)
        date_close_text = body.get('date_close', None)

        if (id_text is not None) and (state_text is not None) and\
            (date_open_text is not None) and (date_close_text is not None)\
            and (code_cashier_text is not None) and\
            (name_cashier_text is not None) and\
            (last_solde_opening is not None) and\
                (last_solde_closing):
            to_be_edit = Cashier.query.filter(Cashier.id ==
                                              id_text).one_or_none()
            to_be_edit.state = state_text
            to_be_edit.date_open = date_open_text
            to_be_edit.date_close = date_close_text
            to_be_edit.save()
            return jsonify({
                            'success': True,
                            'created': to_be_edit.id,
                            'cashier': to_be_edit

                        })
        else:
            raise RequestError(400)

    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)

    except Exception as error:
        abort(error.status)


'''
        GET cashier, return paginated results for cashiers
            http:127.0.0.1/cashier
            This endpoint should return a list of cashiers
'''
