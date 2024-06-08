DROP DATABASE IF EXISTS Mood_Tracker;
CREATE DATABASE Mood_Tracker;
USE Mood_Tracker;


-- create table that holds information on users
CREATE TABLE Users (
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    First_Name VARCHAR(50) NOT NULL,
	Family_Name VARCHAR(50) NOT NULL,
	User_Name VARCHAR(50) NOT NULL UNIQUE,
    Email VARCHAR(50) NOT NULL UNIQUE,
	Password VARCHAR(72) NOT NULL
);


-- create table that stores entries in mood tracker app
CREATE TABLE Entries (
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    User_ID INT NOT NULL,
    Entry_Date DATE NOT NULL,
    Emotion VARCHAR(50),
    Giph_URL VARCHAR(250),
    Choice_J_or_Q VARCHAR(50),
    Response_J_or_Q VARCHAR(500),
    Diary_Entry VARCHAR(500),
    CONSTRAINT FK_Users FOREIGN KEY (User_ID) REFERENCES Users(ID)
);

-- new line above needed for the db_builder