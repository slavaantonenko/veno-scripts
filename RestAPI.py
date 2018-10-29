from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask import jsonify

import logging
import json
import MySQLdb
import datetime
from subprocess import call

app = Flask(__name__)
api = Api(app)

class NewReceipt(Resource):
    def get(self, phone_number, store_name, store_type):
        dateTimeNow = datetime.datetime.now()
        createdDate = dateTimeNow.strftime("%d-%m-%Y %H:%M:%S")
        formatedCreatedDate = dateTimeNow.strftime("%d%m%y%H%M%S")

        params = [phone_number, createdDate, formatedCreatedDate, store_name]
        result = Utils().dbConnection("insertReceipts", params, True)

        call(["python", "/scripts/firebaseNewReceipt.py", str(result[0]), store_name, formatedCreatedDate, str(store_type)])

        tag = "1"
        call(["python", "/scripts/notifications.py", str(result[0]), tag, store_name])

class UpdateAccountInfo(Resource):
    def get(self, account_id, first_name, last_name, update):
        params = [account_id, first_name, last_name, Utils().convertStringToBool(update)]
        Utils().dbConnection("updateAccountInfo", params, False)

class GenerateVerificationCode(Resource):
    def get(self, phone_number):
        params = [phone_number]
        result = Utils().dbConnection("verificationCodeGenerator", params, True)

        return result

class ValidateVerificationCode(Resource):
    def get(self, phone_number, verify_code):
        params = [phone_number, verify_code, 0]
        result = Utils().dbConnection("verificationCodeValidation", params, True)

        return result

class CheckIfAccountExist(Resource):
    def get(self, new_number):
        params = [new_number, None]
        result = Utils().dbConnection("checkAccountExist", params, True)

        return result

class CreateAccount(Resource):
    def get(self, phone_number):
        db = MySQLdb.connect(host="",    # your host, usually localhost
            user="",         # your username
            passwd="",  # your password
            db="")        # name of the data base
        cur = db.cursor()
        cur.callproc("createAccount", (phone_number, 0, None, "", ""))
        data = [dict((cur.description[idx][0], value) for idx, value in enumerate(row)) for row in cur.fetchall()]
        cur.close()
        db.commit()
        db.close()

        return jsonify(data)

class DeleteAccount(Resource):
    def get(self, account_id):
        params = [account_id]
        Utils().dbConnection("deleteAccount", params, False)

class RegisterToken(Resource):
    def get(self, account_id, token):
        params = [account_id, token]
        Utils().dbConnection("registerToken", params, False)

class ChangeNumber(Resource):
    def get(self, new_number, account_id):
        params = [new_number, account_id]
        Utils().dbConnection("changeNumber", params, False)

class GetNewReceipts(Resource):
    def get(self, account_id, date):
        db = MySQLdb.connect(host="localhost",    # your host, usually localhost
            user="",         # your username
            passwd="",  # your password
            db="")        # name of the data base
        cur = db.cursor()
        cur.callproc("getAccountReceipts", (account_id, date))
        data = [dict((cur.description[idx][0], value) for idx, value in enumerate(row)) for row in cur.fetchall()]
        db.close()

        return jsonify(data)

class ManageFavourites(Resource):
    def get(self, account_id, receipt_name, is_favourite):
        params = [account_id, receipt_name, Utils().convertStringToBool(is_favourite)]
        Utils().dbConnection("manageFavourites", params, False)

class RemoveReceipts(Resource):
    def get(self, account_id, receipt_name):
        params = [account_id, receipt_name]
        Utils().dbConnection("removeReceipts", params, False)

