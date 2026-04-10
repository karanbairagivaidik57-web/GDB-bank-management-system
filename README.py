# 🏦 GDB Bank Management System

🚀 A real-world Banking System with ATM simulation, Admin Panel, and secure transaction handling using Python & MySQL.

⭐ Star this repository if you find it useful!

---

## 🚀 Overview

**GDB Bank Management System** is a fully functional console-based banking application built using **Python and MySQL**.
It simulates real-world banking operations such as **account management, ATM transactions, secure PIN handling, and admin controls**.

The project follows a **modular architecture**, making the code clean, scalable, and closer to real-world backend systems.

---

## ✨ Key Features

### 👨‍💼 Admin / Staff Panel

* Secure Staff Login (ID & Password)
* Open New Bank Account
* Search Customer Details
* View Full Customer KYC
* View All Customers (Ledger View)
* Close / Deactivate Account (Soft Delete)

---

### 👤 Customer Banking (ATM / Self-Service)

* 💰 Cash Deposit (ATM & Counter)
* 💸 Cash Withdrawal with limits & validation
* 🔄 Fund Transfer between accounts
* 📜 Transaction History (Mini Statement)
* 🆕 First-Time PIN Generation (System Generated)
* 🔑 Secure PIN Update (User Defined)
* 🏦 Check Balance with receipt output

---

## 🧠 Project Highlights

* ✅ Real-world banking workflow simulation
* ✅ Foreign Key relationships (Bank ↔ Transactions)
* ✅ Centralized database connection (optimized)
* ✅ Custom exception handling system
* ✅ Automatic account number generation
* ✅ Secure PIN validation for transactions
* ✅ Console-based UI with animations

---

## 🏗️ Project Structure

```bash
GDB-Bank-Management-System/
│
├── core/                # Main flow & menus
├── modules/             # Banking operations
├── security/            # PIN management
├── customer/            # Customer data handling
├── database/            # DB creation scripts
├── utils/               # DB connection, exceptions, utilities
│
├── README.md
├── requirements.txt
```

---

## 🗄️ Database Design

### 📌 Tables Used

#### 1. Bank Table

* Account Number (Primary Key)
* Name
* Mobile Number
* Email
* Aadhar
* Account Type (Saving / Current)
* Balance
* Status (Active / Closed)
* Opening Date

#### 2. Transactions Table

* Transaction ID
* Account Number (Foreign Key)
* Transaction Type
* Amount
* Date & Time

#### 3. Staff Table

* Staff ID
* Name
* Password

---

## 🔐 Security Features

* PIN authentication for transactions
* Withdrawal limits & minimum balance enforcement
* Account verification before operations
* Staff authentication system
* Soft delete (Account Closure)

---

## ⚙️ Technologies Used

* Python (Core)
* MySQL
* PyMySQL

---

## ▶️ How to Run

```bash
# Step 1: Setup Database
python BankCreateDatabaseTable.py

# Step 2: Run Application
python BankMain.py
```

---

## ⚠️ Important Notes

* Update database credentials in `BankDB.py`
* Ensure MySQL server is running
* Do not upload real passwords (use placeholders)

---

## 🚀 Future Enhancements

* Web Version using Django
* REST API Integration
* OTP / Email Verification
* GUI Interface (Tkinter / Web)

---

## 👨‍💻 Author

**Karan Bairagi**

---

## 🙌 Support

If you like this project:

* ⭐ Star the repository
* 🔁 Share on LinkedIn
* 💬 Provide feedback

---
