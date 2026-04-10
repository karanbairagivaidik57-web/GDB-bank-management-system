import pymysql
from BankUtility import *
from BankExcept import *
from datetime import datetime,time
import time
def transaction():
    con=None
    cur=None
    try:
        print("\n" + "=" * 90)
        type_effect("              GDB BANK - TRANSACTION ARCHIVE TERMINAL")
        print("=" * 90)
        con = pymysql.connect(
             host="localhost",
             user='root',
             password='Your Password',
             database="bank")
        cur=con.cursor()
        while True:
             try:
                 account = input("\nEnter Account Number (or '0' to exit): ").strip()
                 if account == '0': return
                 spinner_animation("Searching Secure Vault...", duration=1)
                 cur.execute(
                     "select t_id, dot, t_type, amount, remark from transactions where acno=%s ORDER BY dot DESC",
                     (account,))
                 data = cur.fetchall()
                 if not data:
                     raise AccountNotFoundError
                 else:
                     break
             except AccountNotFoundError:
                 print("[!] Error: Account Number not registered in our core database.")
        cur.execute("select cname,status,bal from bank where acno  = %s",(account,))
        all=cur.fetchone()
        name=all[0]
        status=all[1]
        bal=all[2]
        print("-"*90)
        print("\t\t\t\t\t\tGDB BANK - MINI STATEMENT")
        print("-"*90)
        now=datetime.now()

        print(f"Account: {account:<20} | Date: {now.strftime('%d-%m-%Y')} | Time: {now.strftime('%H:%M:%S')}")
        print(f"Customer Name :{name.upper():<20}|STATUS:{status.upper():<15}")
        print("-"*90)
        print(f"{'ID':<5}|{'Date & Time':<30}|{'Type':<10}|{'Amount (₹)':<15}|{'Remark':<20}")
        print("-"*90)
        if not data:
            print("\n\t\t\t--- No Transaction History Found ---")
        else:
            for row in data:
                t_id, dot, t_type, amount, remark = row
                if t_type.lower() == "credit":
                    display_type = "CREDIT"
                    display_amt = f"+{amount:.2f}"
                elif t_type.lower() == "debit":
                    display_type = "DEBIT"
                    display_amt = f"-{amount:.2f}"
                else:
                    display_type = t_type.upper()
                    display_amt = f"{amount:.2f}"
                time.sleep(0.05)
                print(f"{t_id:<6}|{str(dot):<25}|{display_type:<12}|{display_amt:<15}|{remark}")
            print("-" * 90)
            print(f"\t\t\t\t\tCURRENT BALANCE :₹{bal}")
            print("-" * 90)
            print("-" * 90)
            print("\t\t\t*** THANK YOU FOR BANKING WITH GDB ***")
            print("=" * 90)


    except Exception as e:
        print("Technical Error",e)
    finally:
        if con:
            con.close()
            cur.close()
