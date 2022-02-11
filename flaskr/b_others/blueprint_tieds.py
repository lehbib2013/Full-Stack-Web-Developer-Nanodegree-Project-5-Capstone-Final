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

tieds_blueprint = Blueprint('tieds_blueprint', __name__)

'''
      GET fishingTieds, return paginated results for FishingTieds by \
      specifying page and captain arguments number
      http:127.0.0.1/tieds?page=1&captain_id=1
      This endpoint should return a list of current page of Fishing Tieds for\
        specific captain argument,total of
      fishing tieds of provided cashier and current pagenumbe.
'''


@tieds_blueprint.route("/tieds")
@requires_auth("get:everything")
def get_all_fishing_tieds(jwt):
    page = request.args.get('page', 1, type=int)
    captain_id = request.args.get('captain_id', None, type=int)
    if 'captain_id' not in request.args:
        abort(400)
    print("test")
    try:
        current_fishing_tieds = FishingTied.query.filter(
            FishingTied.captain_id == captain_id) \
            .paginate(page, per_page=20, error_out=True, max_per_page=20)
        formatted_tieds = [journ.format() for journ in
                           current_fishing_tieds.items]
        return jsonify({
                'success': True,
                'tieds': formatted_tieds,
                'nbrPages': current_fishing_tieds.pages,
                'total': current_fishing_tieds.total
            })
    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)
    except Exception as error:
        print(sys.exc_info())
        print(error)
        abort(422)


'''
      POST FishingTied
      To create Fishing Tied with following Body.
      { "date_creation":"01-01-2022","date_departure":"01-01-2022",
      "date_arrival":"01-01-2022","amount_gained_captain":"8900",
      "amount_gained_company":"890",
      "total_estimate_price":"890","total_real_price":"7899" ,
      "retained_debt":"789","returned_asset":0,"previous_remained_debt":"0",
      "previous_remained_asset":"0",
      "policy_distribution_id":"","captain_id":""}
'''


@tieds_blueprint.route("/tieds", methods=['POST'])
@requires_auth("post:everything")
def fishing_post_request(jwt):
    body = request.get_json()

    try:
        date_creation_t = body.get('date_creation', 1)
        date_departure_t = body.get('date_departure', None)
        date_arrival_t = body.get('date_arrival', None)
        am_gai_cap_t = body.get('amount_gained_captain', None)
        am_gai_com_t = body.get('amount_gained_company', None)
        tot_est_pr_t = body.get('total_estimate_price', None)
        tot_real_pr_t = body.get('total_real_price', None)
        ret_debt_text = body.get('retained_debt_text', None)
        pr_rem_debt_t = body.get('previous_remained_debt', None)
        pr_rem_ass_t = body.get('previous_remained_asset', None)
        ret_asset_text = body.get('returned_asset', None)
        poli_distr_id = body.get('policy_distribution_id', None)
        captain_id_text = body.get('captain_id', None)
        if (date_creation_t is not None) and\
            (date_departure_t is not None) and\
            (captain_id_text is not None) and\
                (am_gai_cap_t is not None):
            to_be_added = FishingTied(date_creation=date_creation_t,
                                      date_departure=date_departure_t,
                                      date_arrival=date_arrival_t,
                                      amount_gained_captain=am_gai_cap_t,
                                      amount_gained_company=am_gai_com_t,
                                      total_estimate_price=tot_est_pr_t,
                                      total_real_price=tot_real_pr_t,
                                      retained_debt=ret_debt_text,
                                      returned_asset=ret_asset_text,
                                      previous_remained_debt=pr_rem_debt_t,
                                      previous_remained_asset=pr_rem_ass_t,
                                      policy_distribution_id=poli_distr_id,
                                      captain_id=captain_id_text)
            to_be_added.insert()
            first_fetched = FishingTied.query.filter(
              FishingTied.id == to_be_added.id).one_or_none()
            return jsonify({
                            'success': True,
                            'created': to_be_added.id,
                            'tied': first_fetched.format()

                        })
        else:
            raise RequestError(400)

    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)

    except Exception as error:
        abort(error.status)
