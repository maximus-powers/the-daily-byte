-- User table for authentication and settings
CREATE TABLE `user` (
    `userID` INT AUTO_INCREMENT PRIMARY KEY,
    `firstName` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) UNIQUE NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `categories` VARCHAR(255) NOT NULL
);

-- landing section table
CREATE TABLE landing (
    landingID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT NOT NULL,
    memeTerm VARCHAR(255),
    memeURL VARCHAR(255),
    headline TEXT,
    summary TEXT,
    last_updated DATE,
    FOREIGN KEY (userID) REFERENCES user(userID)
);

-- Category tables
CREATE TABLE `business` (
    `recordID` INT AUTO_INCREMENT PRIMARY KEY,
    `userID` INT,
    `last_updated` DATE NOT NULL,
    `headline` VARCHAR(255) NOT NULL,
    `summary` TEXT NOT NULL,
    `url` VARCHAR(255) NOT NULL,
    FOREIGN KEY (`userID`) REFERENCES `user`(`userID`) ON DELETE CASCADE
);

CREATE TABLE `entertainment` (
    `recordID` INT AUTO_INCREMENT PRIMARY KEY,
    `userID` INT,
    `last_updated` DATE NOT NULL,
    `headline` VARCHAR(255) NOT NULL,
    `summary` TEXT NOT NULL,
    `url` VARCHAR(255) NOT NULL,
    FOREIGN KEY (`userID`) REFERENCES `user`(`userID`) ON DELETE CASCADE
);

CREATE TABLE `general` (
    `recordID` INT AUTO_INCREMENT PRIMARY KEY,
    `userID` INT,
    `last_updated` DATE NOT NULL,
    `headline` VARCHAR(255) NOT NULL,
    `summary` TEXT NOT NULL,
    `url` VARCHAR(255) NOT NULL,
    FOREIGN KEY (`userID`) REFERENCES `user`(`userID`) ON DELETE CASCADE
);

CREATE TABLE `health` (
    `recordID` INT AUTO_INCREMENT PRIMARY KEY,
    `userID` INT,
    `last_updated` DATE NOT NULL,
    `headline` VARCHAR(255) NOT NULL,
    `summary` TEXT NOT NULL,
    `url` VARCHAR(255) NOT NULL,
    FOREIGN KEY (`userID`) REFERENCES `user`(`userID`) ON DELETE CASCADE
);

CREATE TABLE `science` (
    `recordID` INT AUTO_INCREMENT PRIMARY KEY,
    `userID` INT,
    `last_updated` DATE NOT NULL,
    `headline` VARCHAR(255) NOT NULL,
    `summary` TEXT NOT NULL,
    `url` VARCHAR(255) NOT NULL,
    FOREIGN KEY (`userID`) REFERENCES `user`(`userID`) ON DELETE CASCADE
);

CREATE TABLE `sports` (
    `recordID` INT AUTO_INCREMENT PRIMARY KEY,
    `userID` INT,
    `last_updated` DATE NOT NULL,
    `headline` VARCHAR(255) NOT NULL,
    `summary` TEXT NOT NULL,
    `url` VARCHAR(255) NOT NULL,
    FOREIGN KEY (`userID`) REFERENCES `user`(`userID`) ON DELETE CASCADE
);

CREATE TABLE `technology` (
    `recordID` INT AUTO_INCREMENT PRIMARY KEY,
    `userID` INT,
    `last_updated` DATE NOT NULL,
    `headline` VARCHAR(255) NOT NULL,
    `summary` TEXT NOT NULL,
    `url` VARCHAR(255) NOT NULL,
    FOREIGN KEY (`userID`) REFERENCES `user`(`userID`) ON DELETE CASCADE
);