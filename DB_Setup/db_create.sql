DROP DATABASE IF EXISTS Mood_Tracker;
CREATE DATABASE Mood_Tracker;
USE Mood_Tracker;


-- create table that holds information on users
CREATE TABLE Users (
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    First_Name VARCHAR(50) NOT NULL,
	Family_Name VARCHAR(50) NOT NULL,
	User_Name VARCHAR(50) NOT NULL,
	Password VARCHAR(50) NOT NULL,
	Profile_Pic VARCHAR(50) NOT NULL
);

-- create table that stores entries in mood tracker app
CREATE TABLE Entries (
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    User_ID INT NOT NULL,
    Entry_Date DATE NOT NULL,
    Emotion VARCHAR(50),
    Giphy_URL VARCHAR(100),
    Quote VARCHAR(100),
    Diary_Entry VARCHAR(500),
    CONSTRAINT FK_Users FOREIGN KEY (User_ID) REFERENCES Users(ID)
);
