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

invoices_blueprint = Blueprint('invoices_blueprint', __name__)

'''
      GET invoicessuppliers, return paginated results for InvoicesSupplier \
        by specifying page and  supplier arguments number
      http:127.0.0.1/invoicessuppliers?page=1&supplier_id=1
      This endpoint should return a list of current page of Invoice Suppliers \
      for specific supplier argument,total of
      invoices of provided supplier and current pagenumbe.

'''


@invoices_blueprint.route("/invoices")
@requires_auth("get:everything")
def get_all_invoices_supplier(jwt):
    page = request.args.get('page', None, type=int)
    supplier_id = request.args.get('supplier_id', None, type=int)
    if 'supplier_id' not in request.args:
        abort(400)
    try:
        current_invoices_supplier = InvoiceSupplier.query\
            .filter(InvoiceSupplier.supplier_id == supplier_id)\
            .paginate(page, per_page=20, error_out=True, max_per_page=20)
        formatted_invoices = [journ.format() for journ in
                              current_invoices_supplier.items]
        return jsonify({
                'success': True,
                'invoices': formatted_invoices,
                'total': current_invoices_supplier.total,
                'nbrPaes': current_invoices_supplier.pages,
            })
    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)
    except Exception as error:
        print(sys.exc_info())
        print(error)
        abort(422)


'''
        POST InvoicesSupplier
        To create invoice of a supplier with following body
        { "montant":"01-01-2022","ref":"01-01-2022","date":"01-01-2022"}
'''


@invoices_blueprint.route("/invoices", methods=['POST'])
@requires_auth("post:everything")
def invoices_post_request(jwt):
    body = request.get_json()
    try:
        amount_text = body.get('montant', None)
        ref_text = body.get('ref', None)
        date_text = body.get('date', None)
        supplier_id = body.get('supplier_id', None)
        if (amount_text is not None) and (ref_text is not None) and\
           (date_text is not None):
            to_be_added = InvoiceSupplier(montant=amount_text,
                                          ref=ref_text, date=date_text,
                                          supplier_id=supplier_id)
            to_be_added.insert()
            invoices = InvoiceSupplier.query.filter(
                InvoiceSupplier.supplier_id == supplier_id).all()
            formatted_results = [item.format() for item in invoices]

            return jsonify({
                            'success': True,
                            'created': to_be_added.id,
                            'invoice': formatted_results
                        })
        else:
            raise RequestError(400)

    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)

    except Exception as error:
        abort(error.status)
