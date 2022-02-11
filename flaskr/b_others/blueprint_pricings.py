
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

pricings_blueprint = Blueprint('pricings_blueprint', __name__)

'''
      GET pricingspecies, return paginated results for PricingSpecie  by \
        specifying page  argument number  http:127.0.0.1/pricings?page=1
        This endpoint should return a list of current page of pricingspecie \
          for current page argument.
'''


@pricings_blueprint.route("/pricings")
@requires_auth("get:everything")
def get_all_pricing(jwt):
    page = request.args.get('page', None, type=int)
    print("test")
    try:
        list_pricings = PricingSpecie.query.paginate(page, per_page=20,
                                                     error_out=True,
                                                     max_per_page=20)
        formatted_pricing = [pric.format() for pric in list_pricings.items]
        return jsonify({
                'success': True,
                'pricings': formatted_pricing,
                'total': list_pricings.total,
                'nbrpages': list_pricings.pages,

            })
    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)
    except Exception as error:
        print(sys.exc_info())
        print(error)
        abort(422)


'''
        POST PricingSpecie
        This endpoint will fix a standrd prices for every specie of fish ,
        so we can help user quickly
        estimate the total price and full all data.
        {"code_pricing":"43" }
'''


@pricings_blueprint.route("/pricings", methods=['POST'])
@requires_auth("post:everything")
def pricing_supplier_post_request(jwt):
    body = request.get_json()
    try:
        code_pricing_text = body.get('code_pricing', 1)
        if (code_pricing_text is not None):
            to_be_added = PricingSpecie(code_pricing=code_pricing_text)
            to_be_added.insert()
            first_fetched_page = PricingSpecie.query.filter(
                PricingSpecie.id == to_be_added.id).one_or_none()
            return jsonify({
                            'success': True,
                            'created': to_be_added.id,
                            'pricing': first_fetched_page.format()

                        })
        else:
            raise RequestError(400)

    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)

    except Exception as error:
        abort(error.status)
