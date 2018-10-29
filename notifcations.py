import MySQLdb, sys
from pyfcm import FCMNotification

accountID = str(sys.argv[1])
accountID = int(accountID)
# title = str(sys.argv[2])
# body = str(sys.argv[3])
tag = str(sys.argv[2])
extras = ""

if len(sys.argv) == 4:
    extras = str(sys.argv[3])

def getRelevantDataMessage():
    data_message = ""
    print tag
    if tag == "1":
        data_message = {
            "Title" : "New receipt",
            "Body" : "You received a new receipt from " + extras,
            "Tag" : tag
        }
    elif tag == "2":
        data_message = {
            "Title" : "Sharing request",
            "Body" : extras + " wants to forward a Veno to you",
            "Tag" : tag
        }
    elif tag == "3":
        data_message = {
            "Title" : "Sharing failed :(",
            "Body" : "You tried to send a receipt to unexisting user",
            "Tag" : tag
        }
    print data_message
    return data_message

############################## MAIN ##################################
db=MySQLdb.connect(host="",    # your host, usually localhost
                user="",         # your username
                passwd="",  # your password
                db="")        # name of the data base

# you must create a Cursor object. It will let
# you execute all the queries you need
cur=db.cursor()

# Use all the SQL you like
cur.execute("SELECT Token FROM RegistrationTokens WHERE ID = %s" , (accountID,))

# Push notification
serverKey = ""
push_service = FCMNotification(api_key=serverKey) #if doesnt work - add <> both sides

for row in cur.fetchall():
    # Send to multiple devices by passing a list of ids.
    #message_title = title
    #message_body = body
    result = push_service.notify_single_device(registration_id=row[0], data_message=getRelevantDataMessage())

    print result
db.close()
