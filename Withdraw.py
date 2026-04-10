from BankDB import get_connection
from Transaction_record import record
from BankUtility import spinner_animation, type_effect, loading_bar, progress_bar, animation
from datetime import datetime,date
import re
from BankExcept import AccountNotFoundError,InvalidPinError,InactiveAccountError,NegativeNumberError,InvalidDenominationError,InsufficientError,MinimumBalanceError,AmountError,NameError,MobileNumberError,AadhaarCardError
def atm():
    con=None
    cur=None
    try:
        con=get_connection()
        cur=con.cursor()
        while True:
            try:
                account = input("\n[#] Please Enter/Swipe Account Number: ").strip()
                spinner_animation("\t[#] READING CARD CHIP")
                cur.execute("select pin,status,cname,bal from bank where acno = %s",(account,))
                data=cur.fetchone()
                if data is None:
                    raise AccountNotFoundError
                elif data[1].lower()=="closed":
                    raise InactiveAccountError
                else:
                    db_pin,db_name,db_bal=data[0],data[2],data[3]
                    type_effect(f"\t[✓] WELCOME, {db_name.upper()}")
                    break
            except AccountNotFoundError:
                print("\t[!] ERROR: Card could not be read. Account not found.")
            except InactiveAccountError:
                print("\t[!] ALERT: This account is currently DEACTIVATED/CLOSED.")
                return
        attempts=0
        while True:
            try:
                user_pin = input("\n[#] Enter 4-Digit Secret PIN: ").strip()
                progress_bar("\t[#] AUTHENTICATING")
                if user_pin!=str(db_pin):
                    raise InvalidPinError
                else:
                    type_effect("\t[✓] ACCESS GRANTED.")
                    break
            except InvalidPinError:
                attempts+=1
                if attempts>=3:
                    print("\t[!] SECURITY ALERT: 3 Failed Attempts. Card Blocked for 24 hours.")
                    return
                print(f"\t[!] Incorrect PIN. {3 - attempts} attempts left.")

        while True:
            try:
                amount = float(input("[#] Enter Withdrawal Amount: "))
                if amount<=0:
                    raise NegativeNumberError
                elif amount%100!=0:
                    raise InvalidDenominationError
                elif amount>float(db_bal):
                    raise InsufficientError
                elif (float(db_bal) - amount) < 500:
                    raise MinimumBalanceError

                elif amount>20000:
                    raise AmountError
                else:
                    loading_bar("\t[#] PROCESSING CASH & COUNTING NOTES", 0.04)
                    break
            except NegativeNumberError:
                print("\t[!] Error: Amount must be greater than 0.")
            except InvalidDenominationError:
                print("\t[!] CDM Alert: Please enter amount in multiples of 100/500/2000.")
            except InsufficientError:
                print("\t[!] ERROR: Insufficient funds in your account.")
            except MinimumBalanceError:
                print("\t[!] ERROR: Transaction Declined. Minimum balance of ₹500 must remain.")
            except AmountError:
                print("\t[!] LIMIT EXCEEDED: Maximum ₹20,000 allowed per transaction.")
            except ValueError:
                print("\t[!] Error: Please enter numeric value only.")
        total=float(db_bal)-amount
        cur.execute("update bank set bal = %s where acno = %s",(total,account,))
        t_id=record(account,"Debit",amount,"ATM Cash Withdrawal",cur)
        animation("\t[#] FINALIZING TRANSACTION")
        type_effect("\t[✓] TRANSACTION SUCCESSFUL. PLEASE COLLECT YOUR CASH.")
        dt=date.today()
        now=datetime.now()
        tm=now.strftime("%H:%M:%S")
        receipt = f"""
{"*" * 60}
            GLOBAL DIGITAL BANK.
            ATM WITHDRAWAL ADVICE
{"*" * 60}
    DATE: {dt}                      TIME: {tm}
    ATM ID: CDB_MUM_042             GDB-WDR-ATM-{t_id}
{"-" * 60}
    CARD NUMBER      : XXXXXXXX{account[-4:]}
    CUSTOMER NAME    : {db_name.upper()}
    
    TRANSACTION      : CASH WITHDRAWAL
    AMOUNT           : ₹{amount:,.2f}
    STATUS           : SUCCESSFUL
{"-" * 60}
    AVAILABLE BAL    : ₹{total:,.2f}
{"-" * 60}
        Please count your cash before leaving.
        Thank you for using our ATM!
{"*" * 60}
        """
        print(receipt)
        con.commit()
    except Exception as e:
        if con:
            con.rollback()
            print("\n" + "=" * 60)
            print("\t[!] TRANSACTION DECLINED")
            print(f"\t[!] SYSTEM ERROR: {e}")
            print("\t[!] STATUS: NO AMOUNT DEDUCTED. PLEASE CONTACT BRANCH.")
            print("=" * 60 + "\n")
    finally:
        if con:
            cur.close()
            con.close()

