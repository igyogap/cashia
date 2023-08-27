import mysql.connector

class DBInterface:

    # Connection Database
    def queries(self, sql):
        mydb = mysql.connector.connect(host="192.168.1.15", user="cashia", password="P3j3ng#99", database="cashia")
        mycursor = mydb.cursor()
        try:
            mycursor.execute(sql)
            result=mycursor.fetchall()
            return result
        except Exception as e :
            print("Error executing SQL Query:",e )

    def commands(self, sql):
        mydb = mysql.connector.connect(host="192.168.1.15", user="cashia", password="P3j3ng#99", database="cashia")
        mycursor = mydb.cursor()
        try:
            mycursor.execute(sql)
            mydb.commit()
        except Exception as e:
            mydb.rollback()

    # Close connection to the server
