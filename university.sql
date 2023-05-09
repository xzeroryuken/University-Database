CREATE DATABASE university;
USE university;

CREATE TABLE `Professor` (
  `Professor_ID` INT,
  `First_Name` VARCHAR(50),
  `Last_Name` VARCHAR(50),
  `Address` VARCHAR(50),
  `Phone_Number` VARCHAR(50),
  `Email` VARCHAR(50),
  PRIMARY KEY (`Professor_ID`)
);

CREATE TABLE `Teaches` (
  `Course_ID` INT,
  `Professor_ID` INT,
  `Semesters` INT,
  FOREIGN KEY (`Professor_ID`) REFERENCES `Professor`(`Professor_ID`)
);

CREATE TABLE `Enrollment` (
  `Student_ID` INT,
  `Course_ID` INT,
  `Grade` VARCHAR(50),
  PRIMARY KEY (`Student_ID`, `Course_ID`),
  FOREIGN KEY (`Student_ID`) REFERENCES `Student`(`Student_ID`),
  FOREIGN KEY (`Course_ID`) REFERENCES `Course`(`Course_ID`)
);

CREATE TABLE `Department` (
  `Department_ID` INT,
  `Department_Name` VARCHAR(50),
  PRIMARY KEY (`Department_ID`)
);

CREATE TABLE `Course` (
  `Course_ID` INT,
  `Department_ID` INT,
  `Professor_ID` INT,
  `Start_Time` TIME,
  `End_Time` TIME,
  `Room_Number` INT,
  `Course_Name` VARCHAR(50),
  `Year` INT,
  `Term` VARCHAR(50),
  PRIMARY KEY (`Course_ID`),
  FOREIGN KEY (`Professor_ID`) REFERENCES `Professor`(`Professor_ID`),
  FOREIGN KEY (`Department_ID`) REFERENCES `Department`(`Department_ID`)
);
CREATE TABLE `Student` (
  `Student_ID` INT,
  `First_Name` VARCHAR(50),
  `Last_Name` VARCHAR(50),
  `Address` VARCHAR(50),
  `Phone_Number` VARCHAR(50),
  `Email` VARCHAR(50),
  `Date_of_Birth` DATE,
  `Password` VARCHAR(50),
  PRIMARY KEY (`Student_ID`)
);
