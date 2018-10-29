import MySQLdb, sys, os
import google.cloud.storage

phoneNumberInput = str(sys.argv[1]) # Number with + at the beginning.
sourceFile = str(sys.argv[2]) # Current input - full file path.

if (len(phoneNumberInput) <= 20 and phoneNumberInput[0] == '+' and phoneNumberInput[1:].isdigit()):
  db=MySQLdb.connect(host="",    # your host, usually localhost
                    user="",         # your username
                    passwd="",  # your password
                    db="")        # name of the data base

  # you must create a Cursor object. It will let
  # you execute all the queries you need
  cur=db.cursor()

  cur.execute("SELECT ID FROM Accounts WHERE PhoneNumber = %s" , (phoneNumberInput,))

  id = str(cur.fetchone()[0])

  # Create a storage client.
  storageClient = google.cloud.storage.Client()

  # TODO (Developer): Replace this with your Cloud Storage bucket name.
  bucketName = ''
  bucket = storageClient.get_bucket(bucketName)

  # TODO (Developer): Replace this with the name of the local file to upload.
  blob = bucket.blob(id + '/' + os.path.basename(sourceFile))

  # Upload the local file to Cloud Storage.
  blob.upload_from_filename(sourceFile)

  print('File {} uploaded to {}.'.format(sourceFile, bucket))

  db.close()