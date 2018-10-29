# python /scripts/copyFilesFromExisted.py "file name" new/old days/months "number of receipts to create" id "store name" "category"

from subprocess import call
from dateutil.relativedelta import relativedelta
from datetime import datetime
import time
import MySQLdb, sys, os

file = str(sys.argv[1])
operation = str(sys.argv[2])
delta = str(sys.argv[3])
number_of_files = int(str(sys.argv[4]))
id = int(str(sys.argv[5]))
store_name = str(sys.argv[6])
category = str(sys.argv[7])
file_name = file.split('-')[0]

db=MySQLdb.connect(host="",    # your host, usually localhost
                  user="",         # your username
                  passwd="",  # your password
                  db="")        # name of the data base
# you must create a Cursor object. It will let
# you execute all the queries you need
cur=db.cursor()

for i in range(0, number_of_files + 1):
    if i != 0:
        filedate = datetime.utcfromtimestamp(os.path.getmtime(file))

        if delta == 'months':
            if operation == 'new':
                end_date = filedate + relativedelta(months=i)
            elif operation == 'old':
                end_date = filedate - relativedelta(months=i)
        elif delta == 'days':
            if operation == 'new':
                end_date = filedate + relativedelta(days=i)
            elif operation == 'old':
                end_date = filedate - relativedelta(days=i)

        end_date_string = end_date.strftime('%d%m%y%H%M')
        print end_date_string
        full_file = file_name + "-" + end_date_string + ".pdf"
        print full_file
        call(["cp", os.getcwd() + "/" + file, os.getcwd() + "/" + full_file])
        call(["touch", "-t", end_date.strftime('%Y%m%d%H%M'), os.getcwd() + "/" + full_file])

        db_time = end_date.strftime('%d-%m-%Y %H:%M:%S')
        cur.execute("call insertReceipts(%s, %s, %s, %s, %s)", (id, full_file, db_time, store_name, category,))
        db.commit()

        # Upload to Firebase
        cur.execute("SELECT PhoneNumber FROM Accounts WHERE ID = %s" , (id,))
        phoneNumber = str(cur.fetchone()[0])

        command = 'python firebaseCloudStorageUpload.py ' + phoneNumber  + ' /receipts/' + id + '/' + full_file 
        os.system(command)
db.close()