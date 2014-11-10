import mysql.connector
from mysql.connector import errorcode
from datetime import date

def update(cursor, data):
    """
    function takes in data, a tuple with pmcId, other authorlist, 
    corrsponding author list with information, and publication date

    function also takes in mysql cursor from the caller

    it does not return anything but update the database
    """

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
                cAuthorId = row[0]
                # the author is in the database
                # update the corresponding entry
                if (row[1] != None and 
                    row[1] < date(int(data[3][0]), int(data[3][1]), int(data[3][2]))):
                    earlierDate = row[1]
                else:
                    earlierDate = date(int(data[3][0]), int(data[3][1]), int(data[3][2]))
                updateAuthor = ("UPDATE authors "
                                "SET total_publication = total_publication + 1, email = %s, independence_date = %s "
                                "WHERE  id = %s")
                authorData = (cAuthor[1], earlierDate, cAuthorId)
                cursor.execute(updateAuthor, authorData)
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
                otherAuthorId = row[0]
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
        paperData = (cAuthorId, date(int(data[3][0]), int(data[3][1]), 
            int(data[3][2])), data[0])
        cursor.execute(addPaper, paperData)
    except mysql.connector.Error as err:
        print(err)
        exit(1)

    
    

if __name__ == '__main__':
    print('function should not be called independently.')
#    data = (3, ['zhou zhou'], [('nico minc', 'fmndd@columbia.edu')], ('2013', '2', '1')) 
#    update(cursor, data)
