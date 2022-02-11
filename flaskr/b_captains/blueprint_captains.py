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
from flaskr.auth.auth import AuthError, requires_auth, requires_auth_regular
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

captain_blueprint = Blueprint('captain_blueprint', __name__)


'''
 GET captains, return paginated results for captains by specifying\
             page argument number
 http:127.0.0.1/captains?page=1
 This endpoint should return a list of current page of captains,\
            number of total captains,
 current page number.
'''


@captain_blueprint.route('/captains_list', methods=['GET'])
@requires_auth_regular
def get_captains_list():
    print("testttt")
    current_page_number = request.args.get('page', 1, type=int)
    current_page_captains = Captain.query.paginate(current_page_number,
                                                   per_page=20,
                                                   error_out=True,
                                                   max_per_page=20)

    captains_list = []
    for captain in current_page_captains:
        captains_list.append({
                "id": captain.id,
                "name": captain.name
                })

    return render_template('pages/captains.html', userinfo=session['profile'],
                           captains=captains_list), 200


@captain_blueprint.route("/captains")
@requires_auth("get:captain")
def get_all_captains(jwt):
    current_page_number = request.args.get('page', 1, type=int)
    print("test")
    try:
        current_page_captains = Captain.query.paginate(current_page_number,
                                                       per_page=20,
                                                       error_out=True,
                                                       max_per_page=20)
        formatted_page_response = [cap.format() for cap in
                                   current_page_captains.items]
        return jsonify({
                  'success': True,
                  'currentPageContent': formatted_page_response,
                  'currentPageNumber': current_page_number,
                  'total': current_page_captains.total,
                  'nbrPages': current_page_captains.pages
              })
    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)

    except Exception as error:
        print(sys.exc_info())
        print(error)
        abort(422)


'''
          POST Captain
          Create new Captain by providing Body object with needed information:
          {"name":"Ahmed","bateau":"Bateau Ely"}
'''


@captain_blueprint.route("/captains", methods=['POST'])
@requires_auth("post:captain")
def captain_post_request(jwt):
    try:
        body = request.get_json()
        name_text = body.get('name', None)
        bateau_text = body.get('bateau', None)
        if (name_text is not None) and (bateau_text is not None):
            to_be_added = Captain(name=name_text, bateau=bateau_text)
            to_be_added.insert()
            fetched_page = Captain.query.paginate(1, per_page=20,
                                                  error_out=True,
                                                  max_per_page=20)
            fetched_formatted_page = [quest.format() for quest in
                                      fetched_page.items]
            return jsonify({
                                'success': True,
                                'created': to_be_added.id,
                                'captains': fetched_formatted_page,
                                'nbrPages': fetched_page.pages,
                                'total': fetched_page.total,
                            })
        else:
            raise RequestError(400)

    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)

    except Exception as error:
        print(sys.exc_info())
        print(error)
        abort(422)


'''
          PATCH Captain
          Create new Captain by providing Body object with needed information:
          {"id":"1","name":"Ahmed","bateau":"Bateau Ely"}

'''


@captain_blueprint.route("/captains", methods=['PATCH'])
@requires_auth("patch:captain")
def captain_patch_request(jwt):
    body = request.get_json()
    try:
        id_text = body.get('id', None)
        name_text = body.get('name', None)
        bateau_text = body.get('bateau', None)
        if (id_text is not None) and (name_text is not None) and\
           (bateau_text is not None):
            to_be_edit = Captain.query.filter(
                Captain.id == id_text).one_or_none()
            to_be_edit.name = name_text
            to_be_edit.bateau = bateau_text
            to_be_edit.update()

            return jsonify({
                                'success': True,
                                'created': to_be_edit.id,
                                'captain': to_be_edit.format()
                            })
        else:
            raise RequestError(400)

    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)

    except Exception as error:
        abort(error.status)


'''
          DELETE captains, delete captain with id
'''


@captain_blueprint.route("/captains/<int:captain_id>", methods=["DELETE"])
@requires_auth("delete:everything")
def delete_captain(jwt, captain_id):
    try:
        current_captain = Captain.query.filter(Captain.id ==
                                               captain_id).one_or_none()
        if current_captain is None:
            raise RequestError(404)
        current_captain.delete()
        current_page_captains = Captain.query.paginate(1, per_page=20,
                                                       error_out=True,
                                                       max_per_page=20)
        formatted_page_response = [cap.format() for cap in
                                   current_page_captains.items]
        return jsonify({
              'success': True,
              'contentCurrentPage': formatted_page_response,
              'currentPageNumber': 0,
              'deleted': current_captain.id,
              'total': current_page_captains.total,
              'nbrPages': current_page_captains.pages
              })
    except RequestError as error:
        print(sys.exc_info())
        abort(error.status)

    except Exception as error:
        print(sys.exc_info())
        abort(error.status)
