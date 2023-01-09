CREATE TABLE SignUpTable(custID varchar(5) NOT NULL UNIQUE, dob varchar(10) NOT NULL, firstName varchar(20) NOT NULL, lastName varchar(20) NOT NULL, 
address varchar(100) NOT NULL, phoneNo varchar(15) NOT NULL, email varchar(50) PRIMARY KEY, password varchar(20) NOT NULL);

SELECT * FROM SignUpTable;
