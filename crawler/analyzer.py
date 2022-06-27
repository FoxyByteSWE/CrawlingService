import os, sys
from s3 import uploadFile, deleteFile
import urllib.request
import logging
import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = "foxybyteswe"

def analyzeText(text):
	client = boto3.client('comprehend')
	response = client.detect_sentiment(
		Text = text,
		LanguageCode = 'it'
	)
	response = parseTextResponse(response)
	print(response)

def parseTextResponse(response):
	dict = {}
	dict["Sentiment"] = response["Sentiment"]
	dict["Positive"] = response["SentimentScore"]["Positive"]
	dict["Negative"] = response["SentimentScore"]["Negative"]
	dict["Neutral"] = response["SentimentScore"]["Neutral"]
	dict["Mixed"] = response["SentimentScore"]["Mixed"]
	return dict

def detectLabels(url):
	urllib.request.urlretrieve(url, "tmp_image.jpg")

	uploadFile("tmp_image.jpg", BUCKET_NAME)

	client = boto3.client('rekognition')
	response = client.detect_labels(
    Image = {
        'S3Object': {
            'Bucket': BUCKET_NAME,
            'Name': 'tmp_image.jpg',
        },
    },
    MaxLabels = 5,
    MinConfidence = 0.5
	)
	deleteFile(BUCKET_NAME, "tmp_image.jpg")
	os.remove("tmp_image.jpg")
	print(response)

def main():
	analyzeText("Molto bello!")
	detectLabels("https://instagram.ffco2-1.fna.fbcdn.net/v/t51.2885-15/11249882_966261376755731_963030927_n.jpg?se=8&stp=dst-jpg_e35&_nc_ht=instagram.ffco2-1.fna.fbcdn.net&_nc_cat=111&_nc_ohc=9lNYboVO5K0AX90TSMu&edm=AKmAybEBAAAA&ccb=7-5&ig_cache_key=MTIyOTEzNTQ0NTAwMDU1ODY0Mg%3D%3D.2-ccb7-5&oh=00_AT-H5SGET-X6zx_j-GGayPMijixUZwQOB6Ssy4c_gdtQSQ&oe=62BFFD3D&_nc_sid=bcb96")

if __name__ == "__main__":
	main()
