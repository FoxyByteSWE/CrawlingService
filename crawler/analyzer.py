import os, sys
import logging
import boto3
from botocore.exceptions import ClientError

def analyzeText():
	client = boto3.client('comprehend')
	text = "Molto bello!"
	response = client.detect_sentiment(
		Text = text,
		LanguageCode = 'it'
	)
	response = parseResponse(response)
	print(response)

def parseResponse(response):
	dict = {}
	dict["Sentiment"] = response["Sentiment"]
	dict["Positive"] = response["SentimentScore"]["Positive"]
	dict["Negative"] = response["SentimentScore"]["Negative"]
	dict["Neutral"] = response["SentimentScore"]["Neutral"]
	dict["Mixed"] = response["SentimentScore"]["Mixed"]
	return dict

def main():
	analyzeText()

if __name__ == "__main__":
	main()
