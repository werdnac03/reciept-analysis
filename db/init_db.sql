CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Username VARCHAR(100),
    PasswordHash TEXT NOT NULL
);

CREATE TABLE Receipts (
    ReceiptID SERIAL PRIMARY KEY,
    CreatorID INT REFERENCES Users(UserID),
    StoreName VARCHAR(255),
    TotalAmount DECIMAL,
    ImageBase64 TEXT,
    OCRText TEXT
);

CREATE TABLE ShareReceipts (
    ShareID SERIAL PRIMARY KEY,
    UserID INT REFERENCES Users(UserID),
    ReceiptID INT REFERENCES Receipts(ReceiptID),
    UNIQUE(UserID, ReceiptID)
);

CREATE TABLE Item (
    ItemID SERIAL PRIMARY KEY,
    ReceiptID INT REFERENCES Receipts(ReceiptID),
    ItemName VARCHAR(255),
    Price DECIMAL,
    Quantity INT DEFAULT 1
);

CREATE TABLE ItemOwnership (
    OwnershipID SERIAL PRIMARY KEY,
    ReceiptID INT REFERENCES Receipts(ReceiptID),
    UserID INT REFERENCES Users(UserID),
    ItemID INT REFERENCES Item(ItemID),
    Quantity INT DEFAULT 1
);

CREATE TABLE Transactions (
    TransactionID SERIAL PRIMARY KEY,
    FromUserID INT REFERENCES Users(UserID),
    ToUserID INT REFERENCES Users(UserID),
    ReceiptID INT REFERENCES Receipts(ReceiptID),
    Amount DECIMAL,
    Status VARCHAR(255) DEFAULT 'pending',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Notification (
    NotificationID SERIAL PRIMARY KEY,
    FromUserID INT REFERENCES Users(UserID),
    ToUserID INT REFERENCES Users(UserID),
    Message TEXT,
    Status VARCHAR(255)
);