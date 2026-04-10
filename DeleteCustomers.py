from BankDB import get_connection
from BankExcept import *
from datetime import datetime
from BankUtility import *
from Transaction_record import record
def delete_customer():
    con=None
    cur=None
    try:
        print("\n" + "!" * 60)
        type_effect("        GDB BANK - ACCOUNT CLOSURE TERMINAL")
        print("!" * 60)
        con=get_connection()
        cur=con.cursor()
        account=""
        db_bal=""
        while True:
            try:
                account = input("\nEnter Account Number to Close (or '0' to cancel): ").strip()
                if account == "0":
                    return
                spinner_animation("Accessing Database Central...", duration=1)
                cur.execute("select acno,pin,bal,status,cname from bank where acno = %s",(account,))
                data=cur.fetchone()
                if data is None:
                    raise AccountNotFoundError
                db_acno, db_pin, db_bal, db_status, db_cname = data[0], data[1], data[2], data[3], data[4]
                if db_status.lower()=="closed":
                    raise InactiveAccountError
                elif float(db_bal)>0:
                    raise BalanceLessthanError
                else:
                    db_cname=data[4]
                    print(f"[+] Account Verified: {db_cname.upper()}")
                    break
            except AccountNotFoundError:
                print("Account not found in our records!")
            except InactiveAccountError:
                print(f"Account {"XXXX-XXXX"+account[-4:]} is already DEACTIVATED.")
            except BalanceLessthanError:
                print(f"\n[!] ALERT: Current Balance is ₹{db_bal}")
                print("Cannot close account with remaining balance. Settle dues first!")

        attempts=0
        while True:
            try:

                user_pin=input("Enter PIN Number :").strip()
                if user_pin!=str(db_pin):
                    raise InvalidPinError
                else:
                    break
            except InvalidPinError:
                attempts+=1
                if attempts==3:
                        print("\n[!!!] Maximum attempts reached. Transaction Terminated.")
                        return
                print(f"Invalid PIN! Please try again.")

        while True:
            confirm = input(f"Are you sure you want to close account of {db_cname.upper()}? (yes/no): ").lower().strip()
            if confirm == "no":
                print("Closure Cancelled.")
                return
            elif confirm == "yes":
                break
            else:
                print("Enter yes or no only")
        dt = datetime.now()
        loading_bar("Finalizing Audit & Deactivating Account", duration=0.02)
        cur.execute("update bank set status = 'CLOSED' , closing_date = %s where acno = %s",(dt,account))
        record(account,"CLOSURE",0.00,"Account Closed by Admin/Staff",cur)
        con.commit()
        print("\n" + "=" * 60)
        animation("SUCCESSFULLY DELETED CUSTOMER", duration=1)
        print(f"Closure Date: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
    except Exception as e:
        con.rollback()
        print("Technical Error:",e)
    finally:
        if con:
            cur.close()
            con.close()