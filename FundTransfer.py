from BankUtility import spinner_animation,loading_bar,animation,type_effect,progress_bar
from BankDB import get_connection
from BankExcept import *
from Transaction_record import record
from datetime import datetime,date


def fund_transfer():
    cur=None
    con=None
    try:
        con = get_connection()
        cur=con.cursor()
        while True:
            try:
                sender_account = input("\n[#] Enter Your Account Number: ").strip()
                spinner_animation("\t[#] FETCHING ACCOUNT DETAILS")
                cur.execute("select acno,pin,status,bal,cname from bank where acno = %s",(sender_account,))
                data=cur.fetchone()
                if data is None:
                    raise AccountNotFoundError
                elif data[2].lower()=="closed":
                    raise InactiveAccountError
                else:
                    s_pin,s_bal,s_cname,s_acno=data[1],data[3],data[4],data[0]
                    type_effect(f"\t[✓] WELCOME, {s_cname.upper()}")
                    break
            except AccountNotFoundError:
                print("\t[!] ERROR: Sender account not found.")
            except InactiveAccountError:
                print("\t[!] ALERT: Your account is CLOSED. Transfers not allowed.")
                return
        attempts=0
        while True:
            try:
                user_pin = input("\n[#] Enter 4-Digit Secret PIN: ").strip()
                progress_bar("\t[#] AUTHENTICATING")
                if user_pin!=str(s_pin):
                    raise InvalidPinError
                else:
                    type_effect("\t[✓] IDENTITY VERIFIED.")
                    break
            except InvalidPinError:
                attempts+=1
                if attempts>=3:
                    print("\t[!] SECURITY ALERT: 3 Failed Attempts. Transaction Terminated.")
                    return
                print(f"\t[!] Incorrect PIN. {3 - attempts} attempts left.")
        while True:
            try:
                receiver_account = input("\n[#] Enter Receiver Account Number: ").strip()
                cur.execute("select acno,bal,cname,status from bank where acno = %s",(receiver_account,))
                data=cur.fetchone()
                if data is None:
                    raise AccountNotFoundError
                elif data[3].lower()=='closed':
                    raise InactiveAccountError
                elif s_acno==receiver_account:
                    raise  AccountsameError
                else:
                    r_bal, r_cname, r_acno = data[1], data[2], data[0]
                    spinner_animation("\t[#] VERIFYING RECEIVER ACCOUNT")
                    break
            except AccountNotFoundError:
                print("\t[!] ERROR: Receiver account does not exist.")
            except InactiveAccountError:
                print("\t[!] ERROR: Receiver account is currently INACTIVE.")
            except AccountsameError:
                print("\t[!] ERROR: You cannot transfer money to your own account.")
        while True:
            confirm = input(f"\n[?] Transfer ₹ to {r_cname.upper()}? (Yes/No): ").lower().strip()
            if confirm=="no":
                print("\t[!] TRANSACTION CANCELLED BY USER.")
                return
            elif confirm == "yes":
                break
            else:
                print("\t[!] Please enter 'Yes' or 'No'.")
        while True:
            try:
                amount = float(input("\n[#] Enter Amount to Transfer: "))
                if amount<=0:
                    raise NegativeNumberError
                elif float(s_bal)-amount<500:
                    raise MinimumBalanceError
                else:
                    break
            except NegativeNumberError:
                print("\t[!] ERROR: Amount must be positive.")
            except MinimumBalanceError:
                print("\t[!] ERROR: Insufficient Balance. Must maintain ₹500 minimum.")
            except ValueError:
                print("\t[!] ERROR: Please enter a valid numeric amount.")
        loading_bar("\t[#] SECURELY TRANSFERRING FUNDS", 0.05)
        sender_amount=float(s_bal)-amount
        receiver_amount=float(r_bal)+amount
        cur.execute("update bank set bal = %s where acno = %s",(sender_amount,sender_account))
        cur.execute("update bank set bal = %s where acno = %s",(receiver_amount,receiver_account))
        t_id=record(s_acno,"Debit",amount,f"Transfer To {r_acno}",cur,s_cname)
        record(r_acno,"Credit",amount,f"Transfer From {s_acno}",cur,r_cname)
        con.commit()
        animation("\t[#] GENERATING TRANSACTION ADVICE")
        type_effect("\t[✓] FUND TRANSFER SUCCESSFUL!")
        dt=date.today()
        now=datetime.now()
        tm=now.strftime("%H:%M:%S")
        receipt = f"""
{"=" * 65}
            GLOBAL DIGITAL BANK - FUND TRANSFER ADVICE
{"=" * 65}
  DATE: {dt}           TIME: {tm}           TXN ID: GDB-FT-{t_id}
{"-" * 65}
  FROM (SENDER)      : {s_cname.upper()}
  SENDER A/C         : XXXXXXXX{s_acno[-4:]}

  TO (RECEIVER)      : {r_cname.upper()}
  RECEIVER A/C       : XXXXXXXX{r_acno[-4:]}
{"-" * 65}
  TRANSFER AMOUNT    : ₹{amount:,.2f}
  TRANSACTION TYPE   : INTER-BANK FUND TRANSFER
  STATUS             : SUCCESSFUL / POSTED
{"-" * 65}
  CURRENT BALANCE    : ₹{sender_amount:,.2f}
{"-" * 65}
    Thank you for using Global Digital Bank Online Services!
{"=" * 65}
"""
        print(receipt)

    except Exception as e:
        if con: con.rollback()
        print(f"\n\t[!] TECHNICAL ERROR: {e}")
    finally:
        if con:
            cur.close()
            con.close()
