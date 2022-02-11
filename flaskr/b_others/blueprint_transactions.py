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

transactions_blueprint = Blueprint('transactions_blueprint', __name__)

'''
        GET cashierTransactions, return list of cashierTransactions
        127.0.0.1:5000/transactions?page=1&journal_id=1
        This endpoint should return a list of current page of cashier \
          transactions for specific cashier argument,total of
        trnsactions of provided cashier and current pagenumbe.
    /transactions/<int:journal_id>
'''


@transactions_blueprint.route("/transactions")
@requires_auth("get:everything")
def get_all_transactions(jwt):
    page = request.args.get('page', 1, type=int)
    journal_id = request.args.get('journal_id', 1, type=int)
    if 'journal_id' not in request.args:
        abort(400)
    try:
        current_journal = CashierJournal.query \
            .filter(CashierJournal.id == journal_id) \
            .one_or_none()
        current_cashier = Cashier.query\
            .filter(Cashier.id == current_journal
                    .cashier_id).one_or_none()
        if current_cashier is None:
            raise RecursionError(404)
        current_transactions = CashierTransaction.query \
            .filter(CashierTransaction.journal_id ==
                    journal_id) \
            .paginate(page, per_page=20, error_out=True,
                      max_per_page=20)
        formatted_transactions = [journ.format() for journ in
                                  current_transactions.items]
        return jsonify({
                'success': True,
                'cashier': current_cashier.name_cashier,
                'codeJournal': current_journal.code,
                'moisJournal': current_journal.mois,
                'anneeJournal': current_journal.annee,
                'currentPageNumber': page,
                'transactionsJournalCurrentPage': formatted_transactions,
                'total': current_transactions.total,
                'nbrPages': current_transactions.pages
            })
    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)
    except Exception as error:
        print(sys.exc_info())
        print(error)
        abort(422)


'''
    POST CashierTransaction
    This endpoint will rely on Key Value of 'transaction_type' to add
    specific class.
    values of this key are :
          consummable, spartPart, general, salary, supply, captainpayement,
           avanvce ,
          supplier, ordinary
          for every Class, the body will contain needed informations to
          istanciate child class.
          To create SalaryTransaction :
                            {
                    "base":{
                              "transaction_sens":"Debit",
                              "transaction_date":"01-01-2012","transaction_reason":"xxxx",
                              "cash_amount":"13900","journal_id":1
                          },
                    "transaction_type":"salary"
                    }

          To create SupplyTransaction :
                    {
                "base":{
                          "transaction_sens":"Debit",
                          "transaction_date":"01-01-2012","transaction_reason":"xxxx",
                          "cash_amount":"13900","journal_id":1
                      },
                "transaction_type":"supply"
                    }
            Detailed informations will be included in Readme.
    '''


