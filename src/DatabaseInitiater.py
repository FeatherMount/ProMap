import os
import mysql.connector
from mysql.connector import errorcode
from datetime import date

import NXMLParser
import DatabaseUpdater

def main():
	"""
	This is the wrapper function, it does not take arguments. 
	It calls NXMLParser.parse first then DatabaseUpdater.update 
	"""
	
	try:
	    conn = mysql.connector.connect(user = 'root', password = 'love',
	                               host = '127.0.0.1',
	                               database = 'promap')
	except mysql.connector.Error as err:
	    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
	        print("password and name pair incorrect")
	    elif err.errno == errorcode.ER_BAD_DB_ERROR:
	        print("no such database")
	    else:
	        print(err)
	        exit(1)

	# obtain connection cursor
	cursor = conn.cursor()
	i = 0
	# walk through all the files
	rootDirectory = 'C:/Users/Zhou/Downloads/ProMap_Data/articles.C-H'
	for aDir, theSubdirs, theFiles in os.walk(rootDirectory):
		
		for aFile in theFiles:
			filename = os.path.join(aDir, aFile)
			print(aFile)
			data = NXMLParser.parse(filename)
			if (data[0] == -1): 
				i = i + 1
				print(i)
				continue
			DatabaseUpdater.update(cursor, data)
			conn.commit()

	cursor.close()
	conn.close()

if __name__ == '__main__':
	main()