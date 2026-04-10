from BankDB import get_connection
from BankExcept import AccountNotFoundError, InvalidPinError,InactiveAccountError

from BankUtility import *
def check_balance():
    con=None
    cur=None
    try:
        con=get_connection()
        cur=con.cursor()
        print("\n" + "═" * 60)
        type_effect(f"║{'SYSTEM: SECURE BALANCE ENQUIRY SERVICE':^58}║")
        print("═" * 60)
        while True:
            try:
                account = input("\nEnter Registered Account Number: ").strip()
                spinner_animation("\t[#] SEARCHING DATABASE...")
                cur.execute("select acno,pin,bal,status,cname,acc_type from bank where acno = %s",(account,))
                data=cur.fetchone()
                if data is None:
                    raise AccountNotFoundError
                elif data[3].lower() == "closed":
                    raise InactiveAccountError
                else:
                    db_acno,db_pin,db_bal,db_status,db_name,db_type=data[0],data[1],data[2],data[3],data[4],data[5]
                    break
            except AccountNotFoundError:
                print("\t[!] ERROR: Account not found. Please check the number.")
            except InactiveAccountError:
                print("\t[!] ALERT: This account is CLOSED. Access denied.")
                return
        attempts=0
        while True:
            try:
                user_pin=input("Enter PIN Number :").strip()
                if user_pin!=str(db_pin):
                    raise InvalidPinError
                else:
                    spinner_animation("\t[#] AUTHENTICATING...")
                    break
            except InvalidPinError:
                attempts+=1
                print(f"\t[!] ACCESS DENIED: Incorrect PIN. (Attempt {attempts})")
                if attempts >= 3:
                    print("\t[!] SECURITY BREACH: Too many attempts. Returning to menu.")
                    return

        loading_bar("\t[#] FETCHING REAL-TIME BALANCE")
        print("\n" + "╔" + "═" * 58 + "╗")
        print(f"║{'GDB BANK OFFICIAL STATEMENT':^58}║")
        print("╠" + "═" * 58 + "╣")
        print(f"  HOLDER    : {db_name.upper()}")
        print(f"  ACCOUNT   : XXXXXXX{account[-4:]}")
        print(f"  TYPE      : {db_type.upper()}")
        print("  " + "-" * 54)
        print(f"  NET BALANCE : INR {db_bal:,.2f}")
        print("  " + "-" * 54)
        print(f"  A/C STATUS  : {db_status.upper()}")
        print("╚" + "═" * 58 + "╝")
        print(f"{'*** Keep your PIN secret ***':^60}\n")
    except Exception as e:
        print("Technical Error",e)
    finally:
        if con:
            cur.close()
            con.close()