def counter():
    con=None
    cur=None
    withdraw_name=""
    withdraw_mobile=""
    remark=""
    try:
        con=get_connection()
        cur=con.cursor()
        while True:
            try:
                account=input("Enter Account Number :").strip()
                spinner_animation("\t[#] ACCESSING BANK DATABASE")  # Animation 1
                cur.execute("select status,bal, aadhaar_id,cname,mobile_number from bank where acno  = %s",(account,))
                data=cur.fetchone()
                if data is None:
                    raise AccountNotFoundError
                elif data[0].lower()=="closed":
                    raise InactiveAccountError
                else:
                    db_bal,db_id,db_name,db_number=data[1],data[2],data[3],data[4]
                    type_effect(f"\t[✓] ACCOUNT FOUND: {db_name.upper()}")
                    break
            except AccountNotFoundError:
                print("\t[!] ERROR: Account number does not exist.")
            except InactiveAccountError:
                print("\t[!] ALERT: This account is CLOSED. Withdrawal not permitted.")
                return
        while True:
            is_holder = input("\n[?] Are you the Account Holder? (Yes/No): ").lower().strip()
            if is_holder=="no":
                while True:
                    cheque = input("\t[?] Do you have an Authorized Cheque? (Yes/No): ").lower().strip()
                    if cheque=="yes":
                            try:
                                name = input("\t[#] Enter Bearer (Your) Name: ").strip()
                                mobile = input("\t[#] Enter Bearer Mobile Number: ").strip()
                                if not re.fullmatch(r"[a-zA-Z ]+",name):
                                    raise NameError
                                elif not re.fullmatch(r"[6-9][0-9]{9}",mobile):
                                    raise MobileNumberError
                                else:
                                    withdraw_name=name
                                    withdraw_mobile=mobile
                                    break
                            except NameError:
                                print("\t[!] Invalid Name format.")
                            except MobileNumberError:
                                print("\t[!] Invalid Mobile Number.")
                    elif cheque=="no":
                        print("\t[!] POLICY: Third-party withdrawal without cheque is strictly prohibited.")
                        return
                    else:
                        print("Please Enter Valid Choice Yes/No only")
                break
            elif is_holder=="yes":
                spinner_animation("\t[#] VERIFYING SIGNATURE FROM RECORDS")
                type_effect("\t[✓] SIGNATURE MATCHED.")
                break
            else:
                print("\t[!] Please enter 'Yes' or 'No'.")
        while True:
            try:
                amount = float(input("[#] Enter Withdrawal Amount: "))
                if amount<=0:
                    raise NegativeNumberError
                elif amount>float(db_bal):
                    raise InsufficientError
                elif float(db_bal)-amount <500:
                    raise AmountError
                elif amount>=50000:
                    print("\t[!] High-Value Transaction detected (Above ₹50,000).")
                    user_id = input("\t[#] Enter Aadhaar Number for KYC: ").strip()
                    if user_id!=str(db_id):
                        raise AadhaarCardError
                    else:
                        loading_bar("\t[#] AUTHORIZING CASH DISBURSEMENT", 0.05)
                        break
                else:
                    break
            except NegativeNumberError:
                print("\t[!] Amount must be positive.")
            except InsufficientError:
                print("\t[!] ERROR: Insufficient Balance.")
            except AmountError:
                print("\t[!] ERROR: Must maintain min. ₹500 balance.")
            except AadhaarCardError:
                print("\t[!] SECURITY ALERT: Aadhaar Verification Failed. Transaction Terminated.")
                return
            except ValueError:
                print("Don't Alpha Numeric and Spaces.")

        total=float(db_bal)-amount
        if is_holder=="yes":
            final_name=db_name
            final_number=db_number
            remark="Cash Withdrawal (Self)"
        else:
            final_name=withdraw_name
            final_number=withdraw_mobile
            remark="Cash Withdrawal by Third Party (Cheque)"
        cur.execute("update bank set bal = %s where acno = %s",(total,account))
        t_id=record(account,"Debit",amount,remark,cur,final_name,final_number)
        type_effect("\t[✓] TRANSACTION COMPLETED SUCCESSFULLY.")
        dt=date.today()
        now=datetime.now()
        tm=now.strftime("%H:%M:%S")
        receipt = f"""
{"=" * 65}
                   GLOBAL DIGITAL BANK
                   CASH WITHDRAWAL SLIP
{"=" * 65}
    DATE: {dt}           TIME: {tm}          GDB-WDR-CTR-{t_id}
    BRANCH: MAIN CITY BRANCH                     CASHIER ID: CSH_01
{"-" * 65}
   ACCOUNT NUMBER    : XXXXXXXX{account[-4:]}
   ACCOUNT HOLDER    : {db_name.upper()}
   RECEIVED BY       : {final_name.upper()}
   
   TRANSACTION TYPE  : CASH WITHDRAWAL (COUNTER)
   WITHDRAWAL AMOUNT : ₹{amount:,.2f}
   STATUS            : DISBURSED / SUCCESSFUL
{"-" * 65}
    AVAILABLE BALANCE : ₹{total:,.2f}
{"-" * 65}

        [ SIGNATURE ]                         [ BANK STAMP ]
        ( {final_name.upper()} )                ( AUTHORIZED )

{"=" * 65}
        Note: Please verify the cash before leaving the counter.
{"=" * 65}
"""
        con.commit()
        print(receipt)

    except Exception as e:
        if con: con.rollback()
        print(f"\n\t[!] SYSTEM ERROR: {e}")
    finally:
        if con:
            cur.close()
            con.close()


def withdraw():
    while True:
        print("-"*60)
        print("\t1.ATM Cash Withdrawal")
        print("\t2.Counter Withdrawal")
        print("-"*60)
        ch=input("Enter Choice :").strip()
        if ch=='1':
            atm()
            break
        elif ch=='2':
            counter()
            break
        else:
            print("\t[!] Invalid Choice! Please select 1, 2, or 3.")