class RequestForwardReceipts(Resource):
    def get(self, receipt_name, id_from, phone_number_to):
        targetAccountExist = None
        db = MySQLdb.connect(host="",    # your host, usually localhost
                  user="",         # your username
                  passwd="",  # your password
                  db="")        # name of the data base

        # you must create a Cursor object. It will let
        # you execute all the queries you need
        cur = db.cursor()
        cur.callproc("checkAccountExist", (phone_number_to, targetAccountExist))

        if (cur.fetchone()[0]):
            requestAlreadyExist = None
            cur.close()
            cur = db.cursor()
            cur.callproc("addRequestedForwardReceipt", (id_from, receipt_name, phone_number_to, requestAlreadyExist, "", ""))
            result = cur.fetchone()

            # If false, this is a new request.
            if not (result[0]):
                cur.close()
                db.commit()

                # Send a forward request notification.
                senderFirstName = result[1]
                senderLastName = result[2]

                cur = db.cursor()
                cur.execute("SELECT ID FROM Accounts WHERE PhoneNumber=%s" , (phone_number_to,))
                idTo = cur.fetchone()[0]
                cur.close()

                tag = "2"
                extras = senderFirstName + " " + senderLastName
                call(["python", "/scripts/notifications.py", str(idTo), tag, extras])
        else:
            # Send sender notification that the desired account doesn't exist.
            tag = "3"
            call(["python", "/scripts/notifications.py", id_from, tag])

        db.close()

class ApproveForwardRequest(Resource):
    def get(self, receipt_name, id_from, id_to):
        call(["python", "/scripts/firebaseCopyFile.py", id_from, id_to, receipt_name])

        params = [id_to, id_from, receipt_name, True]
        Utils().dbConnection("moveFromPSToReceipts", params, False)

class DeclineForwardRequest(Resource):
    def get(self, receipt_name, id_from, id_to):
        params = [id_to, id_from, receipt_name, False]
        Utils().dbConnection("moveFromPSToReceipts", params, False)

class GetRequestedForwards(Resource):
    def get(self, id_to):
        db = MySQLdb.connect(host="",    # your host, usually localhost
                  user="",         # your username
                  passwd="",  # your password
                  db="")        # name of the data base

        # you must create a Cursor object. It will let
        # you execute all the queries you need
        cur = db.cursor()
        cur.execute("SELECT * FROM RequestedForwards WHERE UserID=%s;" , (id_to,))
        data = [dict((cur.description[idx][0], value) for idx, value in enumerate(row)) for row in cur.fetchall()]
        return jsonify(data)

class Utils(object):
    def dbConnection(self, spName, params, needResult):
    # def dbConnection(self):
        db = MySQLdb.connect(host="",    # your host, usually localhost
                  user="",         # your username
                  passwd="",  # your password
                  db="")        # name of the data base
        cur = db.cursor()
        cur.callproc(spName, params)

        if needResult:
            result = cur.fetchone()
            cur.close()
            db.commit()
            db.close()
            return result
        else:
            cur.close()
            db.commit()
            db.close()

    def convertStringToBool(self, string):
        return string.lower() in ['true', '1']


api.add_resource(NewReceipt, '/NewReceipt/<phone_number>/<store_name>/<store_type>')
api.add_resource(UpdateAccountInfo, '/UpdateAccountInfo/<account_id>/<first_name>/<last_name>/<update>')
api.add_resource(GenerateVerificationCode, '/GenerateVerificationCode/<phone_number>')
api.add_resource(ValidateVerificationCode, '/ValidateVerificationCode/<phone_number>/<verify_code>')
api.add_resource(CheckIfAccountExist, '/CheckIfAccountExist/<new_number>')
api.add_resource(CreateAccount, '/CreateAccount/<phone_number>')
api.add_resource(DeleteAccount, '/DeleteAccount/<account_id>')
api.add_resource(RegisterToken, '/RegisterToken/<account_id>/<token>')
api.add_resource(ChangeNumber, '/ChangeNumber/<new_number>/<account_id>')
api.add_resource(RequestForwardReceipts, '/RequestForward/<receipt_name>/<id_from>/<phone_number_to>')
api.add_resource(ApproveForwardRequest, '/ApproveForwardRequest/<receipt_name>/<id_from>/<id_to>')
api.add_resource(DeclineForwardRequest, '/DeclineForwardRequest/<receipt_name>/<id_from>/<id_to>')
api.add_resource(GetRequestedForwards, '/GetRequestedForwards/<id_to>')
api.add_resource(GetNewReceipts, '/GetNewReceipts/<account_id>/<date>')
api.add_resource(ManageFavourites, '/ManageFavourites/<account_id>/<receipt_name>/<is_favourite>')
api.add_resource(RemoveReceipts, '/RemoveReceipts/<account_id>/<receipt_name>')

if __name__ == '__main__':
    app.debug = True
    logging.basicConfig(filename='/var/www/restapi/api.log',level=logging.DEBUG)
    app.run(host='0.0.0.0', port='')
