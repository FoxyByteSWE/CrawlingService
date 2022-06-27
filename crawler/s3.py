import os, sys
import logging
import boto3
from botocore.exceptions import ClientError

KEY_ID = "AKIARMTOPHZNJLHKG34W"
ACCESS_KEY = "InRFYCONYUELaWnhdkoh9lP9ybM63Fef0r50vjBt"

def listBuckets():
	s3 = boto3.client('s3')
	response = s3.list_buckets()

	print('Existing buckets:')
	for bucket in response['Buckets']:
		print(f'  {bucket["Name"]}')

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


def main():
	listBuckets()
	#uploadFile((str(sys.path[0]))+"/data/locationsData.json", "foxybyteswe")
	downloadFile("foxybyteswe", "locationsData.json", (str(sys.path[0]))+"/data/Downloaded_locationsData.json")

if __name__ == "__main__":
	main()
