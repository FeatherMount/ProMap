import mysql.connector
from mysql.connector import errorcode

def update(data):
    """
    function takes in data, a tuple with pmcId, other authorlist, 
    corrsponding author list with information, and publication date

    it does not return anything but update the database
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

    try:
        # check if the paper already exists in database
        query = "SELECT id FROM papers WHERE pmcid = {}".format(data[0])
        cursor.execute(query)
        if (cursor):
            print('duplicate insertion: rejected')
            return 0
        # process corresponding authors
        # the following id will be used to update 'papers' table
        cAuthorId = 0
        for cAuthor in data[2]:
            # check to see the the author is in the database
            query = "SELECT id FROM authors WHERE name = {}".format(cAuthor['name'])
            cursor.execute(query)
            if (cursor):
                cAuthorId = cursor[0]['id']
                # the author is in the database
                # update the corresponding entry
                # TODO
            else:
                # the author is not in the database
                # insert a new entry
                addAuthor = ("INSERT INTO authors "
                             "(name, email, total_pubication, independence_date) "
                             "VALUES (%s, %s, %s, %s)")
                authorData = (cAuthor['name'], cAuthor['email'], '1', date(data[3]))
                cursor.execute(addAutor, authorData)
                cAuthorId = cursor.lastrowid

        # process other authors
        for otherAuthorName in data[1]:
            # check to see if the author is in the database
            query = "SELECT id FROM authors WHERE name = {}".format(otherAuthorName)
            cursor.execute(query)
            if (cursor):
                # the author is in the database
                # update the corresponding entry
                # TODO
            else:
                # the author is not in the database
                # insert a new entry
                addAuthor = ("INSERT INTO authors  "
                             "(name, total_publication) "
                             "VALUES (%s, %s)")
                authorData = (otherAuthorName, '1')
                cursor.execute(addAuthor, authorData)

        # insert new record to 'papers' table
        addPaper = ("INSERT INTO papers "
                    "(c_author, publication_date, pmcid) "
                    "VALUES (%s, %s, %s)")
        paperData = (cAuthorId, date(data[3]), data[0])
        cursor.execute(addPaper, paperData)
    except mysql.connector.Error as err:
        print(err)
        exit(1)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    update(data)
