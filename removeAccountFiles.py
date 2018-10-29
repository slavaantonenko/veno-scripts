import os
import sys
import MySQLdb

id = str(sys.argv[1])
listFiles = str(sys.argv[2]).split(',')

db=MySQLdb.connect(host="",    # your host, usually localhost
                  user="",         # your username
                  passwd="",  # your password
                  db="")        # name of the data base
# you must create a Cursor object. It will let
# you execute all the queries you need
cur=db.cursor()

for root, dirs, files in os.walk('/receipts/' + id):
    for file in files:
        if file in listFiles[:-1]:
            os.remove(root + "/" + file)
            cur.execute("call removeReceipts(%s, %s)", (id, file,))
            db.commit()

db.close()