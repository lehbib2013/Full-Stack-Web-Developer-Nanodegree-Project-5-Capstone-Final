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
from flask_cors import CORS, cross_origin
import random
from sqlalchemy import null
from sqlalchemy import or_
from flaskr.auth.auth import AuthError, requires_auth
from jose import jwt
from six.moves.urllib.request import urlopen

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

supplier_blueprint = Blueprint('supplier_blueprint', __name__)


@supplier_blueprint.route('/suppliers_list', methods=['GET'])
@cross_origin()
@requires_auth("get:supplier")
def get_suppliers_list(jwt):
    current_page_number = request.args.get('page', 1, type=int)
    current_page_suppliers = Supplier.query.paginate(current_page_number,
                                                     per_page=20,
                                                     error_out=True,
                                                     max_per_page=20)

    suppliers_list = []
    for supplier in current_page_suppliers:
        suppliers_list.append({
                "id": supplier.id,
                "name": supplier.name
                })

    return render_template('pages/suppliers.html', suppliers=suppliers_list),\
        (200)


@supplier_blueprint.route("/suppliers")
@requires_auth("get:supplier")
def get_all_suppliers(jwt):
    current_page_number = request.args.get('page', 1, type=int)
    print("test")
    try:
        current_page_suppliers = Supplier.query.paginate(
            current_page_number, per_page=20, error_out=True,
            max_per_page=20)
        formatted_page_response = [cap.format() for cap in
                                   current_page_suppliers.items]
        return jsonify({
                  'success': True,
                  'currentPageContent': formatted_page_response,
                  'currentPageNumber': current_page_number,
                  'total': current_page_suppliers.total,
                  'nbrPages': current_page_suppliers.pages
              })
    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)

    except Exception as error:
        print(sys.exc_info())
        print(error)
        abort(422)


'''
          POST Supplier
          Create new Supplier by providing Body object with needed information:
          {"name":"Supp 1"}
'''


@supplier_blueprint.route("/suppliers", methods=['POST'])
@requires_auth("post:supplier")
def supplier_post_request(jwt):
    try:
        body = request.get_json()
        name_text = body.get('name', None)
        if 'name' not in body:
            raise RequestError(400)
        if (name_text is not None):
            to_be_added = Supplier(name=name_text)
            to_be_added.insert()
            fetched_page = Supplier.query.paginate(1, per_page=20,
                                                   error_out=True,
                                                   max_per_page=20)
            fetched_formatted_page = [supp.format() for supp in
                                      fetched_page.items]
            return jsonify({
                                'success': True,
                                'created': to_be_added.id,
                                'suppliers': fetched_formatted_page,
                                'nbrPages': fetched_page.pages
                            })
        else:
            raise RequestError(422)

    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)

    except Exception as error:
        print(sys.exc_info())
        print(error)
        abort(422)


@supplier_blueprint.route("/suppliers", methods=['PATCH'])
@requires_auth("patch:supplier")
def supplier_patch_request(jwt):
    body = request.get_json()
    try:
        id_text = body.get('id', None)
        name_text = body.get('name', None)
        
        if (id_text is not None) and (name_text is not None):
            to_be_edit = Supplier.query.filter(
                Supplier.id == id_text).one_or_none()
            to_be_edit.name = name_text
            to_be_edit.update()

            return jsonify({
                                'success': True,
                                'created': to_be_edit.id,
                                'supplier': to_be_edit.format()
                            })
        else:
            raise RequestError(400)

    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)

    except Exception as error:
        abort(error.status)


'''
  DELETE  supplier, delete supplier with id

'''


@supplier_blueprint.route("/suppliers/<int:supplier_id>", methods=["DELETE"])
@requires_auth("delete:everything")
def delete_supplier(jwt, supplier_id):
    try:
        current_supplier = Supplier.query.filter(Supplier.id ==
                                                 supplier_id).one_or_none()
        if current_supplier is None:
            raise RequestError(404)
        current_supplier.delete()
        current_page_suppliers = Supplier.query.paginate(1, per_page=20,
                                                         error_out=True,
                                                         max_per_page=20)
        formatted_page_response = [cap.format() for cap in
                                   current_page_suppliers.items]
        return jsonify({
                  'success': True,
                  'contentCurrentPage': formatted_page_response,
                  "deleted": current_supplier.id,
                  'currentPageNumber': 0,
                  'total': current_page_suppliers.total,
                  'nbrPages': current_page_suppliers.pages
              })

    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)

    except Exception as error:
        print(sys.exc_info())
        abort(error.status)
