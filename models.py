from dataclasses import dataclass
import os
from sqlalchemy import Column, String, Boolean, Float, DateTime, Integer
import datetime
import enum
from flask_sqlalchemy import SQLAlchemy, BaseQuery
import json
from sqlalchemy.orm import relationship
from sqlalchemy.sql.elements import AnnotatedColumnElement
from sqlalchemy.sql.schema import ColumnDefault, ForeignKey
from sqlalchemy.sql.sqltypes import Date, DateTime
from flask_migrate import Migrate

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()
#  connect to a local postgresql database
CASHIER_TRANSACTION_ID = 'cashier_transactions.id'
FISHING_TIED_ID = 'fishing_tied.id'
'''
setup_db(app) binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Extend the base Model class to add common methods
'''


class BasicOperationsCRUD(db.Model):
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


'''
Question

# this class was added to avoid return 422 no
# matter what reason happened so we can controller
# returned statue code
# by the help of this link : https://stackoverflow.com/questions/68399132/
# failing-to-send-404-http-status-on-flask-when-client-tries-to-get-a-nonexistent
'''


class RequestError(Exception):
    def __init__(self, status):
        self.status = status

    def __str__(self):
        return repr(self.status)


class CashierState(enum.Enum):
    OPENED = 1
    CLOSED = 2


class CashierState(enum.Enum):
    OPENED = 1
    CLOSED = 2


class ConsumableType(enum.Enum):
    GASOIL = 1
    EAU = 2
    NOURITURE = 3
    SARDINE = 4
    GLACE = 5
    GENERAU = 7
    PDR = 8
    AUTRES = 9


class ExpenseType(enum.Enum):
    ACCOUNTABLE = 1
    NONACCOUNTABLE = 2


class TransactionSens(enum.Enum):
    Debit = 1
    Credit = 1


class TransactionType(enum.Enum):
    Consummable = 1
    SpartPart = 2
    General = 3
    Salary = 4
    CashSupply = 5
    CaptainPayement = 6
    Avanvce = 7
    SupplierPayement = 8
    Ordinary = 9


class FamilySpecies(enum.Enum):
    POUPLPE = 1
    PG = 2
    PF = 3
    PR = 4
    REJETS = 5


@dataclass
class Supplier(BasicOperationsCRUD):
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    transaction_cashier = relationship("SupplierCashierTransaction")
    invoices_supplier = relationship("InvoiceSupplier")

    def __init__(self, name):
        self.name = name

    def format(self):
        return {
          'id': self.id,
          'name': self.name
        }


@dataclass
class Captain(BasicOperationsCRUD):
    __tablename__ = "captain"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    bateau = Column(String)
    fishing_tieds = relationship("FishingTied", back_populates="captain")

    def __init__(self, name, bateau):
        self.name = name
        self.bateau = bateau

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'bateau': self.bateau
          }


@dataclass
class InvoiceSupplier(BasicOperationsCRUD):
    __tablename__ = 'invoice_supplier'
    id = Column(Integer, primary_key=True)
    montant = Column(Float)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    ref = Column(String)
    supplier_id = Column(Integer, ForeignKey("supplier.id"))

    def __init__(self, montant, date, ref, supplier_id):
        self.montant = montant
        self.date = date
        self.ref = ref
        self.supplier_id = supplier_id

    def format(self):
        return {
          'id': self.id,
          'montant': self.montant,
          'date': self.date,
          'ref': self.ref,
          'supplier_id': self.supplier_id
        }


@dataclass
class Cashier(BasicOperationsCRUD):
    __tablename__ = 'cashier'
    id = Column(Integer, primary_key=True)
    code_cashier = Column(String, nullable=True)
    name_cashier = Column(String, nullable=True)
    last_solde_opening = Column(Float, nullable=False)  # optional argument
    last_solde_closing = Column(Float, nullable=False)  # optional argument
    state = Column(String, default=CashierState.OPENED)
    date_open = Column(DateTime,  nullable=False)  # optional argument
    date_close = Column(DateTime,  nullable=True, default=None)
    cashier_journals = relationship("CashierJournal", back_populates="cashier")

    def __init__(self, code_cashier, name_cashier, last_solde_opening,
                 last_solde_closing, state, date_open, date_close):
        self.code_cashier = code_cashier
        self.name_cashier = name_cashier
        self.last_solde_opening = last_solde_opening
        self.last_solde_closing = last_solde_closing
        self.state = state
        self.date_open = date_open
        self.date_close = date_close

    def format(self):
        return {
          'id': self.id,
          'code_cashier': self.code_cashier,
          'name_cashier': self.name_cashier,
          'last_solde_opening': self.last_solde_opening,
          'last_solde_closing': self.last_solde_closing,
          'state': self.state,
          'date_open': self.date_open,
          'date_close': self.date_close
          }


