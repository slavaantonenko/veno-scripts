import MySQLdb, sys
from pyfcm import FCMNotification

phoneNumberFrom = str(sys.argv[1])
phoneNumberTo = str(sys.argv[2])
senderFirstName = ""
senderLastName = ""

db=MySQLdb.connect(host="",    # your host, usually localhost
                user="",         # your username
                passwd="",  # your password
                db="")        # name of the data base

# you must create a Cursor object. It will let
# you execute all the queries you need
cur=db.cursor()

cur.execute("SELECT Notifications FROM AccountInfo WHERE ID = (SELECT ID FROM Accounts WHERE PhoneNumber = %s)" , (phoneNumberInput,))

if (cur.fetchone()[0]):
    cur.execute("SELECT FirstName, LastName FROM AccountInfo WHERE ID = (SELECT ID FROM Accounts WHERE PhoneNumber = %s)" , (phoneNumberFrom,))
    result = cur.fetchone()
    senderFirstName = result[0]
    senderLastName = result[1]

    # Get all device's token which using this phone number. 
    cur.execute("SELECT Token FROM RegistrationTokens WHERE ID = (SELECT ID FROM Accounts WHERE PhoneNumber = %s)" , (phoneNumberTo,))

    # Push notification
    serverKey = ""
    push_service=FCMNotification(api_key=serverKey) #if doesnt work - add <> both sides

    for row in cur.fetchall():

        # Send to multiple devices by passing a list of ids.
        message_title = "Sharing request"
        message_body = senderFirstName + " " + senderLastName + " wants to share a veno with you"

        result = push_service.notify_single_device(registration_id=row[0], message_title=message_title, message_body=message_body, tag="Share")
        print result

    db.close()