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

policies_blueprint = Blueprint('policies_blueprint', __name__)

'''
GET yielddistributionpolicy, return plist of for YieldDistributionPolicy \
    by specifying page  argument number
    http:127.0.0.1/poicies
    This endpoint should return a list of Distribuion Policy.
'''


@policies_blueprint.route("/policies")
@requires_auth("get:everything")
def get_all_distributions(jwt):
    print("test")
    try:
        list_policies = YieldDistributionPolicy.query.all()
        formatted_policies = [poly.format() for poly in list_policies]
        return jsonify({
                'success': True,
                'policies': formatted_policies,
                'total': len(formatted_policies)
            })
    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)
    except Exception as error:
        print(sys.exc_info())
        print(error)
        abort(422)


@policies_blueprint.route("/policies", methods=['POST'])
@requires_auth("post:everything")
def policy_post_request(jwt):
    body = request.get_json()

    try:
        designation_text = body.get('designation', None)
        code_text = body.get('code', None)
        rate_company_text = body.get('rate_company', None)
        rate_captain_text = body.get('rate_captain', None)
        amortization_rate_text = body.get('amortization_rate', None)
        if (designation_text is not None) and (code_text is not None) and\
            (rate_company_text is not None) and \
            (rate_captain_text is not None) and \
                (amortization_rate_text is not None):
            to_be_added = YieldDistributionPolicy(
                designation=designation_text, code=code_text,
                rate_company=rate_company_text,
                rate_captain=rate_captain_text,
                amortization_rate=amortization_rate_text)
            to_be_added.insert()
            policies = YieldDistributionPolicy.query.all()
            formatted_results = [item.format() for item in policies]
            return jsonify({
                            'success': True,
                            'created': to_be_added.id,
                            'policies': formatted_results

                        })
        else:
            raise RequestError(422)

    except Exception as error:
        print(sys.exc_info())
        print(error)
        abort(error.status)
