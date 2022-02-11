# Motivation for project

This project is my last capstone project for Full Stack Developer Nanodegree and it comes to build a bonding experience for a fishing company called AYA.
At the end of this course I decided to rewrite one of my preview JAVA projects from old days to a FLASK Stack to master all concepts on a real professional projects.
In my future front end projects I will accomplish this app.

# Udacity Capstone Project

This company has some boats which make tieds on regular basic times (every one or two weeks).
At the end of each tied, the boat must declare the catched quantities during his last tide.
Finally these quantities will be sell on the local market and collected funds will be saved in companies cashier for later repartition.
The fishing company will share the received funds of this operation with captain of boat for every completed tide.
Before any repartition of the funds: all registered expenses or advanced cashes will be deducted and get back to company4s account as these charges were payed by the company to facilitate the tied flow work .
There are some sort of  agreements in the form of policies fixing the rates of the share for every part(either company or captain).
So when the amount of the repartition will be calculated , this will happen on a basis of policy s provided rates.
For different boats there are different policies.
Expenses of any tde can be different but there are main parts:
1. # Consumables : like water,... (they are fixed and rarely changing)
2. # Spart parts : like any replacement due to a mecanic repair or similar needs
3. # General : like other basic expenses 

Current project will build an API to to satisfy provided bussness requirements. 

I used and inspired many parts of this work from a  some  provided examples coding from instructor's videos course as well as from my previous projects and valued advices of mentors during the past reviews.

For this project I used   virtual environement venv to manage separatly all dependencies needed by project 

# create and activate a virtual environment
```
python3 -m venv venv
source venv/bin/activate
```


# Getting Started

# Pererequisites  & Installations
Python3 ,pip3 and node are required for a developper to use  current API.

to install all needed moduls including Flask ,SQLAlchemy ,Flask-Cors and softwares :
```
   pip3 install -r requirements.txt
```
with postgres running lunch:
```
psql aya < aya.psql
```
after moving to [starter] directory , run the backend as following:

# For Mac/Linux
```
export FLASK_APP=flaskr
export FLASK_ENV=development
```
# For Windows
```
set FLASK_APP=flaskr
set FLASK_ENV=development
```
# Make sure to run this command from the project directory (not from the flaskr)
```
flask run
```
# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/flaskr` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 


# Tests
For Tests, you need to lunch following command to prepare test environement.
```
dropdb aya_test
createdb aya_test
psql aya_test < aya.psql
python test_flaskr.py

```

All API Endpoints where tested by TDD Approach.

# Getting tokens to use for testing
to be able to test endpoints from CURL or POSTMAN, it  is necessary to open this url:
```
https://dev-llz9tf-n.us.auth0.com/authorize?audience=mycapstone&response_type=token&client_id=xRUm9KcctNSUOTPZd4sKJvjeLj3uhJKf&redirect_uri=https://localhost:8080/login-result

```
in case you getting an expired token response, you need to logout before executing the preview URL :
```
{
    "code": "token_expired",
    "description": "token is expired"
}
```
the address you need to open to logout in the first (in such case) is :
```
https://dev-llz9tf-n.us.auth0.com/v2/logout?client_id=xRUm9KcctNSUOTPZd4sKJvjeLj3uhJKf&token_type=Bearer
```
After this, lunch:
```
https://dev-llz9tf-n.us.auth0.com/authorize?audience=mycapstone&response_type=token&client_id=xRUm9KcctNSUOTPZd4sKJvjeLj3uhJKf&redirect_uri=https://localhost:8080/login-result

```
# RBAC
In this app , there are two roles :
1. master role grantedto execute  all  GET/POST/PATCH/DELETE operations on all objects
2. agent role with ability just to execute only GET operations.

# the configured permissions are :
post:everything
patch:everything
get:everything
delete: everything
additionally and to match project specifications there are also:
get:supplier
post:supplier
get:supplier
patch:supplier
get:scaptain
post:captain
get:captain
patch:captain

# there are two users :
master role assigned for  user : 
# devexpress2013@gmail with password : GooglE2013$$
and 
agent role assigned for:
# user : lehbib@agrineq.mr with password :GooglE2013##


# Migrating database
Before lunching migrations commands , we need to export the DATABASE_URL :