@dataclass
class CashierJournal(BasicOperationsCRUD):
    __tablename__ = 'cashier_journal'
    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    mois = Column(Integer, nullable=False)
    annee = Column(Integer, nullable=False)
    cashier_id = Column(Integer, ForeignKey('cashier.id'))
    cashier = relationship("Cashier", back_populates="cashier_journals")
    transactions = relationship("CashierTransaction")

    def __init__(self, code, mois, annee, cashier_id):
        self.code = code
        self.mois = mois
        self.annee = annee
        self.cashier_id = cashier_id

    def format(self):
        return {
                'id': self.id,
                'code': self.code,
                'mois': self.mois,
                'annee': self.annee,
                'cashier_id': self.cashier_id
                }


@dataclass
class CashierTransaction(BasicOperationsCRUD):
    __tablename__ = 'cashier_transactions'

    id = Column(Integer, primary_key=True)
    transaction_sens = Column(String, nullable=False)  # Cor D
    transaction_type = Column(String)
    # Consummable, SpartPart, General,\
    # Salary,CashSupply, FishingTiedPayement, Other
    transaction_date = Column(DateTime, nullable=False)
    transaction_reason = Column(String)
    cash_amount = Column(Float)
    journal_id = Column(Integer, ForeignKey('cashier_journal.id'))

    __mapper_args__ = {
          'polymorphic_identity': 'transaction',
          'polymorphic_on': transaction_type
      }

    def __init__(self, transaction_sens, transaction_type,
                 transaction_date, transaction_reason, cash_amount,
                 journal_id):
        self.transaction_sens = transaction_sens
        self.transaction_type = transaction_type
        self.transaction_date = transaction_date
        self.transaction_reason = transaction_reason
        self.cash_amount = cash_amount
        self.journal_id = journal_id

    def format(self):
        return {
              'id': self.id,
              'transaction_sens': self.transaction_sens,
              'transaction_type': self.transaction_type,
              'transaction_date': self.transaction_date,
              'transaction_reason': self.transaction_reason,
              'cash_amount': self.cash_amount,
              'journal_id': self.journal_id
              }


@dataclass
class OrdinaryCashierTransaction(CashierTransaction):
    __tablename__ = 'ordinary_ct'
    __mapper_args__ = {'polymorphic_identity': 'ordinary'}
    id = Column(Integer, ForeignKey(CASHIER_TRANSACTION_ID),
                primary_key=True)

    def __init__(self, transaction_sens, transaction_type, transaction_date,
                 transaction_reason, cash_amount, journal_id):
        super().__init__(transaction_sens, transaction_type, transaction_date,
                         transaction_reason, cash_amount, journal_id)

    def format(self):
        return {
            'id': self.id,
            'transaction_sens': super().transaction_sens,
            'transaction_type': super().transaction_type,
            'transaction_date': super().transaction_date,
            'transaction_reason': super().transaction_reason,
            'cash_amount': super().cash_amount,
            'journal_id': super().journal_id
            }


@dataclass
class SalaryCashierTransaction(CashierTransaction):
    __tablename__ = 'salary_ct'
    __mapper_args__ = {'polymorphic_identity': 'salary'}
    id = Column(Integer, ForeignKey(CASHIER_TRANSACTION_ID),
                primary_key=True)

    def __init__(self,  transaction_sens, transaction_type, transaction_date,
                 transaction_reason, cash_amount, journal_id):
        super().__init__(transaction_sens, transaction_type,
                         transaction_date, transaction_reason,
                         cash_amount, journal_id)

    def format(self):
        return {
          'id': self.id,
          'transaction_sens': super().transaction_sens,
          'transaction_type': super().transaction_type,
          'transaction_date': super().transaction_date,
          'transaction_reason': super().transaction_reason,
          'cash_amount': super().cash_amount,
          'journal_id': super().journal_id
        }


