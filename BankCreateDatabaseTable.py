import pymysql
con=pymysql.connect(host="localhost",user="root",password="YOUR PASSWORD")
cur=con.cursor()
cur.execute("CREATE DATABASE BANK")
cur.execute("USE BANK")
cur.execute("CREATE TABLE if not exists bank(acno varchar(12) primary key,"
            "cname varchar(50) not null,"
            "mobile_number varchar(15) unique not null,"
            "email_id varchar(100),"
            "aadhaar_id varchar(12) not null,"
            "nominee varchar(50),"
            "IFSC varchar(11) not null,"
            "PIN char(4) not null,"
            "bal decimal(15,2) default 0.00,"
            "acc_type varchar(11) not null,"
            "status varchar(50) not null,"
            "opening_date datetime default current_timestamp)")
cur.execute("CREATE TABLE if not exists Transactions(t_id int primary key auto_increment,"
            "acno varchar(12) not null,"
            "dot datetime default current_timestamp not null,"
            "t_type varchar(20) not null,"
            "amount decimal(15,2) not null,"
            "remark varchar(255) not null,"
            "foreign key(acno) references bank(acno))")
print("Table and Database Successfully Created")
con.commit()
con.close()
