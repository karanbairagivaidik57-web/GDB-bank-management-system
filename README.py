# 🏦 GDB Bank Management System

🚀 A real-world Banking System with ATM simulation, Admin Panel, and secure transaction handling using Python & MySQL.

⭐ Star this repository if you find it useful!

---

## 🚀 Overview

GDB Bank Management System is a fully functional console-based banking application built using Python and MySQL.  
It simulates real-world banking operations such as account management, ATM transactions, secure PIN handling, and admin controls.

The project follows a modular architecture, making the code clean, scalable, and closer to real-world backend systems.

---

## ✨ Key Features

### 👨‍💼 Admin / Staff Panel

- Secure Staff Login (ID & Password)
- Open New Bank Account
- Search Customer Details
- View Full Customer KYC
- View All Customers (Ledger View)
- Close / Deactivate Account (Soft Delete)

---

### 👤 Customer Banking (ATM / Self-Service)

- 💰 Cash Deposit (ATM & Counter)
- 💸 Cash Withdrawal with limits & validation
- 🔄 Fund Transfer between accounts
- 📜 Transaction History (Mini Statement)
- 🆕 First-Time PIN Generation (System Generated)
- 🔑 Secure PIN Update (User Defined)
- 🏦 Check Balance with receipt output

---

## 🧠 Project Highlights

- Real-world banking workflow simulation  
- Foreign Key relationships (Bank ↔ Transactions)  
- Centralized database connection  
- Custom exception handling  
- Automatic account number generation  
- Secure PIN validation  
- Console-based UI with animations  

---

## 🏗️ Project Structure

```
GDB-Bank-Management-System/
│
├── core/
├── modules/
├── security/
├── customer/
├── database/
├── utils/
│
├── README.md
├── requirements.txt
```

---

## 🗄️ Database Design

### Tables Used

**Bank Table**
- Account Number (Primary Key)
- Name
- Mobile Number
- Email
- Aadhar
- Account Type
- Balance
- Status
- Opening Date

**Transactions Table**
- Transaction ID
- Account Number (Foreign Key)
- Transaction Type
- Amount
- Date & Time

**Staff Table**
- Staff ID
- Name
- Password

---

## 🔐 Security Features

- PIN authentication for transactions  
- Withdrawal limits & minimum balance rules  
- Account verification before operations  
- Staff authentication system  
- Soft delete (account closure)  

---

## ⚙️ Technologies Used

- Python  
- MySQL  
- PyMySQL  

---

## ▶️ How to Run

```
python BankCreateDatabaseTable.py
python BankMain.py
```

---

## ⚠️ Important Notes

- Update database credentials in BankDB.py  
- Ensure MySQL server is running  
- Do not upload real passwords  

---

## 🚀 Future Enhancements

- Django Web Version  
- REST API Integration  
- OTP Verification  
- GUI Interface  

---

## 👨‍💻 Author

Karan Bairagi

---

## 🙌 Support

If you like this project:

- Star the repository  
- Share on LinkedIn  
- Give feedback  
