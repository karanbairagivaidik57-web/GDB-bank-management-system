from BankDB import get_connection
from BankUtility import *
def search_customer():
    con=None
    cur=None
    try:

        con=get_connection()
        cur=con.cursor()
        print("\n" + "=" * 60)
        type_effect(">>> GDB BANKING CENTRAL SEARCH TERMINAL")
        print("=" * 60)
        account = input("\nEnter A/C No or Mobile Number: ").strip()
        if not account:
            print("\n[!] ERROR: Search field cannot be empty.")
            return
        spinner_animation("Searching Server Databases", duration=1.5)
        cur.execute("select acno,cname,mobile_number,acc_type,bal,status from bank where acno = %s or mobile_number = %s",(account,account))
        data=cur.fetchall()
        if not data:
            print("\n" + "-" * 60)
            print(f"[!] ALERT: No record found for ID: {account}")
            print("-" * 60)
        else:
            print("-" * 100)
            print(f"{'A/C NO':<15} {'CUSTOMER NAME':<20} {'MOBILE':<15} {'TYPE':<12} {'BALANCE':<15} {'STATUS':<10}")
            print("-" * 100)
            for row in data:
                print(
                    f"{row[0]:<15} {row[1].upper():<20} {row[2]:<15} {row[3].upper():<12} {row[4]:<15,.2f} {row[5].upper():<10}")
            print("-" * 100)
    except Exception as error:
        print("Technical Error:",error)
    finally:
        if con:
            con.close()
            cur.close()