--OVO JE ZA POKRETANJE: sqlcmd -S localhost\SQLEXPRESS -i baza\zahtev.sql
USE EKO;  
GO  

select * from formica;
GO
quit

DROP TABLE poziv;
GO
quit

select * from Users;
GO
quit

SELECT name, max_length, precision FROM sys.columns WHERE object_id = OBJECT_ID('Users') 
GO
quit

--Listaj sve tabele u semi
SELECT name
FROM sys.tables
GO
quit

CREATE TABLE Ids (
    ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    Email varchar(70) NOT NULL,
    Pass varchar(32) NOT NULL,
);
GO

CREATE TABLE Users (
    ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    Email varchar(70) NOT NULL,
    Ime varchar(20) NOT NULL,
    Prezime varchar(30) NOT NULL,
    Grad varchar(30) NOT NULL,
);
GO
quit

select * from Ids;
GO

quit

INSERT INTO Users
VALUES (4, "Andreja", "Jankovic")
GO

quit

CREATE DATABASE EKO
ON   
( NAME = EKO_podaci,  
    FILENAME = "C:\Users\Andreja\Documents\BAZE_SQL_SERVER\eko_podaci.mdf",
    SIZE = 10MB,  
    FILEGROWTH = 5MB )  
LOG ON  
( NAME = EKO_log,  
    FILENAME = "C:\Users\Andreja\Documents\BAZE_SQL_SERVER\eko_log.ldf",  
    SIZE = 2MB,  
    FILEGROWTH = 1MB );  
GO
quit