@dataclass
class SupplyCashierTransaction(CashierTransaction):
    __tablename__ = 'supply_ct'
    __mapper_args__ = {'polymorphic_identity': 'supply'}
    id = Column(Integer, ForeignKey(CASHIER_TRANSACTION_ID),
                primary_key=True)

    def __init__(self,  transaction_sens, transaction_type, transaction_date,
                 transaction_reason, cash_amount, journal_id):
        super().__init__(transaction_sens, transaction_type,
                         transaction_date, transaction_reason,
                         cash_amount, journal_id)

    def format(self):
        return {
          'id': self.id
        }


@dataclass
class SupplierCashierTransaction(CashierTransaction):
    # cash <=0
    __tablename__ = 'supplier_ct'
    __mapper_args__ = {'polymorphic_identity': 'supplier'}
    id = Column(Integer, ForeignKey(CASHIER_TRANSACTION_ID),
                primary_key=True)
    supplier_id = Column(Integer, ForeignKey("supplier.id"))
    ref_invoice = Column(String)

    def __init__(self,  transaction_sens, transaction_type, transaction_date,
                 transaction_reason, cash_amount, supplier_id,
                 ref_invoice, journal_id):
        super().__init__(transaction_sens, transaction_type, transaction_date,
                         transaction_reason, cash_amount, journal_id)
        self.supplier_id = supplier_id
        self.ref_invoice = ref_invoice

    def format(self):
        return {
          'id': self.id,
          'transaction_sens': super().transaction_sens,
          'transaction_type': super().transaction_type,
          'transaction_date': super().transaction_date,
          'transaction_reason': super().transaction_reason,
          'cash_amount': super().cash_amount,
          'journal_id': super().journal_id,
          'supplier_id': self.supplier_id,
          'ref_invoice': self.ref_invoice
        }


@dataclass
class CaptainPaymentCashierTransaction(CashierTransaction):
    __tablename__ = 'Captain_payment_ct'
    __mapper_args__ = {'polymorphic_identity': 'captainpayment'}
    id = Column(Integer, ForeignKey(CASHIER_TRANSACTION_ID),
                primary_key=True)
    ref_payment = Column(String)
    fishing_tied = Column(Integer, ForeignKey(FISHING_TIED_ID))

    def __init__(self,  transaction_sens, transaction_type, transaction_date,
                 transaction_reason, cash_amount, ref_payment, fishing_tied,
                 journal_id):
        super().__init__(transaction_sens, transaction_type, transaction_date,
                         transaction_reason, cash_amount, journal_id)
        self.ref_payment = ref_payment
        self.fishing_tied = fishing_tied

    def format(self):
        return {
          'id': self.id,
          'transaction_sens': super().transaction_sens,
          'transaction_type': super().transaction_type,
          'transaction_date': super().transaction_date,
          'transaction_reason': super().transaction_reason,
          'cash_amount': super().cash_amount,
          'journal_id': super().journal_id,
          'ref_payment': self.ref_payment,
          'fishing_tied': self.fishing_tied
        }


@dataclass
class AvanceCashierTransaction(CashierTransaction):
    __tablename__ = 'avance_ct'
    __mapper_args__ = {'polymorphic_identity': 'avance'}
    id = Column(Integer, ForeignKey(CASHIER_TRANSACTION_ID),
                primary_key=True)
    ref_avance = Column(String)
    fishing_tied = Column(Integer, ForeignKey(FISHING_TIED_ID))

    def __init__(self,  transaction_sens, transaction_type, transaction_date,
                 transaction_reason, cash_amount, ref_avance, fishing_tied,
                 journal_id):
        super().__init__(transaction_sens, transaction_type, transaction_date,
                         transaction_reason, cash_amount, journal_id)
        self.ref_avance = ref_avance
        self.fishing_tied = fishing_tied
        self.cashier_journal_id = journal_id

    def format(self):
        return {
          'id': self.id,
          'transaction_sens': super().transaction_sens,
          'transaction_type': super().transaction_type,
          'transaction_date': super().transaction_date,
          'transaction_reason': super().transaction_reason,
          'cash_amount': super().cash_amount,
          'journal_id': super().journal_id,
          'ref_avance': self.ref_avance,
          'fishing_tied': self.fishing_tied
        }


