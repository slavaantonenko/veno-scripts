import MySQLdb, sys
id = str(sys.argv[1])
listFiles = str(sys.argv[2]).split(',')
status = str(sys.argv[3])
db=MySQLdb.connect(host="",    # your host, usually localhost
                  user="",         # your username
                  passwd="",  # your password
                  db="")        # name of the data base
# you must create a Cursor object. It will let
# you execute all the queries you need
cur=db.cursor()

for fileName in listFiles[:-1]:
  cur.execute("UPDATE Receipts SET IsFavourite = %s WHERE Name = %s AND UserID = %s" , (status, fileName, id,))
  db.commit()

db.close()