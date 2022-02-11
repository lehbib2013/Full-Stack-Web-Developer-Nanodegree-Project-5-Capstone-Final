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

species_blueprint = Blueprint('species_blueprint', __name__)

'''
    GET Specie, return paginated results for Capture  by specifying page \
    argument number http:127.0.0.1/species?page=1
    This endpoint should return a list of current page of Species for \
    specific  page argument,total of
    species of provided tied and current pagenumbe.
'''


@species_blueprint.route("/species")
@requires_auth("get:everything")
def get_all_species(jwt):
    page = request.args.get('page', 1, type=int)
    print("test")
    try:
        current_species = Specie.query.paginate(page, per_page=20,
                                                error_out=True,
                                                max_per_page=20)
        formatted_specie = [spec.format() for spec in
                            current_species.items]
        return jsonify({
                'success': True,
                'species': formatted_specie,
                'total': current_species.total,
                'pages': current_species.pages
            })
    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)
    except Exception as error:
        print(sys.exc_info())
        print(error)
        abort(422)


'''
        POST  Specie
        Create a specie of fish
        {"designation":"xxx", "famille":"xx" }
'''


@species_blueprint.route("/species", methods=['POST'])
@requires_auth("post:everything")
def species_post_request(jwt):
    body = request.get_json()
    try:
        designation_text = body.get('designation', None)
        famille_text = body.get('famille', None)

        if (designation_text is not None) and (famille_text is not None):
            to_be_added = Specie(designation=designation_text,
                                 famille=famille_text)
            to_be_added.insert()
            species = Specie.query.order_by(Specie.id).all()
            formatted_results = [item.format() for item in species]
            return jsonify({
                            'success': True,
                            'created': to_be_added.id,
                            'species': formatted_results

                        })
        else:
            raise RequestError(400)

    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)

    except Exception as error:
        abort(error.status)
