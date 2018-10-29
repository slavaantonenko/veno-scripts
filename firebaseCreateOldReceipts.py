from random import randint
import google.cloud.storage, sys
import MySQLdb

idTo = str(sys.argv[1])

db = MySQLdb.connect(host="",    # your host, usually localhost
                  user="",         # your username
                  passwd="",  # your password
                  db="")        # name of the data base
cur = db.cursor()
cur.execute("SELECT * FROM Receipts WHERE UserID=%s;" , (idTo,))
data = [dict((cur.description[idx][0], value) for idx, value in enumerate(row)) for row in cur.fetchall()]

# Create a storage client.
storageClient = google.cloud.storage.Client()

# TODO (Developer): Replace this with your Cloud Storage bucket name.
bucketName = ''
bucket = storageClient.get_bucket(bucketName)

for row in data:
    # TODO (Developer): Replace this with the name of the local file to upload.
    sourceBlob = bucket.blob('Demo-Receipts/' + str(randint(1, 2)) + '/' + row['StoreName'] + '.pdf')
    destinationBlob = idTo + '/' + row['Name']

    bucket.copy_blob(sourceBlob, bucket ,destinationBlob)

    print('Blob {} in bucket {} copied to blob {}.'.format(sourceBlob.name, bucketName, destinationBlob))