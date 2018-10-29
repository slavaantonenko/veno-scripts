import google.cloud.storage, sys

idFrom = str(sys.argv[1])
idTo = str(sys.argv[2])
sourceFile = str(sys.argv[3])

# Create a storage client.
storageClient = google.cloud.storage.Client()

# TODO (Developer): Replace this with your Cloud Storage bucket name.
bucketName = ''
bucket = storageClient.get_bucket(bucketName)

# TODO (Developer): Replace this with the name of the local file to upload.
sourceBlob = bucket.blob(idFrom + '/' + sourceFile)
# destinationBlob = bucket.blob(idTo + '/' + sourceFile)
destinationBlob = idTo + '/' + sourceFile

bucket.copy_blob(sourceBlob, bucket ,destinationBlob)

print('Blob {} in bucket {} copied to blob {}.'.format(sourceBlob.name, bucketName, destinationBlob))