@dataclass
class SpartPartCashierTransaction(CashierTransaction):
    __tablename__ = 'spartpart_ct'
    __mapper_args__ = {'polymorphic_identity': 'spartpart'}
    id = Column(Integer, ForeignKey(CASHIER_TRANSACTION_ID),
                primary_key=True)
    weight_kg = Column(Float)
    unit_price = Column(Float)
    total_price = Column(Float)
    imputed_captain_share = Column(Float)
    non_imputed_share = Column(Float)
    fishing_tied = Column(Integer, ForeignKey(FISHING_TIED_ID))

    def __init__(self, transaction_sens, transaction_type, transaction_date,
                 transaction_reason, cash_amount, weight_kg, unit_price,
                 total_price, imputed_captain_share, non_imputed_share,
                 fishing_tied, journal_id):
        super().__init__(transaction_sens, transaction_type, transaction_date,
                         transaction_reason, cash_amount, journal_id)
        self.weight_kg = weight_kg,
        self.unit_price = unit_price,
        self.total_price = total_price,
        self.imputed_captain_share = imputed_captain_share,
        self.non_imputed_share = non_imputed_share,
        self.fishing_tied = non_imputed_share,
        self.cashier_journal_id = non_imputed_share
        self.fishing_tied = fishing_tied

    def format(self):
        return {
          'id': self.id,
          'transaction_sens': super().transaction_sens,
          'transaction_type': super().transaction_type,
          'transaction_date': super().transaction_date,
          'transaction_reason': super().transaction_reason,
          'cash_amount': super().cash_amount,
          'journal_id': super().journal_id,
          'weight_kg': self.weight_kg,
          'unit_price': self.unit_price,
          'total_price': self.total_price,
          'imputed_captain_share': self.imputed_captain_share,
          'non_imputed_share': self.non_imputed_share,
          'fishing_tied': self.fishing_tied
            }


# cashe =0 par defaut
@dataclass
class ConsumableCashierTransaction(CashierTransaction):
    __tablename__ = 'consumable_ct'
    __mapper_args__ = {'polymorphic_identity': 'consumable'}
    id = Column(Integer, ForeignKey(CASHIER_TRANSACTION_ID),
                primary_key=True)
    weight_kg = Column(Float)
    unit_price = Column(Float)
    total_price = Column(Float)
    imputed_captain_share = Column(Float)
    non_imputed_share = Column(Float)
    fishing_tied = Column(Integer, ForeignKey(FISHING_TIED_ID))

    def __init__(self,  transaction_sens, transaction_type, transaction_date,
                 transaction_reason, cash_amount, weight_kg, unit_price,
                 total_price, imputed_captain_share, non_imputed_share,
                 fishing_tied, journal_id):
        super().__init__(transaction_sens, transaction_type, transaction_date,
                         transaction_reason, cash_amount, journal_id)
        self.weight_kg = weight_kg
        self.unit_price = unit_price
        self.total_price = total_price
        self.imputed_captain_share = imputed_captain_share
        self.non_imputed_share = non_imputed_share
        self.fishing_tied = non_imputed_share
        self.cashier_journal_id = non_imputed_share
        self.fishing_tied = fishing_tied

    def format(self):
        return {
                'id': self.id,
                'transaction_sens': super().transaction_sens,
                'transaction_type': super().transaction_type,
                'transaction_date': super().transaction_date,
                'transaction_reason': super().transaction_reason,
                'cash_amount': super().cash_amount,
                'journal_id': super().journal_id,
                'weight_kg': self.weight_kg,
                'unit_price': self.unit_price,
                'total_price': self.total_price,
                'imputed_captain_share': self.imputed_captain_share,
                'non_imputed_share': self.non_imputed_share,
                'fishing_tied': self.fishing_tied
              }


