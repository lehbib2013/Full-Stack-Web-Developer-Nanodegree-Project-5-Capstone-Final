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

detailspricing_blueprint = Blueprint('detailspricing_blueprint', __name__)


'''
      GET detailspricingSpecie, return paginated results for \
        DetailsPricingSpecie  by specifying pricingspecie  argument number
      http:127.0.0.1/detailspricing?pricing_id=1
        This endpoint should return a details  of current provided\
        pricingspecie.
'''


@detailspricing_blueprint.route("/detailspricing")
@requires_auth("get:everything")
def get_details_pricing(jwt):
    pricing_id = request.args.get('pricing_id', None, type=int)
    if 'pricing_id' not in request.args:
        abort(400)
    try:
        list_details_pricings = DetailsPricingSpecie.query.filter(
            DetailsPricingSpecie.pricing_id == pricing_id).all()
        formatted_details_pricing = [detpric.format() for detpric in
                                     list_details_pricings]
        return jsonify({
                'success': True,
                'details': formatted_details_pricing,
                'total': len(list_details_pricings)
            })
    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)
    except Exception as error:
        print(sys.exc_info())
        print(error)
        abort(422)


'''
        POST DetailsPricingSpecie
        This is a content of pricing for every specie .
        To encourage a captain of board to get more fish there are
        two prices to adapt from them based on quantity
        {"pricing_id":"1","specie_id":"1","border_quantity":"34",
        "unit_price_calc_of_superior_quantity_for_captain":"32",
        "unit_price_calc_of_inferior_quantity_for_captain":"234",
        "unit_price_sale":"122"}
'''


@detailspricing_blueprint.route("/detailspricing", methods=['POST'])
@requires_auth("post:everything")
def details_post_request(jwt):
    body = request.get_json()
    up_cal_inf = 'unit_price_calc_of_superior_quantity_for_captain'
    up_cal_sup = 'unit_price_calc_of_inferior_quantity_for_captain'
    try:
        pricing_id_text = body.get('pricing_id', None)
        specie_id_text = body.get('specie_id', None)
        border_q_t = body.get('border_quantity', None)
        u_p_c_of_sup_t = body.get(up_cal_inf, None)
        u_p_c_of_inf_t = body.get(up_cal_sup, None)
        u_p_sale_t = body.get('unit_price_sale', None)

        if (pricing_id_text is not None) and (specie_id_text is not None)\
            and (border_q_t is not None) and\
            (u_p_c_of_sup_t is not None) and\
                (u_p_c_of_inf_t is not None) and (u_p_sale_t is not None):
            to_be_added = DetailsPricingSpecie(pricing_id=pricing_id_text,
                                               specie_id=specie_id_text,
                                               border_quantity=border_q_t,
                                               unit_price_calc_of_superior_quantity_for_captain=u_p_c_of_sup_t,
                                               unit_price_calc_of_inferior_quantity_for_captain=u_p_c_of_inf_t,
                                               unit_price_sale=u_p_sale_t)
            to_be_added.insert()
            fetched_results = DetailsPricingSpecie.query.filter(
                DetailsPricingSpecie.pricing_id == pricing_id_text).all()
            formatted_results = [item.format() for item in fetched_results]
            return jsonify({
                                'success': True,
                                'created': to_be_added.id,
                                'detail': formatted_results

                            })
        else:
            raise RequestError(400)

    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)

    except Exception as error:
        abort(error.status)
