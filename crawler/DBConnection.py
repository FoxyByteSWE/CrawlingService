# standard packages
import sys, os
import mysql.connector
from mysql.connector import Error
import pandas as pd

# packages written as part of the project
from S3Connection import S3Connection

sys.path.insert(1, (str(sys.path[0]))+"/../IGCrawlerService/crawler/")

from media.FoxyByteMedia import FoxyByteMedia
from location.Location import Location

# S3 bucket name
BUCKET_NAME = "foxybyteswe"

class DBConnection:

	def __init__(self, hostname = "localhost", user = "root", password = "root", server_connection = None, database_connection = None, s3 = None):
		self.hostname = hostname
		self.user = user
		self.password = password
		self.server_connection = server_connection
		self.database_connection = database_connection
		self.s3 = s3

	def createServerConnection(self, host_name = None, user_name = None, user_password = None):

		if host_name is None:
			host_name = self.hostname

		if user_name is None:
			user_name = self.user

		if user_password is None:
			user_password = self.password

		connection = None
		try:
			connection = mysql.connector.connect(
				host=host_name,
				user=user_name,
				passwd=user_password
			)
			print("Successfully connected to MySQL server")
		except Error as err:
			print(f"Error: '{err}'")

		self.server_connection = connection
		return connection

	def createDatabase(self, name, connection = None):

		if connection is None:
			connection = self.server_connection

		cursor = connection.cursor(buffered=True)

		"""
		query = "DROP DATABASE IF EXISTS " + name + ";"
		try:
			cursor.execute(query)
			print("Successfully dropped database " + name)
		except Error as err:
			print(f"Error: '{err}'")
		"""

		query = "CREATE DATABASE IF NOT EXISTS " + name + ";"
		try:
			cursor.execute(query)
			print("Successfully created database " + name)
		except Error as err:
			print(f"Error: '{err}'")

	def createDatabaseConnection(self, db_name, host_name = None, user_name = None, user_password = None):

		if host_name is None:
			host_name = self.hostname

		if user_name is None:
			user_name = self.user

		if user_password is None:
			user_password = self.password

		connection = None
		try:
			connection = mysql.connector.connect(
				host=host_name,
				user=user_name,
				passwd=user_password,
				database=db_name
			)
			print("Successfully connected to database " + db_name)
		except Error as err:
			print(f"Error: '{err}'")

		self.database_connection = connection
		return connection

	def executeQuery(self, query, connection = None):

		if connection is None:
			connection = self.database_connection

		cursor = connection.cursor(buffered=True)
		try:
			cursor.execute(query)
			connection.commit()
			print("Successfully executed " + query)
			#print("\nResult:")
			#result = cursor.fetchall();
			#for row in result:
				#print(row)
		except Error as err:
			print(f"Error: '{err}'")

	def insertRestaurants(self, restaurants, connection = None):

		if connection is None:
			connection = self.database_connection

		drop_restaurants = "DROP TABLE IF EXISTS restaurants;"

		create_restaurants = """CREATE TABLE IF NOT EXISTS restaurants(
			Codice_pk VARCHAR(20) PRIMARY KEY,
			Nome VARCHAR(50) NOT NULL,
			Categoria  VARCHAR(20),
			Indirizzo VARCHAR(150),
			Sito VARCHAR(70),
			Telefono VARCHAR(16),
			Immagine VARCHAR(1500),
			Longitudine FLOAT,
			Latitudine FLOAT,
			Ranking FLOAT
		)"""

		self.executeQuery(drop_restaurants)

		self.executeQuery(create_restaurants)

		for r in restaurants:
			#print(r.pk)
			#print(r.name)
			#r.printRanking()
			#print('\n')
			pk = '"' + str(r.pk) + '", '
			if pk == '""' or pk == '"None", ':
				pk = 'NULL, '
			name = str(r.name)
			name = name.replace('"', "'")
			name = '"' + name + '", '
			if name == '""' or name == '"None", ':
				name = 'NULL, '
			category = '"' + str(r.category) + '", '
			if category == '""' or category == '"None", ':
				category = 'NULL, '
			address = '"' + str(r.address) + '", '
			#print(address)
			if address == '""' or address == '"None", ':
				address = 'NULL, '
			website = '"' + str(r.website) + '", '
			if website == '""' or website == '"None", ':
				website = 'NULL, '
			phone = '"' + str(r.phone) + '", '
			if phone == '""' or phone == '"None", ':
				phone = 'NULL, '
			main_image_url = '"' + str(r.main_image_url) + '", '
			if main_image_url == '""' or main_image_url == '"None", ':
				main_image_url = 'NULL, '
			lng = '"' + str(r.coordinates[0]) + '", '
			if lng == '""' or lng == '"None", ':
				lng = 'NULL, '
			lat = '"' + str(r.coordinates[1]) + '", '
			if lat == '""' or lat == '"None", ':
				lat = 'NULL, '
			ranking = '"' + str(r.returnFormattedRanking()) + '"'
			if ranking == '""' or ranking == '"None", ':
				ranking = 'NULL, '

			insert_restaurant = "INSERT INTO restaurants VALUES (" + pk + name + category + address + website + phone + main_image_url + lng + lat + ranking + ');'
			#print(insert_restaurant)
			self.executeQuery(insert_restaurant)


	def insertUser(self, parameter):
        #TODO: implement
		pass

	def insertMedia(self, parameter):
        #TODO: implement
		pass

	def createS3Connection(self):
		self.s3 = S3Connection(BUCKET_NAME)

	def uploadDB(self, db, fileDirectory = None):

		if fileDirectory is None:
			fileDirectory = str(sys.path[0]) + "/"

		self.createS3Connection()
		command = 'mysqldump -u "root" -proot "' + db + '" > '  + fileDirectory + db + '_database.sql'
		os.system(command)
		file = fileDirectory + db + "_database.sql"
		self.s3.uploadFile(file)

	def downloadDB(self, db, fileDirectory = None):

		if fileDirectory is None:
			fileDirectory = str(sys.path[0]) + "/"

		self.createS3Connection()
		object = db + "_database.sql"
		file = fileDirectory + db + "_database.sql"
		self.s3.downloadFile(object, file)
		self.createServerConnection()
		self.createDatabase(db)
		command = 'mysql -u root -proot ' + db + ' < ' + fileDirectory + db + '_database.sql'
		os.system(command)

def main():

	db = DBConnection()

	#db.createServerConnection()
	#db.createDatabase("michelinsocial")

	#db.createDatabaseConnection("michelinsocial")
	#db.insertRestaurants()

	#db.uploadDB("michelinsocial")
	#db.downloadDB("michelinsocial")

if __name__ == "__main__":
	main()