@dataclass
class GeneralCashierTransaction(CashierTransaction):
    __tablename__ = 'general_ct'
    __mapper_args__ = {'polymorphic_identity': 'general'}
    id = Column(Integer, ForeignKey(CASHIER_TRANSACTION_ID),
                primary_key=True)
    fishing_tied = Column(Integer, ForeignKey(FISHING_TIED_ID))

    def __init__(self,  transaction_sens, transaction_type, transaction_date,
                 transaction_reason, cash_amount, fishing_tied, journal_id):
        super().__init__(transaction_sens, transaction_type, transaction_date,
                         transaction_reason, cash_amount, journal_id)
        self.fishing_tied = fishing_tied

    def format(self):
        return {
          'id': self.id,
          'fishing_tied': self.fishing_tied,
          'transaction_sens': super().transaction_sens,
          'transaction_date': super().transaction_date,
          'transaction_type': super().transaction_type,
          'transaction_reason': super().transaction_reason,
          'cash_amount': super().cash_amount,
          'journal_id': super().journal_id,
        }


@dataclass
class YieldDistributionPolicy(BasicOperationsCRUD):
    __tablename__ = "distribution_policy"
    id = Column(Integer, primary_key=True)
    designation = Column(String)
    code = Column(String)
    rate_company = Column(Float)
    rate_captain = Column(Float)
    amortization_rate = Column(Float)

    def __init__(self,  designation, code, rate_company, rate_captain,
                 amortization_rate):
        self.designation = designation
        self.code = code
        self.rate_company = rate_company
        self.rate_captain = rate_captain
        self.amortization_rate = amortization_rate

    def format(self):
        return {
          'id': self.id,
          'designation': self.designation,
          'code': self.code,
          'rate_company': self.rate_company,
          'rate_captain': self.rate_captain,
          'amortization_rate': self.amortization_rate
          }


@dataclass
class FishingTied(BasicOperationsCRUD):
    __tablename__ = 'fishing_tied'
    id = Column(Integer, primary_key=True)
    date_creation = Column(DateTime, nullable=False)
    date_departure = Column(DateTime, nullable=False)
    date_arrival = Column(DateTime, nullable=True)
    amount_gained_captain = Column(Float, default=0)
    amount_gained_company = Column(Float, default=0)
    total_estimate_price = Column(Float)
    total_real_price = Column(Float)
    retained_debt = Column(Float, default=0)
    returned_asset = Column(Float, default=0)
    previous_remained_debt = Column(Float, default=0)
    previous_remained_asset = Column(Float, default=0)
    policy_distribution_id = Column(Integer)
    transactions_captains = relationship("CaptainPaymentCashierTransaction")
    transactions_consum = relationship("ConsumableCashierTransaction")
    transactions_spartpart = relationship("SpartPartCashierTransaction")
    transactions_avance = relationship("AvanceCashierTransaction")
    transactions_generals = relationship("GeneralCashierTransaction")
    captures_of_fishing_tied = relationship("Capture")
    captain_id = Column(Integer, ForeignKey("captain.id"))
    captain = relationship("Captain", back_populates="fishing_tieds")

    def __init__(self,  date_creation, date_departure, date_arrival,
                 amount_gained_captain, amount_gained_company,
                 total_estimate_price, total_real_price, retained_debt,
                 returned_asset, previous_remained_debt,
                 previous_remained_asset, policy_distribution_id, captain_id):

        self.date_creation = date_creation
        self.date_departure = date_departure
        self.date_arrival = date_arrival
        self.amount_gained_captain = amount_gained_captain
        self.amount_gained_company = amount_gained_company
        self.total_estimate_price = total_estimate_price
        self.total_real_price = total_real_price
        self.retained_debt = retained_debt
        self.returned_asset = returned_asset
        self.previous_remained_debt = previous_remained_debt
        self.previous_remained_asset = previous_remained_asset
        self.policy_distribution_id = policy_distribution_id
        self.captain_id = captain_id

    def format(self):
        return {
          'id': self.id,
          'date_creation': self.date_creation,
          'date_departure': self.date_departure,
          'date_arrival': self.date_arrival,
          'amount_gained_captain': self.amount_gained_captain,
          'amount_gained_company': self.amount_gained_company,
          'total_estimate_price': self.total_estimate_price,
          'total_real_price': self.total_real_price,
          'retained_debt': self.retained_debt,
          'returned_asset': self.returned_asset,
          'previous_remained_debt': self.previous_remained_debt,
          'previous_remained_asset': self.previous_remained_asset,
          'policy_distribution_id': self.policy_distribution_id,
          'captain_id': self.captain_id
         }


