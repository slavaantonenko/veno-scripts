import google.cloud.storage, sys

id = str(sys.argv[1])
sourceFile = str(sys.argv[2])
date = str(sys.argv[3])
store_type = str(sys.argv[4])

# Create a storage client.
storageClient = google.cloud.storage.Client()

# TODO (Developer): Replace this with your Cloud Storage bucket name.
bucketName = ''
bucket = storageClient.get_bucket(bucketName)

# TODO (Developer): Replace this with the name of the local file to upload.
sourceBlob = bucket.blob('Demo-Receipts/' + store_type + '/' + sourceFile + '.pdf')

destinationBlob = id + '/' + sourceFile + '-' + date + '.pdf'

bucket.copy_blob(sourceBlob, bucket ,destinationBlob)

print('Blob {} in bucket {} created in blob {}.'.format(sourceBlob.name, bucketName, destinationBlob))