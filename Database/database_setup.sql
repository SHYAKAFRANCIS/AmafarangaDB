use tricode_db;
CREATE TABLE USERS (
    User_id INT PRIMARY KEY AUTO_INCREMENT,
    Phone_number VARCHAR(20) UNIQUE NOT NULL,
    Full_name VARCHAR(100),
    Email VARCHAR(100),
    Registration_date VARCHAR(100),
    Status VARCHAR(20) DEFAULT 'ACTIVE',
    Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE TABLE CATEGORIES (
    Category_id INT PRIMARY KEY AUTO_INCREMENT,
    Category_name VARCHAR(100),
    Description TEXT
);
CREATE TABLE FEE_TYPES (
    fee_type_id INT PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(50),
    fee_percentage DECIMAL(5,2) DEFAULT 0.21,
    fixed_amount DECIMAL(15,2),
    min_fee DECIMAL(10,2),
    max_fee DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE
);
CREATE TABLE TRANSACTIONS (
    Transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    Sender_id INT NOT NULL,
    Receiver_id INT NOT NULL,
    Category_id INT NOT NULL,
    Amount DECIMAL(15,2) NOT NULL,
    Transaction_type TIMESTAMP NOT NULL,
    Transaction_status VARCHAR(20) DEFAULT 'ACTIVE',

    FOREIGN KEY (Sender_id) REFERENCES USERS(User_id),
    FOREIGN KEY (Receiver_id) REFERENCES USERS(User_id),
    FOREIGN KEY (Category_id) REFERENCES CATEGORIES(Category_id)
);
CREATE TABLE SYSTEM_LOGS (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id INT,
    Actor VARCHAR(100),
    Log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Status_message TEXT,

    FOREIGN KEY (transaction_id) REFERENCES TRANSACTIONS(Transaction_id)
);
CREATE TABLE USER_TRANSACTIONS (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    transaction_id INT NOT NULL,
    role ENUM('sender', 'receiver', 'approver', 'viewer', 'favorite', 'witness', 'auditor') DEFAULT 'viewer',
    Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES USERS(User_id),
    FOREIGN KEY (transaction_id) REFERENCES TRANSACTIONS(Transaction_id),

    UNIQUE KEY unique_user_transaction_role (user_id, transaction_id, role)
);
CREATE TABLE TRANSACTION_FEES (
    transaction_fee_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id INT NOT NULL,
    fee_type_id INT NOT NULL,
    fee_amount DECIMAL(10,2),
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (transaction_id) REFERENCES TRANSACTIONS(Transaction_id),
    FOREIGN KEY (fee_type_id) REFERENCES FEE_TYPES(fee_type_id)
);
INSERT INTO USERS (Phone_number, Full_name, Email, Registration_date, Status) VALUES
('+250788123456', 'Keza Meghan', 'keza.meg@gmail.com', '2024-01-15', 'ACTIVE'),
('+250788234567', 'Uncle Ben', 'uncle.b@gmail.com', '2024-02-20', 'ACTIVE'),
('+250788345678', 'Uncle Francis', 'uncle.f@gmail.com', '2024-03-10', 'ACTIVE'),
('+250788456789', 'Nganji Jospin', 'Nganji.j@gmail.com', '2024-04-05', 'ACTIVE'),
('+250788567890', 'Uncle Mosh', 'mosh@gmail.com', '2024-05-12', 'INACTIVE'),
('+250788678901', 'Aunty Meg', 'meg@gmail.com', '2024-06-18', 'ACTIVE'),
('+250788789012', 'Tonton Rich', 'tonton.r@gmail.com', '2024-07-22', 'ACTIVE'),
('+250788890123', 'Shyaka Francis', 'shyaka.f@gmail.com', '2024-08-30', 'ACTIVE');

INSERT INTO CATEGORIES (Category_name, Description) VALUES
('Transfer', 'Money transfer between users'),
('Payment', 'Payment for goods or services'),
('Withdrawal', 'Cash withdrawal from account'),
('Deposit', 'Money deposit into account'),
('Utility Bill', 'Utility bill payments'),
('Airtime', 'Mobile airtime purchase'),
('School Fees', 'School fee payments'),
('Donation', 'Charitable donations');

INSERT INTO FEE_TYPES (type_name, fee_percentage, fixed_amount, min_fee, max_fee, is_active) VALUES
('Processing Fee', 2.00, 0.00, 100.00, 5000.00, TRUE),
('Platform Fee', 0.00, 50.00, 50.00, 50.00, TRUE),
('International Transfer Fee', 3.50, 0.00, 500.00, 10000.00, TRUE),
('Express Processing Fee', 1.00, 200.00, 200.00, 3000.00, TRUE),
('ATM Withdrawal Fee', 0.00, 300.00, 300.00, 300.00, TRUE),
('Premium Service Fee', 0.50, 100.00, 100.00, 2000.00, FALSE);

INSERT INTO TRANSACTIONS (Sender_id, Receiver_id, Category_id, Amount, Transaction_type, Transaction_status) VALUES
(1, 2, 1, 50000.00, '2025-01-15 10:30:00', 'COMPLETED'),
(2, 3, 2, 25000.00, '2025-01-16 14:45:00', 'COMPLETED'),
(3, 4, 1, 100000.00, '2025-01-17 09:15:00', 'COMPLETED'),
(4, 1, 5, 15000.00, '2025-01-18 16:20:00', 'PENDING'),
(6, 7, 2, 75000.00, '2025-01-20 13:30:00', 'COMPLETED'),
(7, 8, 6, 5000.00, '2025-01-21 08:45:00', 'COMPLETED'),
(8, 6, 1, 45000.00, '2025-01-22 15:10:00', 'FAILED'),
(2, 4, 7, 200000.00, '2025-01-23 10:00:00', 'COMPLETED'),
(3, 1, 4, 60000.00, '2025-01-23 12:30:00', 'PENDING');

INSERT INTO SYSTEM_LOGS (transaction_id, Actor, Status_message) VALUES
(1, 'Keza Meghan', 'Transaction initiated successfully'),
(1, 'System', 'Payment processed'),
(1, 'System', 'Transaction completed'),
(2, 'Uncle Ben', 'Transaction initiated successfully'),
(2, 'System', 'Transaction completed'),
(3, 'Uncle Francis', 'Transaction initiated successfully'),
(3, 'System', 'Large amount flagged for review'),
(3, 'Admin', 'Transaction approved'),
(3, 'System', 'Transaction completed'),
(4, 'Nganji Jospin', 'Transaction initiated successfully'),
(4, 'System', 'Awaiting payment confirmation'),
(5, 'Aunty Meg', 'Withdrawal request submitted'),
(5, 'System', 'Transaction completed');

INSERT INTO TRANSACTION_FEES (transaction_id, fee_type_id, fee_amount) VALUES
-- Transaction 1 fees
(1, 1, 1000.00),  -- Processing fee (2% of 50000)
(1, 2, 50.00),    -- Platform fee
-- Transaction 2 fees
(2, 1, 500.00),   -- Processing fee (2% of 25000)
(2, 2, 50.00),    -- Platform fee
-- Transaction 3 fees
(3, 1, 2000.00),  -- Processing fee (2% of 100000)
(3, 2, 50.00),    -- Platform fee
(3, 4, 200.00),   -- Express processing fee
-- Transaction 4 fees
(4, 1, 300.00),   -- Processing fee (2% of 15000)
-- Transaction 5 fees
(5, 1, 600.00),   -- Processing fee (2% of 30000)
(5, 5, 300.00),   -- ATM withdrawal fee
-- Transaction 6 fees
(6, 1, 1500.00),  -- Processing fee (2% of 75000)
(6, 2, 50.00),    -- Platform fee
-- Transaction 7 fees
(7, 1, 100.00),   -- Processing fee (min fee applied)
-- Transaction 9 fees
(9, 1, 4000.00),  -- Processing fee (2% of 200000)
(9, 2, 50.00),    -- Platform fee
-- Transaction 10 fees
(10, 1, 1200.00); -- Processing fee (2% of 60000)

SELECT * FROM USERS;
UPDATE USERS SET Full_name='UNCLE KAMI' WHERE User_id=5;
DELETE FROM TRANSACTIONS WHERE Receiver_id=5;
SELECT * FROM USERS;
UPDATE USERS SET Status = 'ACTIVE' WHERE User_id IN (1, 2);
SELECT * FROM USERS;
DELETE FROM USERS WHERE User_id = 5;
SELECT * FROM TRANSACTIONS;
UPDATE TRANSACTIONS SET Receiver_id = 2 WHERE Transaction_id = 5;
SELECT * FROM TRANSACTIONS;
DELETE FROM USERS WHERE User_id = 5;
SELECT * FROM USERS;
SELECT * FROM TRANSACTIONS;
DROP TABLE USER_TRANSACTIONS;
SELECT * FROM USERS;