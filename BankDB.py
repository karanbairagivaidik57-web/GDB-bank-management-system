import pymysql
def get_connection():
    try:
        con=pymysql.connect(
            host="localhost",
            user="root",
            password="Your Password",
            database="BANK"
        )
        return con
    except Exception as e:
        print("MySQL Error :",e)