@dataclass
class Capture(BasicOperationsCRUD):
    __tablename__ = 'capture'
    id = Column(Integer, primary_key=True)
    specie_name = Column(String)
    quantity = Column(Float)
    captain_unit_price = Column(Float)
    unit_discount = Column(Float)
    total_price = Column(Float)
    unit_sale_price = Column(Float)
    total_sale_price = Column(Float)
    fishing_tied_id = Column(Integer, ForeignKey(FISHING_TIED_ID))

    def __init__(self,  specie_name, quantity, captain_unit_price,
                 unit_discount, total_price, unit_sale_price, total_sale_price,
                 fishing_tied_id):

        self.specie_name = specie_name
        self.quantity = quantity
        self.captain_unit_price = captain_unit_price
        self.unit_discount = unit_discount
        self.total_price = total_price
        self.unit_sale_price = unit_sale_price
        self.total_sale_price = total_sale_price
        self.fishing_tied_id = fishing_tied_id

    def format(self):
        return {
          'id': self.id,
          'specie_name': self.specie_name,
          'quantity': self.quantity,
          'captain_unit_price': self.captain_unit_price,
          'unit_discount': self.unit_discount,
          'total_price': self.total_price,
          'unit_sale_price': self.unit_sale_price,
          'total_sale_price': self.total_sale_price,
          'fishing_tied_id': self.fishing_tied_id
        }


@dataclass
class Specie(BasicOperationsCRUD):
    __tablename__ = "specie"
    id = Column(Integer, primary_key=True)
    designation = Column(String)
    famille = Column(String)

    def __init__(self, designation, famille):

        self.designation = designation
        self.famille = famille

    def format(self):
        return {
          'id': self.id,
          'designation': self.designation,
          'famille': self.famille
        }


@dataclass
class PricingSpecie(BasicOperationsCRUD):
    __tablename__ = "pricing_specie"
    id = Column(Integer, primary_key=True)
    code_pricing = Column(String)
    details_pricing = relationship("DetailsPricingSpecie",
                                   back_populates="pricing")

    def __init__(self,  code_pricing):
        self.code_pricing = code_pricing

    def format(self):
        return {
          'id': self.id,
          'code_pricing': self.code_pricing
        }


@dataclass
class DetailsPricingSpecie(BasicOperationsCRUD):
    __tablename__ = "details_pricing_specie"
    id = Column(Integer, primary_key=True)
    pricing_id = Column(Integer, ForeignKey("pricing_specie.id"))
    pricing = relationship("PricingSpecie", back_populates="details_pricing")
    specie_id = Column(Integer, ForeignKey("specie.id"))
    border_quantity = Column(Float)
    unit_price_calc_of_superior_quantity_for_captain = Column(Float)
    unit_price_calc_of_inferior_quantity_for_captain = Column(Float)
    unit_price_sale = Column(Float)

    def __init__(self, pricing_id, specie_id, border_quantity,
                 unit_price_calc_of_superior_quantity_for_captain,
                 unit_price_calc_of_inferior_quantity_for_captain,
                 unit_price_sale):

        self.pricing_id = pricing_id
        self.specie_id = specie_id
        self.border_quantity = border_quantity
        self.unit_price_calc_of_superior_quantity_for_captain = \
            unit_price_calc_of_superior_quantity_for_captain
        self.unit_price_calc_of_inferior_quantity_for_captain = \
            unit_price_calc_of_inferior_quantity_for_captain
        self.unit_price_sale = unit_price_sale

    def format(self):
        return {
          'id': self.id,
          'pricing_id': self.pricing_id,
          'pricing': self.pricing.code_pricing,
          'specie_id': self.specie_id,
          'border_quantity': self.border_quantity,
          'unit_price_calc_of_superior_quantity_for_captain':
          self.unit_price_calc_of_superior_quantity_for_captain,
          'unit_price_calc_of_inferior_quantity_for_captain':
          self.unit_price_calc_of_inferior_quantity_for_captain,
          'unit_price_sale': self.unit_price_sale
        }
