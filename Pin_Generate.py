from BankDB import get_connection
from BankExcept import AccountNotFoundError,InvalidPinError,InactiveAccountError
from BankUtility import spinner_animation,loading_bar,animation,type_effect
import random
def pin_generate():
    print("\n" + "═" * 60)
    type_effect("\tCENTRAL BANK: SECURE PIN GENERATION SERVICE")
    print("═" * 60)
    con=None
    cur=None
    try:
        con=get_connection()
        cur=con.cursor()
        while True:
            try:
                account=input("\nEnter Registered Account Number:").strip()
                query="select status,pin from bank where acno=%s"
                value=(account,)
                cur.execute(query,value)
                data=cur.fetchone()
                if data is None:
                    raise AccountNotFoundError
                elif data[0].lower()=="closed":
                    raise InactiveAccountError
                else:
                    spinner_animation("\t[#] SCANNING CORE BANKING DATABASE")
                    db_pin=data[1]
                    break
            except AccountNotFoundError:
                print("\t[!] ERROR: Account details not found in our records.")
            except InactiveAccountError:
                print("\t[!] ALERT: This account is currently DEACTIVATED.")
                return

        while True:
            try:
                user_pin=input("Enter your Temporary/Existing PIN:")
                if str(db_pin)!=str(user_pin):
                    raise InvalidPinError
                else:
                    spinner_animation("\t[#] AUTHENTICATING SECURE SESSION")
                    break
            except InvalidPinError:
                print("\t[!] ACCESS DENIED: Incorrect PIN. Please try again.")
        print("\n\t" + "-" * 40)
        type_effect("\t[i] INITIATING RANDOM PIN ALGORITHM...")
        loading_bar("\t[#] GENERATING 256-BIT ENCRYPTION")
        new_pin=random.randint(1000,9999)
        loading_bar("\t[#] SYNCHRONIZING WITH SERVER")
        query="update bank set pin=%s where acno=%s"
        value=(new_pin,account)
        cur.execute(query,value)
        con.commit()
        animation("\t[#] FINALIZING SYSTEM RECORDS")
        print("\n" + "=" * 60)
        print("\t      SECURE SYSTEM-GENERATED RECEIPT")
        print("\n"+"=" * 60)
        print(f"\t ACCOUNT      : XXXXXXX{account[-4:]}")
        print("\t SERVICE      : AUTO PIN GENERATION")
        print("\t STATUS       : SUCCESSFUL")
        print("\t" + "─" * 45)
        print(f"\t >>> NEW PERMANENT PIN: [ {new_pin} ] <<<")
        print("\t" + "─" * 45)
        print("\t SECURITY TIP : Memorize this PIN immediately.")
        print("=" * 60 + "\n")
        print("Please keep it secret for security reasons.")
    except Exception as e:
        print("Error",e)
    finally:
        cur.close()
        con.close()

