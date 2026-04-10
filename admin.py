import pymysql

from BankAccountOpen import accountopen
from DeleteCustomers import delete_customer
from ViewAllCustomer import view_all_customers
from SearchCustomer import search_customer
from ViewSingalCustomer import view_singal_customer
from BankUtility import *
def admin_login():
    con=None
    cur=None
    try:
        con=pymysql.connect(
            host="localhost",
            password="Your password",
            user="root",
            database="BANK"
        )
        print("\n" + "=" * 60)
        type_effect("        GDB BANK - SECURE STAFF TERMINAL v2.0")
        print("=" * 60)
        login = input("\nEnter Staff ID       : ").strip()
        password = input("Enter Staff Password : ").strip()
        spinner_animation("Authenticating Credentials", duration=1.5)
        cur=con.cursor()
        cur.execute("select * from staff where staff_id = %s and password = %s",(login,password))
        data=cur.fetchone()
        if data is None:
            print("\n" + "!" * 60)
            type_effect("[!!] ACCESS DENIED: Invalid Staff ID or Password.")
            print("!" * 60)
        else:
            animation(f"Welcome, {data[1].upper()} | Access Granted", duration=1)
            while True:
                print("\n" + "╔" + "═" * 45 + "╗")
                print(f"║{'ADMIN CONTROL PANEL - GDB BANK':^45}║")
                print("╠" + "═" * 45 + "╣")
                print("║ 1. ➕ Open New Bank Account                ║")
                print("║ 2. 🔍 Search Customer Details              ║")
                print("║ 3. 👤 View Single Customer (Full KYC)      ║")
                print("║ 4. 📊 View All Customers (Ledger)          ║")
                print("║ 5. ❌ Close / Deactivate Account           ║")
                print("║ 6. 🚪 Logout & Secure Terminal             ║")
                print("╚" + "═" * 45 + "╝")
                try:
                    ch = input("Enter System Choice [1-4]: ").strip()

                    if ch == '1':
                        accountopen()
                    elif ch == '2':
                        search_customer()
                    elif ch == '3':
                        view_singal_customer()
                    elif ch=='4':
                            view_all_customers()
                    elif ch=='5':
                            delete_customer()
                    elif ch=='6':
                        loading_bar("Signing Out & Clearing Cache", duration=0.01)
                        print("\n[+] Session Ended Successfully. Have a great day!")
                        return
                    else:
                        print("\n[!] Invalid Choice! Please select between 1 and 4.")
                except ValueError:
                    print("\n[!] Error: Please enter a numeric value.")


    except Exception as e:
        print("Technical Error",e)
    finally:
        if con:
            con.close()
            cur.close()