@transactions_blueprint.route("/transactions", methods=['POST'])
@requires_auth("post:everything")
def transactions_post_request():
    body = request.get_json(jwt)
    try:
        transaction_type = body.get('transaction_type', None)
        base = body.get('base', None)
        supplier = body.get('supplier', None)
        payment = body.get('payment', None)
        avance = body.get('avance', None)
        consumable = body.get('consumable', None)
        spartpart = body.get('spartpart', None)
        general = body.get('general', None)
        print(transaction_type)
        if (base is not None):
            if transaction_type == 'supply':
                tobe_added = SupplyCashierTransaction(
                    transaction_sens=base['transaction_sens'],
                    transaction_type='supply',
                    transaction_date=base['transaction_date'],
                    transaction_reason=base['transaction_reason'],
                    cash_amount=base['cash_amount'],
                    journal_id=base['journal_id'])
                tobe_added.insert()
                return jsonify({
                                'success': True,
                                'created': tobe_added.id
                            })

            if transaction_type == 'captainpayment':
                tobe_added = CaptainPaymentCashierTransaction(
                    transaction_sens=base['transaction_sens'],
                    transaction_type='captainpayment',
                    transaction_date=base['transaction_date'],
                    transaction_reason=base['transaction_reason'],
                    cash_amount=base['cash_amount'],
                    journal_id=base['journal_id'],
                    ref_payment=payment['ref_payment'],
                    fishing_tied=payment['fishing_tied'])
                tobe_added.insert()
                return jsonify({
                                'success': True,
                                'created': tobe_added.id
                            })
            if transaction_type == 'salary':
                tobe_added = SalaryCashierTransaction(
                    transaction_sens=base['transaction_sens'],
                    transaction_type='salary',
                    transaction_date=base['transaction_date'],
                    transaction_reason=base['transaction_reason'],
                    cash_amount=base['cash_amount'],
                    journal_id=base['journal_id'])
                tobe_added.insert()
                return jsonify({
                                'success': True,
                                'created': tobe_added.id
                            })

            if transaction_type == 'supplier':
                tobe_added = SupplierCashierTransaction(
                    transaction_sens=base['transaction_sens'],
                    transaction_type='supplier',
                    transaction_date=base['transaction_date'],
                    transaction_reason=base['transaction_reason'],
                    cash_amount=base['cash_amount'],
                    journal_id=base['journal_id'],
                    supplier_id=supplier['supplier_id'],
                    ref_invoice=supplier['ref_invoice'])
                tobe_added.insert()
                return jsonify({
                                'success': True,
                                'created': tobe_added.id
                            })

            if transaction_type == 'ordinary':
                tobe_added = OrdinaryCashierTransaction(
                    transaction_sens=base['transaction_sens'],
                    transaction_type='ordinary',
                    transaction_date=base['transaction_date'],
                    transaction_reason=base['transaction_reason'],
                    cash_amount=base['cash_amount'],
                    journal_id=base['journal_id'])
                tobe_added.insert()
                return jsonify({
                                'success': True,
                                'created': tobe_added.id
                            })

            if transaction_type == 'consumable':
                tobe_added = ConsumableCashierTransaction(
                    transaction_sens=base['transaction_sens'],
                    transaction_type='consumable',
                    transaction_date=base['transaction_date'],
                    transaction_reason=base['transaction_reason'],
                    cash_amount=base['cash_amount'],
                    weight_kg=consumable['weight_kg'],
                    unit_price=consumable['unit_price'],
                    total_price=consumable['total_price'],
                    imputed_captain_share=(
                        consumable['imputed_captain_share']),
                    non_imputed_share=consumable['non_imputed_share'],
                    fishing_tied=consumable['fishing_tied'],
                    journal_id=base['journal_id']
                    )
                tobe_added.insert()
                return jsonify({
                                'success': True,
                                'created': tobe_added.id
                            })

            if transaction_type == 'avance':
                tobe_added = AvanceCashierTransaction(
                    transaction_sens=base['transaction_sens'],
                    transaction_type='avance',
                    transaction_date=base['transaction_date'],
                    transaction_reason=base['transaction_reason'],
                    cash_amount=base['cash_amount'],
                    ref_avance=avance['ref_avance'],
                    fishing_tied=avance['fishing_tied'],
                    journal_id=base['journal_id'])
                tobe_added.insert()
                return jsonify({
                                'success': True,
                                'created': tobe_added.id
                            })

            if transaction_type == 'general':
                tobe_added = GeneralCashierTransaction(
                    transaction_sens=base['transaction_sens'],
                    transaction_type='general',
                    transaction_date=base['transaction_date'],
                    transaction_reason=base['transaction_reason'],
                    cash_amount=base['cash_amount'],
                    journal_id=base['journal_id'],
                    fishing_tied=general['fishing_tied'])
                tobe_added.insert()
                return jsonify({
                                'success': True,
                                'created': tobe_added.id
                            })
            if transaction_type == 'spartpart':
                tobe_added = SpartPartCashierTransaction(
                    transaction_sens=base['transaction_sens'],
                    transaction_type='spartpart',
                    transaction_date=base['transaction_date'],
                    transaction_reason=base['transaction_reason'],
                    cash_amount=base['cash_amount'],
                    weight_kg=spartpart['weight_kg'],
                    unit_price=spartpart['unit_price'],
                    total_price=spartpart['total_price'],
                    imputed_captain_share=spartpart['imputed_captain_share'],
                    non_imputed_share=spartpart['non_imputed_share'],
                    fishing_tied=spartpart['fishing_tied'],
                    journal_id=base['journal_id'])
                tobe_added.insert()
                return jsonify({
                                'success': True,
                                'created': tobe_added.id
                            })
        else:
            raise RecursionError(400)

    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)

    except Exception as error:
        print(sys.exc_info())
        print(error)
        abort(error.status)


