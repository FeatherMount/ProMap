import mysql.connector
from mysql.connector import errorcode
from datetime import date

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
        row = cursor.fetchone()
        if (row != None):
            print('duplicate insertion: rejected')
            return 0
        # process corresponding authors
        # the following id will be used to update 'papers' table
        cAuthorId = 0
        for cAuthor in data[2]:
            # check to see the the author is in the database
            query = ("SELECT id, independence_date "
                     "FROM authors "
                     "WHERE name = %s")
            queryData = (cAuthor[0],)
            cursor.execute(query, queryData)
            row = cursor.fetchone()
            if (row != None):
                cAuthorId = row['id']
                # the author is in the database
                # update the corresponding entry
                if (date(cursor[0]['independence_date']) < date(data[3])):
                    earlierDate = date(cursor[0]['independence_date'])
                else:
                    earlierDate = date(data[3])
                updateAuthor = ("UPDATE authors "
                                "SET total_publication = total_publication + 1, independence_date = %s "
                                "WHERE  id = %s")
                authorData = (earlierDate, cAuthorId)
                cursor.execute(upDateAuthor, authorData)
            else:
                # the author is not in the database
                # insert a new entry
                addAuthor = ("INSERT INTO authors "
                             "(name, email, total_publication, independence_date) "
                             "VALUES (%s, %s, %s, %s)")
                
                authorData = (cAuthor[0], cAuthor[1], 1, date(int(data[3][0]), \
                int(data[3][1]), int(data[3][2])))
                cursor.execute(addAuthor, authorData)
                cAuthorId = cursor.lastrowid

        # process other authors
        for otherAuthorName in data[1]:
            # check to see if the author is in the database
            query = ("SELECT id FROM authors WHERE name = %s")
            queryData = (otherAuthorName,)
            cursor.execute(query, queryData)
            row = cursor.fetchone()
            if (row != None):
                otherAuthorId = cursor[0]['id']
                # the author is in the database
                # update the corresponding entry
                updateAuthor = ("UPDATE authors "
                                "SET total_publication = total_publication + 1 "
                                "WHERE id = %s")
                authorData = (otherAuthorId,)
                cursor.execute(updateAuthor, authorData)
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
    data = (1, ['zhou zhou'], [('zhou zhou', 'zz2181@columbia.edu')], ('2014', '1', '1')) 
    update(data)
