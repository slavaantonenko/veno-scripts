import sys, os
import google.cloud.storage

sourceFile = str(sys.argv[1]) # Current input - full file path.

# Create a storage client.
storageClient = google.cloud.storage.Client()

# TODO (Developer): Replace this with your Cloud Storage bucket name.
bucketName = ''
bucket = storageClient.get_bucket(bucketName)

# TODO (Developer): Replace this with the name of the local file to upload.
blob = bucket.blob('Stores-Logos/' + os.path.basename(sourceFile))

# Upload the local file to Cloud Storage.
blob.upload_from_filename(sourceFile)

print('File {} uploaded to {}.'.format(sourceFile, bucket))