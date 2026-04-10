from BankDB import get_connection
from BankExcept import AccountNotFoundError,InactiveAccountError,InvalidPinError,NegativeNumberError,InvalidDenominationError,MobileNumberNotMatchError,NameError,MobileNumberError
from BankUtility import spinner_animation,type_effect,loading_bar,progress_bar,animation
from Transaction_record import record
from datetime import datetime,date
import re
def atm():
    con=None
    cur=None
    try:
        con=get_connection()
        cur=con.cursor()
        while True:
            try:
                account=input("Enter Account Number :").strip()
                cur.execute("select status,pin,bal,cname from bank where acno=%s",(account,))
                data=cur.fetchone()
                if data is None: raise AccountNotFoundError
                elif data[0].lower()=="closed":raise InactiveAccountError
                else:
                    spinner_animation("\t[#] READING CARD CHIP...")
                    db_pin,db_bal,db_name=data[1],data[2],data[3]
                    break
            except AccountNotFoundError:
                print("\t[!] ERROR: Card could not be read. Account not found.")
            except InactiveAccountError:
                print("\t[!] ALERT: This account is currently DEACTIVATED.")
                return
        attempts=0
        while True:
            try:
                user_pin=input("Enter PIN 4 Digit:").strip()
                progress_bar("\t[#] VERIFYING PIN")
                if str(db_pin)!=str(user_pin):
                    raise InvalidPinError
                else:
                    type_effect(f"\n\t[✓] ACCESS GRANTED. WELCOME {db_name.upper()}!")
                    break
            except InvalidPinError:
                attempts+=1
                if attempts>=3:
                    print("\t[!] SECURITY ALERT: Too many failed attempts.")
                    return
                print(f"\t[!] Incorrect PIN. ({3 - attempts} attempts left)")
        while True:
            try:

                amount = float(input("Enter Deposit Amount :"))
                if amount <= 0:
                    raise NegativeNumberError
                elif amount % 100 != 0:
                    raise InvalidDenominationError
                else:
                    loading_bar("\t[#] VERIFYING CURRENCY & COUNTING NOTES...")
                    break
            except NegativeNumberError:
                print("\t[!] Error: Amount must be greater than 0.")
            except InvalidDenominationError:
                print("\t[!] CDM Alert: Machine only accepts 100, 200, 500 notes.")
            except ValueError:
                print("\t[!] Error: Enter numeric value for amount.")
        total = float(db_bal) + amount
        cur.execute("update bank set bal = %s where acno = %s",(total,account))
        t_id=record(account,"Credit",amount,"CDM Cash Deposit",cur)
        animation("\t[#] DEPOSITING CASH TO YOUR ACCOUNT")
        con.commit()
        type_effect("\n\t[✓] CASH DEPOSITED SUCCESSFULLY!")
        dt = date.today()
        now = datetime.now()
        tm = now.strftime("%H:%M:%S")
        receipt=f"""
{"*" * 60}
        GLOBAL DIGITAL BANK
        ATM / CDM CASH DEPOSIT SLIP
{"*" * 60}
DATE: {dt}                      TIME: {tm}
{"-" * 60}
    TRANSACTION ID   : GDB-DEP-ATM-{t_id}
    ACCOUNT NUMBER   : XXXXXXXX{account[-4:]}
    CUSTOMER NAME    : {db_name.upper()}

    TYPE             : CASH DEPOSIT (CDM)
    AMOUNT           : {amount:,.2f}
    STATUS           : SUCCESSFUL
{"-" * 60}
    TOTAL BALANCE    : ₹{total}
{"-" * 60}
    Keep your receipt for your records. Thank You!
{"*" * 60}
"""
        print(receipt)
    except Exception as e:
        if con:
            con.rollback()
            print("\n" + "=" * 60)
            print("\t[!] TRANSACTION DECLINED")
            print(f"\t[!] SYSTEM MESSAGE: {e}")
            print("\t[!] STATUS: NO AMOUNT DEDUCTED. PLEASE TRY AGAIN.")
            print("=" * 60 + "\n")
    finally:
        if con:
            cur.close()
            con.close()


