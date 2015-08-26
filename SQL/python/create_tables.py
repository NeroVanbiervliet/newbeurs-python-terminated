#!/usr/bin/python
import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="lnrddvnc", db="oakTest")

# cursor object
cur = conn.cursor() 

#query = "DROP 

#query = ("CREATE TABLE user("
#	"id int NOT NULL AUTO_INCREMENT,"
#	"name varchar(30) NOT NULL UNIQUE,"
#	"passwordHashed varchar(100),"
#	"PRIMARY KEY (id));")

#query = ("CREATE TABLE stock("
#	"id int NOT NULL AUTO_INCREMENT,"
#	"name varchar(30) NOT NULL,"
#	"ticker varchar(10) NOT NULL UNIQUE,"
#	"market varchar(20),"
#	"PRIMARY KEY (id));")

#query = ("CREATE TABLE stockCategory("
#	"id int NOT NULL AUTO_INCREMENT,"
#	"stock int NOT NULL,"
#	"criterium varchar(20) NOT NULL,"
#	"value varchar(30) NOT NULL,"
#	"FOREIGN KEY (stock) REFERENCES stock(id),"
#	"PRIMARY KEY (id));")

#query = ("CREATE TABLE method("
#	"id int NOT NULL AUTO_INCREMENT,"
#	"name varchar(20) NOT NULL UNIQUE,"
#	"description varchar(150),"
#	"PRIMARY KEY (id));")

#query = ("CREATE TABLE strategy("
#	"id int NOT NULL AUTO_INCREMENT,"
#	"name varchar(20) NOT NULL UNIQUE,"
#	"method int NOT NULL,"
#	"isActive boolean NOT NULL DEFAULT TRUE,"
#	"parameters varchar(100) NOT NULL DEFAULT '',"
#	"FOREIGN KEY (method) REFERENCES method(id),"
#	"PRIMARY KEY (id));")

#query = ("CREATE TABLE strategyEditHistory("
#	"id int NOT NULL AUTO_INCREMENT,"
#	"strategy int NOT NULL,"
#	"editor int NOT NULL,"
#	"timestamp datetime NOT NULL DEFAULT GETDATE(),"
#	"newParameters varchar(100) NOT NULL DEFAULT '',"
#	"FOREIGN KEY (strategy) REFERENCES strategy(id),"
#	"FOREIGN KEY (editor) REFERENCES user(id),"
#	"PRIMARY KEY (id));")

#query = ("CREATE TABLE transaction("
#	"id int NOT NULL AUTO_INCREMENT,"
#	"stock int NOT NULL,"
#	"isBuy boolean NOT NULL,"
#	"numOfStock int NOT NULL,"
#	"timestamp datetime NOT NULL DEFAULT GETDATE(),"
#	"operator int NOT NULL,"
#	"price float NOT NULL,"
#	"transactionCost float NOT NULL,"
#	"FOREIGN KEY (stock) REFERENCES stock(id),"
#	"FOREIGN KEY (operator) REFERENCES user(id),"
#	"PRIMARY KEY (id));")

#query = ("CREATE TABLE simulation("
#	"id int NOT NULL AUTO_INCREMENT,"
#	"name varchar(30) NOT NULL UNIQUE,"
#	"description varchar(60) NOT NULL DEFAULT '',"
#	"owner int NOT NULL,"
#	"timestampStart datetime NOT NULL DEFAULT GETDATE(),"
#	"timestampEnd datetime NOT NULL DEFAULT GETDATE(),"
#	"gain float NOT NULL,"
#	"return float NOT NULL,"
#	"status varchar(8) NOT NULL,"
#	"FOREIGN KEY (stock) REFERENCES stock(id),"
#	"FOREIGN KEY (owner) REFERENCES user(id),"
#	"PRIMARY KEY (id));")

#query = ("CREATE TABLE webAppLoginHistory("
#	"id int NOT NULL AUTO_INCREMENT,"
#	"succeeded boolean NOT NULL DEFAULT TRUE,"
#	"user int NOT NULL,"
#	"timestamp datetime NOT NULL DEFAULT GETDATE(),"
#	"FOREIGN KEY (user) REFERENCES user(id),"
#	"PRIMARY KEY (id));")

#query = ("CREATE TABLE portfolio("
#	"id int NOT NULL AUTO_INCREMENT,"
#	"name varchar(30) UNIQUE NOT NULL,"
#	"capital int NOT NULL,"
#	"PRIMARY KEY (id));")

cur.execute(query)
cur.close()
conn.commit()
conn.close()
