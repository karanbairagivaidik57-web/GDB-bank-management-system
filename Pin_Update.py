from BankUtility import type_effect,spinner_animation,loading_bar,animation
from BankExcept import AccountNotFoundError,InvalidPinError,InactiveAccountError
from BankDB import get_connection
def pin_update():
    print("\n" + "="*60)
    type_effect("\tSECURITY CENTER: PIN UPDATE SERVICE")
    print("="*60)
    con=None
    cur=None
    try:
        con=get_connection()
        cur=con.cursor()
        while True:
            try:
                account=input("Enter Account Number :").strip()
                query="select pin,status from bank where acno=%s"
                value=(account,)
                cur.execute(query,value)
                data=cur.fetchone()
                if data is None:
                    raise AccountNotFoundError
                elif data[1].lower()=="closed":
                    raise InactiveAccountError
                else:
                    spinner_animation("\t[#] ACCESSING ENCRYPTED DATABASE...")
                    db_pin=data[0]
                    break
            except AccountNotFoundError:
                print("\t[!] SECURITY ALERT: Account Number not found in our records.")
            except InactiveAccountError:
                print("\t[!] ACCESS DENIED: This account has been deactivated or closed.")
                return
        attempts=0
        while True:
            try:

                user_pin=input("Enter Old PIN :").strip()
                if str(db_pin)!=user_pin:
                    raise InvalidPinError
                spinner_animation("\t[#] VERIFYING CREDENTIALS...")
                break
            except InvalidPinError:
                attempts+=1
                if attempts>=3:
                    print("\t[!] TOO MANY INVALID ATTEMPTS!")
                    spinner_animation("\t[#] ACCOUNT TEMPORARILY LOCKED. PLEASE WAIT", duration=30)
                    attempts = 0
                else:
                    print(f"\t[!] ACCESS DENIED: Incorrect PIN.")


        while True:
            new_pin=input("Enter PIN 4 Digit :").strip()
            confirm_pin=input("Enter Confirm PIN :").strip()
            if new_pin!=confirm_pin:
                print("\t[!] VALIDATION ERROR: PIN confirmation does not match. Please re-enter.")
            elif len(new_pin)!=4 or not new_pin.isdigit():
                print("\t[!] SYSTEM NOTICE: PIN must be a 4-digit numeric code only.")
            elif new_pin==str(db_pin):
                print("\t[!] POLICY VIOLATION: New PIN cannot be identical to the Old PIN.")
            else:
                break
        print("\t" + "-" * 40)
        loading_bar("\t[#] SYNCHRONIZING NEW SECURITY KEY")
        query="update bank set pin=%s where acno=%s"
        value=(new_pin,account)
        cur.execute(query,value)
        con.commit()
        animation("\t[#] UPDATING SERVER RECORDS")
        print("\n" + "*" * 60)
        type_effect("\t✔ PIN UPDATED SUCCESSFULLY!")
        print("\n\t" + "═" * 45)
        print("\t      OFFICIAL SECURITY RECEIPT")
        print("\t" + "═" * 45)
        print(f"\t ACCOUNT      : XXXXXXX{account[-4:]}")
        print("\t SERVICE      : PIN RE-GENERATION")
        print("\t STATUS       : SUCCESSFUL / ENCRYPTED")
        print("\t REMARK       : PIN UPDATED SECURELY")
        print("\t" + "═" * 45)
        print("\t   Thank you for choosing Secure Banking")
        print("\t" + "═" * 45 + "\n")
        print("\tNOTICE     : Never share your PIN with anyone.")
        print("*" * 60 + "\n")
    except ValueError:
        print("\t[!] INPUT ERROR: Alphanumeric characters or spaces are not allowed.")
    except Exception as e:
        print("Error :",e)
    finally:
        if con:
            cur.close()
            con.close()