export DATABASE_URL = "postgresql://postgres@localhost:5432/aya"

 ```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
 ```

 Alternatively, it is possible to use Flask CLI instead of using running manage.py file:
 ```
export DATABASE_URL=your_local_url
export FLASK_APP=flaskr
export FLASK_ENV=dev
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
 ```
# setup env variables locally 
```
chmod +x setup.sh
source setup.sh
```
# API References

**Getting started**

This app can be hosted only locally at following base url : (http://127.0.0.1:5000/) and it can communicate in the future with any frontend module.
During the design, I applied the joined table inheritance concept during modeling of CashierTransaction object.
The user of futur app will work on his own Cashier to input some transactions linked to fishing activity as explained earlier.
The cashier transaction can be one of the following cases :
 # Consummable : this is a transaction type of expense related to every tide. it includes : water ,fuel,sardine ..
 # SpartPart : this is a transaction type of expense related to every tide. it includes exclusivly spart parts
 # General  : this is a transaction type of general expense related to every tide. it includes general rubrics
 # Salary : this is a transaction type of expense related to a salaries of a team company.
 # CashSupply : this is a transaction type of supplying a cashier with needed funds (from bank or other sources)
 # CaptainPayement : this is a transaction type to pay an amount of gained funds part for a captain after he    completed a tide.
 # Avanvce  this is a transaction type to save an advance cash to a captain (this will be deducted after tide completion from his gained amount part)
 # SupplierPayement : tis transaction type to modelize the payments of the suppliers
 # Ordinary  : this is a general trnsaction of cash not related to a tide but to a general activity.
 
 Inheritance will facilitate the API work. we need just one endpoint /transactions to get and post the different types of transactions but just we will use different bodies for different post requests to get the job quickly done.

 GET /transactions?page=1&journal_id=1
 ```
 {
    "anneeJournal": 2022,
    "cashier": "Cashier 02",
    "codeJournal": "JOURN022022",
    "currentPageNumber": 1,
    "moisJournal": 2,
    "nbrPages": 1,
    "success": true,
    "total": 10,
    "transactionsJournalCurrentPage": [
        {
            "cash_amount": 13900.0,
            "id": 1,
            "journal_id": 1,
            "transaction_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "transaction_reason": "xxxx",
            "transaction_sens": "Debit",
            "transaction_type": "salary"
        },
        {
            "cash_amount": 13900.0,
            "id": 2,
            "journal_id": 1,
            "ref_invoice": "JKKKK",
            "supplier_id": 1,
            "transaction_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "transaction_reason": "xxxx",
            "transaction_sens": "Debit",
            "transaction_type": "supplier"
        },
        {
            "id": 3
        },
        {
            "cash_amount": 13900.0,
            "id": 4,
            "journal_id": 1,
            "ref_invoice": "JKKKK",
            "supplier_id": 1,
            "transaction_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "transaction_reason": "xxxx",
            "transaction_sens": "Debit",
            "transaction_type": "supplier"
        },
        {
            "cash_amount": 34500.0,
            "fishing_tied": 1,
            "id": 5,
            "journal_id": 1,
            "ref_payment": "deuxiem payement",
            "transaction_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "transaction_reason": "paiment de capitaine",
            "transaction_sens": "Credit",
            "transaction_type": "captainpayment"
        },
        {
            "cash_amount": 4500.0,
            "fishing_tied": 1,
            "id": 6,
            "journal_id": 1,
            "ref_avance": "avance capitaine ",
            "transaction_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "transaction_reason": "avance capitaine",
            "transaction_sens": "Debit",
            "transaction_type": "avance"
        },
        {
            "cash_amount": 34000.0,
            "fishing_tied": 15.0,
            "id": 7,
            "imputed_captain_share": 4500.0,
            "journal_id": 1,
            "non_imputed_share": 15.0,
            "total_price": 47000.0,
            "transaction_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "transaction_reason": "spart part 1",
            "transaction_sens": "Debit",
            "transaction_type": "spartpart",
            "unit_price": 45.0,
            "weight_kg": 234.0
        },
        {
            "cash_amount": 34000.0,
            "fishing_tied": 1,
            "id": 8,
            "imputed_captain_share": 0.0,
            "journal_id": 1,
            "non_imputed_share": 12345.0,
            "total_price": 46780.0,
            "transaction_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "transaction_reason": "Consum 1x",
            "transaction_sens": "Debit",
            "transaction_type": "consumable",
            "unit_price": 20.0,
            "weight_kg": 23.0
        },
        {
            "cash_amount": 13900.0,
            "id": 9,
            "journal_id": 1,
            "transaction_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "transaction_reason": "xxxx",
            "transaction_sens": "Debit",
            "transaction_type": "ordinary"
        },
        {
            "cash_amount": 13900.0,
            "fishing_tied": 1,
            "id": 10,
            "journal_id": 1,
            "transaction_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "transaction_reason": "xxxx",
            "transaction_sens": "Debit",
            "transaction_type": "general"
        }
    ]
}
 ```
 *** Note ***
 For simplicity , timeline and to be conform to project requirement I will be limited for this reference to ducment here just two objects : **Captain** and  **Supplier** and for four type of operations: **GET/DELETE/POST/PATCH**.
 However all API Endpoints worked well and was tested with CURL and POSTMAN.

 Test Driven Developement was succesfully checked aginst all endpoints of **Captain** and  **Supplier**.

For POST requests, this a simple example to post an specific type **CaptainPaymentCashierTransaction** :
# POST /transactions   
# Body :
```
{
"base":{
          "transaction_sens":"Credit",
          "transaction_date":"01-01-2012","transaction_reason":"paiment de capitaine","cash_amount":"34500","journal_id":1
       },
"payment":{
    "ref_payment":"deuxiem payement",
    "fishing_tied":"1"
},
"transaction_type":"captainpayment"
}
```
# Returned response :
```
{
    "created": 5,
    "success": true
}
```

**Errors handling**

the errors are returned in the following [json formats] :

```
{
  "error": 422, 
  "message": "Unprocessoble error", 
  "success": true
}
The API can return following error codes:
404 : if resource wasn't found
422 : if error is not processable 
400 : if the request is bad
405 : if the method is not allowed
```

**Endpoints Description**
 All Endpoints was tested on POSTMAN and CURL
# 1. Suppliers

 # GET /suppliers
retuns a ist of suppliers 

```
sample:  127.0.0.1:5000/transactions?page=1&journal_id=1

{
    "anneeJournal": 2022,
    "cashier": "Cashier 02",
    "codeJournal": "JOURN022022",
    "currentPageNumber": 1,
    "moisJournal": 2,
    "nbrPages": 1,
    "success": true,
    "total": 10,
    "transactionsJournalCurrentPage": [
        {
            "cash_amount": 13900.0,
            "id": 1,
            "journal_id": 1,
            "transaction_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "transaction_reason": "xxxx",
            "transaction_sens": "Debit",
            "transaction_type": "salary"
        },
        {
            "cash_amount": 13900.0,
            "id": 2,
            "journal_id": 1,
            "ref_invoice": "JKKKK",
            "supplier_id": 1,
            "transaction_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "transaction_reason": "xxxx",
            "transaction_sens": "Debit",
            "transaction_type": "supplier"
        },
        {
            "id": 3
        },
        {
            "cash_amount": 13900.0,
            "id": 4,
            "journal_id": 1,
            "ref_invoice": "JKKKK",
            "supplier_id": 1,
            "transaction_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "transaction_reason": "xxxx",
            "transaction_sens": "Debit",
            "transaction_type": "supplier"
        },
        {
            "cash_amount": 34500.0,
            "fishing_tied": 1,
            "id": 5,
            "journal_id": 1,
            "ref_payment": "deuxiem payement",
            "transaction_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "transaction_reason": "paiment de capitaine",
            "transaction_sens": "Credit",
            "transaction_type": "captainpayment"
        },
        {
            "cash_amount": 4500.0,
            "fishing_tied": 1,
            "id": 6,
            "journal_id": 1,
            "ref_avance": "avance capitaine ",
            "transaction_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "transaction_reason": "avance capitaine",
            "transaction_sens": "Debit",
            "transaction_type": "avance"
        },
        {
            "cash_amount": 34000.0,
            "fishing_tied": 15.0,
            "id": 7,
            "imputed_captain_share": 4500.0,
            "journal_id": 1,
            "non_imputed_share": 15.0,
            "total_price": 47000.0,
            "transaction_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "transaction_reason": "spart part 1",
            "transaction_sens": "Debit",
            "transaction_type": "spartpart",
            "unit_price": 45.0,
            "weight_kg": 234.0
        },
        {
            "cash_amount": 34000.0,
            "fishing_tied": 1,
            "id": 8,
            "imputed_captain_share": 0.0,
            "journal_id": 1,
            "non_imputed_share": 12345.0,
            "total_price": 46780.0,
            "transaction_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "transaction_reason": "Consum 1x",
            "transaction_sens": "Debit",
            "transaction_type": "consumable",
            "unit_price": 20.0,
            "weight_kg": 23.0
        },
        {
            "cash_amount": 13900.0,
            "id": 9,
            "journal_id": 1,
            "transaction_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "transaction_reason": "xxxx",
            "transaction_sens": "Debit",
            "transaction_type": "ordinary"
        },
        {
            "cash_amount": 13900.0,
            "fishing_tied": 1,
            "id": 10,
            "journal_id": 1,
            "transaction_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "transaction_reason": "xxxx",
            "transaction_sens": "Debit",
            "transaction_type": "general"
        }
    ]
}
```

# GET suppliers
return paginated suppliers

```
sample:  curl 'http://127.0.0.1:5000/suppliers?page=1'
    {
    "currentPageContent": [
        {
            "id": 1,
            "name": "Supp 3uiiii"
        }
    ],
    "currentPageNumber": 1,
    "nbrPages": 1,
    "success": true,
    "total": 1
     }
               
```

# DELETE /suppliers/<int:supplier_id>
delete a supplier by providing it ID .

```
sample :  curl -X DELETE http://127.0.0.1:5000/suppliers/1 
```
```
{
    "contentCurrentPage": [],
    "currentPageNumber": 0,
    "deleted": 1,
    "nbrPages": 0,
    "success": true,
    "total": 0
}
```

# POST /suppliers
```
 sample : curl -X POST -H "Content-Type: application/json" -d '{"name":"Ahmed Trading"}' http://127.0.0.1:5000/suppliers
```
```
{
    "created": 3,
    "nbrPages": 1,
    "success": true,
    "suppliers": [
        {
            "id": 3,
            "name": "Supp 3"
        }
    ]
}
```
# PATCH /suppliers
patches a supplier
```
sample : curl -X PATCH -H "Content-Type: application/json" -d '{"id": 3,"name": "Supp 3uiiii"}' http://127.0.0.1:5000//suppliers
```
```
    {
    "created": 3,
    "success": true,
    "supplier": {
        "id": 3,
        "name": "Supp 3uiiii"
    }
}
```

      
# 2. Captains

# GET captains
return paginated captains 

```
sample:  curl 'http://127.0.0.1:5000/captains?page=1'
   {
    "currentPageContent": [
        {
            "bateau": "Bateau hhhhh",
            "id": 2,
            "name": "Mohamed Alouve"
        }
    ],
    "currentPageNumber": 1,
    "nbrPages": 1,
    "success": true,
    "total": 1
}  
```

# DELETE /captains/<int:captain_id>
delete a captain by providing it ID .

```
sample :  curl -X DELETE http://127.0.0.1:5000/captains/2 
```
```
{
    "contentCurrentPage": [],
    "currentPageNumber": 0,
    "deleted": 2,
    "nbrPages": 0,
    "success": true,
    "total": 0
}
```

# POST /captains
```
 sample : curl -X POST -H "Content-Type: application/json" -d ' {"name":"Mohamed Ali","bateau":"Bateau Elvela7"}' http://127.0.0.1:5000/captains
```
```
{
    "captains": [
        {
            "bateau": "Bateau Elvela7",
            "id": 3,
            "name": "Mohamed Ali"
        }
    ],
    "created": 3,
    "nbrPages": 1,
    "success": true,
    "total": 1
}
```
# PATCH /captains
patches a captain
```
sample : curl -X PATCH -H "Content-Type: application/json" -d '{ "bateau": "Bateau Elvela7","id": 3,"name": "Mohamed Ali"}' http://127.0.0.1:5000//captains
```
```
{
    "captain": {
        "bateau": "Bateau Elvela7",
        "id": 3,
        "name": "Mohamed Ali"
    },
    "created": 3,
    "success": true
}
```

# Authors

Mohamed Lehbib Ould Youba

# Acknowledgments

All thanks to Udacity's instructors of this course as well as for technical mentors for helping me during the work on this project.