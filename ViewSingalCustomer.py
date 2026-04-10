from BankDB import get_connection
from BankUtility import *

def view_singal_customer():
    con=None
    cur=None
    try:

        con=get_connection()
        cur=con.cursor()
        print("\n" + "=" * 60)
        type_effect(">>> ACCESSING RESTRICTED KYC DATA")
        print("=" * 60)
        account = input("\nEnter Target Account/Mobile: ").strip()
        loading_bar("Decrypting Profile Data", duration=0.01)
        cur.execute("select * from bank where acno = %s or mobile_number = %s",(account,account))
        data=cur.fetchone()
        if data is None:
            print("\n[!] ACCESS DENIED: Identity not found.")
        else:
            animation("Verifying Credentials", duration=1)
            print("\n" + "╔" + "═" * 58 + "╗")
            print(f"║{'CUSTOMER MASTER PROFILE':^58}║")
            print("╠" + "═" * 58 + "╣")
            print(f"  Account Number   : {data[0]}")
            print(f"  Customer Name    : {data[1].upper()}")
            print(f"  Mobile Number    : {data[2]}")
            print(f"  Email Address    : {data[3]}")
            print(f"  Aadhar ID        : {'XXXX-XXXX-' + data[4][-4:]}")  # Security masking
            print(f"  Nominee          : {data[5].upper()}")
            print(f"  IFSC Code        : {data[6]}")
            print(f"  Account Type     : {data[9].upper()}")
            print(f"  Current Balance  : ₹{data[8]:,.2f}")
            print(f"  Account Status   : {data[10].upper()}")
            print(f"  Opening Date     : {data[11]}")
            print("╚" + "═" * 58 + "╝")
    except Exception as e:
        print("Technical Error",e)
    finally:
        if con:
            con.close()
            cur.close()

