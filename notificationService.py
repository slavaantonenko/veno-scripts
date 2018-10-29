import MySQLdb, sys
from pyfcm import FCMNotification

phoneNumberInput = str(sys.argv[1])

if (len(phoneNumberInput) <= 20 and phoneNumberInput[0] == '+' and phoneNumberInput[1:].isdigit()):
  db=MySQLdb.connect(host="",    # your host, usually localhost
                    user="",         # your username
                    passwd="",  # your password
                    db="")        # name of the data base

  # you must create a Cursor object. It will let
  # you execute all the queries you need
  cur=db.cursor()

  cur.execute("SELECT Notifications FROM AccountInfo WHERE ID = (SELECT ID FROM Accounts WHERE PhoneNumber = %s)" , (phoneNumberInput,))

  if (cur.fetchone()[0]):
    # Use all the SQL you like
    cur.execute("SELECT Token FROM RegistrationTokens WHERE ID = (SELECT ID FROM Accounts WHERE PhoneNumber = %s)" , (phoneNumberInput,))

    # Push notification
    serverKey = ""
    push_service=FCMNotification(api_key=serverKey) #if doesnt work - add <> both sides

    for row in cur.fetchall():
      # Send to multiple devices by passing a list of ids.
      message_title="new receipt"
      message_body="Hope you're having fun this weekend, don't forget to check today's news"
      #result = push_service.notify_multiple_devices(registration_ids = tokens, message_title = message_title, message_body = message_body)
      result=push_service.notify_single_device(registration_id=row[0], message_title=message_title, message_body=message_body)


      print result
  db.close()