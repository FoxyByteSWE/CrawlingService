import os, sys
import logging
import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = "foxybyteswe"

def listBuckets():
	s3 = boto3.client('s3')
	response = s3.list_buckets()

	print('Existing buckets:')
	for bucket in response['Buckets']:
		print(f'  {bucket["Name"]}')

def listBucketObjetcs(bucket):
	s3 = boto3.client('s3')
	for key in s3.list_objects(Bucket=bucket)['Contents']:
		print(key['Key'])

def uploadFile(file_name, bucket, object_name=None):
	# If S3 object_name was not specified, use file_name
	if object_name is None:
		object_name = os.path.basename(file_name)

	# Upload the file
	s3 = boto3.client('s3')
	try:
		response = s3.upload_file(file_name, bucket, object_name)
	except ClientError as e:
		logging.error(e)
		return False
	return True

def downloadFile(bucket, object_name, file_name):
	s3 = boto3.client('s3')
	s3.download_file(bucket, object_name, file_name)

def deleteFile(bucket, file_name):
	s3_client = boto3.client('s3')
	response = s3_client.delete_object(
		Bucket = bucket,
		Key = file_name
	)

def main():
	listBuckets()
	listBucketObjetcs(BUCKET_NAME)
	#uploadFile((str(sys.path[0]))+"/data/locationsData.json", BUCKET_NAME)
	#downloadFile(BUCKET_NAME, "locationsData.json", (str(sys.path[0]))+"/data/Downloaded_locationsData.json")
	#deleteFile(BUCKET_NAME, "locationsData.json")

if __name__ == "__main__":
	main()
