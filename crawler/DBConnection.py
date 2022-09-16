import logging
import pymysql

from pprint import pprint
class DBConnection:

	#def __init__(self, hostname = "michelinsocial.ctr0m4f2rgau.eu-west-1.rds.amazonaws.com", user = "admin", password = "#g7ct=MD", server_connection = None, database_connection = None):
	def __init__(self, hostname = "localhost", user = "root", password = "root", server_connection = None, database_connection = None):
		self.hostname = hostname
		self.user = user
		self.password = password
		self.server_connection = server_connection
		self.database_connection = database_connection

	def createServerConnection(self, host_name = None, user_name = None, user_password = None):

		if host_name is None:
			host_name = self.hostname

		if user_name is None:
			user_name = self.user

		if user_password is None:
			user_password = self.password

		connection = None
		try:
			connection = pymysql.connect(
				host = host_name,
				user = user_name,
				passwd = user_password
			)
			print("Successfully connected to MySQL server")
		except pymysql.Error as err:
			print(f"Error: '{err}'")

		self.server_connection = connection
		return connection

	def createDatabase(self, name, connection = None):

		if connection is None:
			connection = self.server_connection

		cursor = connection.cursor()

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
			connection.commit()
			print("Successfully created database " + name)
		except pymysql.Error as err:
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
			connection = pymysql.connect(
				host = host_name,
				user = user_name,
				passwd = user_password,
				database = db_name
			)
			print("Successfully connected to database " + db_name)
		except pymysql.Error as err:
			print(f"Error: '{err}'")

		self.database_connection = connection
		return connection

	def executeQuery(self, query, connection = None):

		if connection is None:
			connection = self.database_connection

		cursor = connection.cursor()
		try:
			cursor.execute(query)
			connection.commit()
			print("Successfully executed " + query)
			print("\nResult:")
			result = cursor.fetchall();
			for row in result:
				print(row)
		except pymysql.Error as err:
			print(f"Error: '{err}'")

	
	def insertItem(self, item: dict, table: str):

		for k,v in item.items():
			item[k] = str(item[k])
			item[k] = item[k].replace('"', "'")
			item[k] = '"' + item[k] + '"'
			if item[k] == '""' or item[k] == '"None"':
				item[k] = '"NULL"'

		placeholders = ', '.join(item.values())
		columns = ', '.join(item.keys())
		sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table, columns, placeholders)
		print(sql)
		self.executeQuery(sql)


	def removeUser(self, item: dict):
		sql = "DELETE FROM users WHERE pk == " + item['pk']
		self.executeQuery(sql)

	def readItem(self, query:str):
			connection = self.database_connection
			desc = connection.cursor()
			desc.execute(query)
			connection.commit()

			list = []
			for row in desc.fetchall():
				dict = {}
				for i in range(len(desc.description)):
					dict[desc.description[i][0]] = row[i]
				list.append(dict)

			print(list)

			#pprint(vars(desc))

db = DBConnection()
db.createServerConnection()
db.createDatabaseConnection("michelinsocial")
dict = {'Categoria': 'CIAO',
  'Codice_pk': '000000',
  'Immagine': '',
  'Indirizzo': 'VIA"CIAO',
  'Latitudine': 11.1111,
  'Longitudine': 22.2222,
  'Nome': 'Farina del TUO sacco',
  'Ranking': 10,
  'Sito': 'https://www.farinadelmiosaccoferrara.it',
  'Telefono': '0532474303'}
db.insertItem(dict, "restaurants")
