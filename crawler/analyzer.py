import os, sys
import logging
import boto3
from botocore.exceptions import ClientError

def analyzeText(text):
	client = boto3.client('comprehend')
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
	analyzeText("Molto bello!")

if __name__ == "__main__":
	main()
