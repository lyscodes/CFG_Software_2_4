DROP DATABASE IF EXISTS Mood_Tracker;
CREATE DATABASE Mood_Tracker;
USE Mood_Tracker;


-- create table that holds information on users
CREATE TABLE Users (
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    First_Name VARCHAR(50) NOT NULL,
	Family_Name VARCHAR(50) NOT NULL,
	User_Name VARCHAR(50) NOT NULL UNIQUE,
	Password VARCHAR(50) NOT NULL,
	Profile_Pic VARCHAR(50) NOT NULL
);

-- create table that stores entries in mood tracker app
CREATE TABLE Entries (
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    User_Name VARCHAR(50) NOT NULL UNIQUE,
    Entry_Date DATE NOT NULL,
    Emotion VARCHAR(50),
    Response VARCHAR(500),
    Diary_Entry VARCHAR(500));