def counter():
    depositer_name = ""
    depositer_phone = ""
    remark=""
    final_name=""
    final_number=""
    con=None
    cur=None
    try:
        con=get_connection()
        cur=con.cursor()
        while True:
            try:
                account=input("Enter Account Number :").strip()
                spinner_animation("\r\t[#] ACCESSING CENTRAL DATABASE")
                cur.execute("select cname,status,bal,mobile_number from bank where acno = %s",(account,))
                data=cur.fetchone()
                if data is None:
                    raise AccountNotFoundError
                elif data[1].lower()=="closed":
                    raise InactiveAccountError
                else:
                    db_name,db_bal,db_number=data[0],data[2],data[3]
                    type_effect(f"\t[✓] ACCOUNT FOUND: {db_name.upper()}")
                    break
            except AccountNotFoundError:
                print("\r\t[!] ERROR: Account not found in our records.")
            except InactiveAccountError:
                print("\t[!] ALERT: This account is currently DEACTIVATED.")
                return
        while True:
            confirm_name = input(f"Is This Account Holder [{db_name}] (Yes/No) :").lower()
            if confirm_name=="no":
                print("\t[!] Transaction Cancelled by User.")
                return
            elif confirm_name!="yes":
                print("\t[!] Please enter valid Yes/No only.")
            else:
                break
        while True:
            try:
                confirm = input("Are You The Account Holder (Yes/No) :").lower().strip()
                if confirm=="yes":
                    mobile_number=input("Enter Your Mobile Number :").strip()
                    progress_bar("\t[#] VERIFYING REGISTERED MOBILE")
                    if mobile_number!=str(db_number):
                        raise MobileNumberNotMatchError

                    else:
                        type_effect("\t[✓] IDENTITY VERIFIED SUCCESSFULLY.")
                        break
                elif confirm=="no":
                    while True:
                        try:
                            depos_name=input("Enter Your Name :").strip()
                            depos_mobile=input("Enter Mobile Number :").strip()
                            if not re.fullmatch(r"[A-Za-z ]+",depos_name):
                                raise NameError
                            elif not re.fullmatch(r"[6-9][0-9]{9}",depos_mobile):
                                raise MobileNumberError
                            else:
                                depositer_name=depos_name
                                depositer_phone=depos_mobile
                                break
                        except NameError:
                            print("\t[!] Invalid Name. Use alphabets only.")
                        except MobileNumberError:
                            print("\t[!] Invalid Mobile. Enter 10 digits starting with 6-9.")
                    break
                elif confirm!="yes":
                    print("\t[!] Please Enter Valid Choice (Yes/No).")
                else:
                    break
            except MobileNumberNotMatchError:
                print("\t[!] SECURITY ALERT: Mobile number does not match our records.")

        while True:
            try:

                amount=float(input("Enter Deposit Amount :"))
                if amount<=0:
                    raise NegativeNumberError
                else:
                    loading_bar("\t[#] CASHIER VERIFYING CASH & CURRENCY", 0.02)
                    break
            except NegativeNumberError:
                print("\t[!] Error: Amount must be greater than 0.")
            except ValueError:
                print("\t[!] Error: Please enter numeric value for amount.")
        if confirm=="yes":
            final_name=db_name
            final_number=db_number
            remark="Self Cash Deposit"
        elif confirm=="no":
            final_name=depositer_name
            final_number=depositer_phone
            remark="Third Party Deposit"
        total=float(db_bal)+amount
        cur.execute("update bank set bal = %s where acno  = %s",(total,account))
        t_id=record(account,"Deposit",amount,remark,cur,final_name.upper(),final_number)
        con.commit()
        dt=date.today()
        now=datetime.now()
        tm=now.strftime("%H:%M:%S")
        animation("\t[#] FINALIZING TRANSACTION & GENERATING SLIP")
        receipt = f"""
        {"=" * 65}
                   GLOBAL DIGITAL BANK.
        {"=" * 65}
           DATE: {dt}                              TIME: {tm}
           BRANCH: MAIN CITY BRANCH                GDB-DEP-CTR-{t_id}
        {"-" * 65}
           ACCOUNT NUMBER    : XXXXXXXX{account[-4:]}
           ACCOUNT HOLDER    : {db_name.upper()}

           TRANSACTION TYPE  : CASH DEPOSIT (COUNTER)
           AMOUNT            : ₹{amount:.2f}
           STATUS            : SUCCESSFUL / POSTED
        {"-" * 65}
           DEPOSITED BY      : {final_name.upper()} 
           CONTACT NUMBER    : {final_number}
        {"-" * 65}
           TOTAL BALANCE     : ₹{total:.2f}
        {"-" * 65}

           This is a computer-generated acknowledgement. 
           [ STAMPED & VERIFIED BY CASHIER ]
        {"=" * 65}
        """
        print(receipt)
    except Exception as e:
        if con:
            con.rollback()
            print("\n" + "!" * 65)
            print("\t[!] TRANSACTION FAILED: TECHNICAL ERROR")
            print(f"\t[!] ERROR DETAILS: {e}")
            print("\t[!] STATUS: ANY CASH TAKEN WILL BE RETURNED IMMEDIATELY.")
            print("\t[!] PLEASE CONTACT THE BRANCH MANAGER.")
            print("!" * 65 + "\n")
    finally:
        if con:
            cur.close()
            con.close()



def deposit():
    while True:
        try:

            print("\n" + "=" * 50)
            print("          CENTRAL DIGITAL BANK - DEPOSIT SECTION")
            print("=" * 50)
            print("1.\tATM / CDM (Self-Service)")
            print("2.\tCounter (Branch-Service)")
            print("-" * 50)
            ch=input("Enter Your Choice :").strip()
            if ch=="1":
                atm()
                break
            elif ch=="2":
                counter()
                break
            else:
                print("\t[!] Invalid Choice! Please select 1, 2, or 3.")
        except ValueError:
            print("\t[!] Error: Please enter a numeric choice only.")






































