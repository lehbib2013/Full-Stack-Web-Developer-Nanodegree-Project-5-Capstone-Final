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

captures_blueprint = Blueprint('captures_blueprint', __name__)

'''
GET Captures, return paginated results for Capture  by specifying\
fishingtied argument number
http:127.0.0.1/captures?tied=1
This endpoint should return a list of current page of Captures for\
specific tied argument,total of
captures of provided tied and current pagenumbe.
'''


@captures_blueprint.route("/captures")
@requires_auth("get:everything")
def get_all_captures(jwt):
    fishing_tied_id = request.args.get('tied', None, type=int)
    if 'tied' not in request.args:
        abort(400)
    print("test")
    try:
        list_captures = Capture.query\
            .filter(Capture.fishing_tied_id == fishing_tied_id).all()
        formatted_captures = [capture.format() for capture in
                              list_captures]
        return jsonify({
                'success': True,
                'captures': formatted_captures,
                'total': len(formatted_captures)
            })
    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)
    except Exception as error:
        print(sys.exc_info())
        print(error)
        abort(422)


'''
        POST  Capture
        {"specie_name":"xxx", "quantity":"xx" ,"captain_unit_price":"45",
        "unit_discount":"55","total_price":"3","unit_sale_price":"",
        "total_sale_price":"","fishing_tied_id":""}
'''


@captures_blueprint.route("/captures", methods=['POST'])
@requires_auth("post:everything")
def captures_post_request(jwt):
    body = request.get_json()
    try:
        specie_name_text = body.get('specie_name', 1)
        quantity_text = body.get('quantity', None)
        captain_unit_price_t = body.get('captain_unit_price', None)
        unit_discount_text = body.get('unit_discount', None)
        total_price_text = body.get('total_price', None)
        unit_sale_price_text = body.get('unit_sale_price', None)
        total_sale_price_text = body.get('total_sale_price', None)
        fishing_tied_id_text = body.get('fishing_tied_id', None)

        if (specie_name_text is not None) and (quantity_text is not None)\
            and (captain_unit_price_t is not None) and\
            (unit_discount_text is not None) and\
            (total_price_text is not None) and\
            (unit_sale_price_text is not None)\
            and (total_sale_price_text is not None)\
                and (fishing_tied_id_text is not None):
            to_be_added = Capture(specie_name=specie_name_text,
                                  quantity=quantity_text,
                                  captain_unit_price=captain_unit_price_t,
                                  unit_discount=unit_discount_text,
                                  total_price=total_price_text,
                                  unit_sale_price=unit_sale_price_text,
                                  total_sale_price=total_sale_price_text,
                                  fishing_tied_id=fishing_tied_id_text)
            to_be_added.insert()
            captures = Capture.query.filter(
                Capture.fishing_tied_id == fishing_tied_id_text).all()
            formatted_results = [item.format() for item in captures]
            return jsonify({
                            'success': True,
                            'created': to_be_added.id,
                            'captures': formatted_results

                        })
        else:
            raise RequestError(422)

    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)

    except Exception as error:
        print(sys.exc_info())
        print(error)
        abort(error.status)
