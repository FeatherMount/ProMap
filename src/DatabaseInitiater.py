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
	                               database = 'ProMap')
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

	# TODO 
	filename = '../resource/Cancer_Biol_Med_2012_Jun_9(2)_85-89.nxml'
	data = NXMLParser.parse(filename)
	DatabaseUpdater.update(cursor, data)

	conn.commit()
	cursor.close()
	conn.close()

if __name__ == '__main__':
	main()