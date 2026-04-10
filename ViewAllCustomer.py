from BankDB import get_connection
from BankUtility import *
def view_all_customers():
    con=None
    cur=None
    try:
        con=get_connection()
        cur=con.cursor()
        progress_bar("Compiling Master Ledger", duration=2)
        print("\n" + "=" * 115)
        print(f"{'A/C NO':<15} {'CUSTOMER NAME':<25} {'MOBILE':<15} {'TYPE':<12} {'BALANCE':<20} {'STATUS':<10}")
        print("=" * 115)
        cur.execute("select acno,cname,mobile_number,acc_type,bal,status from bank")
        data=cur.fetchall()
        if not data:
            print("\n[!] DATA ERROR: No customers found in Bank.")
            return
        formatted = 0
        total_active=0
        total_inactive=0
        for row in data:
            print(f"{row[0]:<15} {row[1].upper():<25} {row[2]:<15} {row[3].upper():<12} ₹{row[4]:<20,.2f} {row[5].upper():<10}")
            bal=row[4]
            formatted+=bal
            if row[5].lower()=="active":
                total_active+=1
            else:
                total_inactive+=1
        total_bal=f"{formatted:,.2f}"
        length=len(data)
        print("=" * 115)
        type_effect("\n>>> INTERNAL AUDIT SUMMARY:")
        print(f"Total Customers: {length}          | Total Active:{total_active}          |Total Closed :{total_inactive}")
        print(f"TOTAL BANK DEPOSITS :{total_bal}")
        print("-"*100)
    except Exception as e:
        print("Technical Error",e)
    finally:
        if con:
            con.close()
            cur.close()