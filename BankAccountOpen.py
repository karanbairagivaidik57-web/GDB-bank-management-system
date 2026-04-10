from Transaction_record import record
import re,random
from BankUtility import type_effect,progress_bar,spinner_animation,loading_bar,animation
from BankDB import get_connection
from BankExcept import NameError,MobileNumberError,EmailError,AadharCardError,BalanceError,SavcurError
def accountopen():
    print("\n"+"="*60)
    type_effect("\t\tWelcome to Global Digital Bank – Secure Banking")
    print("="*60)
    while True:
        try:

            name = input("\tEnter Full Name (As per Aadhar) :").strip().lower()
            if re.fullmatch(r"[a-zA-Z ]+",name):
                break
            else:
                raise NameError
        except NameError:
            print("\n[VALIDATION FAILED]: Name contains invalid characters. Use alphabets only.")
    while True:
        try:

            mobile_number=input("\tEnter 10-Digit Mobile Number: ")
            if re.fullmatch(r"[6-9][0-9]{9}",mobile_number):
                break
            else:
                raise MobileNumberError
        except MobileNumberError:
            print("\n[VALIDATION FAILED]: Invalid Mobile Number. Must be 10 digits starting with 6-9.")
    while True:
        try:

            email=input("\tEnter Email Address: ").strip().lower()
            if not email.endswith("@gmail.com") or not len(email)>10 or " " in email:
                raise EmailError
            else:
                break
        except EmailError:
            print("\n[VALIDATION FAILED]: Invalid Email Format. Only @gmail.com is allowed.")
    while True:
        try:

            aadhar=input("\tEnter 12-Digit Aadhar Card Number: ")
            if aadhar.isdigit() and len(aadhar)==12:
                break
            else:
                raise AadharCardError
        except AadharCardError:
            print("\n[VALIDATION FAILED]: Aadhar Verification Failed. Must be a 12-digit numeric code.")
    while True:
        try:

            nomiee=input("\tEnter Nominee Name: ").strip().lower()
            if re.fullmatch(r"[a-zA-Z ]+",nomiee):
                break
            else:
                raise NameError
        except NameError:
            print("\n[VALIDATION FAILED]: Name contains invalid characters. Use alphabets only.")
    while True:
        try:

            bal=float(input("\tEnter Balance at least 500 For Open Account :"))
            if bal>=500:
                break
            else:
                raise BalanceError
        except BalanceError:
            print(f"\n[TRANSACTION REJECTED]: Low Opening Balance. Minimum INR 500.00 required.")
    while True:
        try:

            acc_type=input("\tEnter Account Type (Saving/Current) :").strip().lower()
            if acc_type in ["saving","current"]:
                break
            else:
                raise SavcurError
        except SavcurError:
            print("\n[SYSTEM ERROR]: Unsupported Account Type. Please choose 'Saving' or 'Current'.")

    print("\n")
    progress_bar("Verifying Customer Details")
    spinner_animation("Connecting to Secure Server")
    con = None
    cur=None
    try:
        ifsc= "KARB0001234"
        status="Active"
        pin = random.randint(1000, 9999)
        bank_code="10"
        type_code="10" if acc_type=="saving" else "11"
        account=random.randint(1000000,99999999)
        acno=bank_code+type_code+str(account)
        con=get_connection()
        cur=con.cursor()
        loading_bar("Saving Information to Database")
        query="insert into bank(acno,cname,mobile_number,email_id,aadhaar_id,nominee,ifsc,pin,bal,acc_type,status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values=(acno,name,mobile_number,email,aadhar,nomiee,ifsc,pin,bal,acc_type,status)
        cur.execute(query,values)
        record(acno, "Credit", bal, "Opening Balance", cur)
        animation("Generating Account Number")
        print("\n" + "*" * 50)
        type_effect("          ACCOUNT CREATED SUCCESSFULLY          ")
        print("*" * 50)
        print(f" CUSTOMER NAME : {name.upper()}")
        print(f" ACCOUNT NO.   : ACC{acno}")
        print(f" IFSC CODE     : {ifsc}")
        print(f" ACCOUNT TYPE  : {acc_type.upper()}")
        print(f" TEMP PIN      : {pin}")
        print("-" * 50)
        print(" NOTE:Temporary PIN generated. Please visit Option 2 in PIN generate to update your PIN.")
        print("*" * 50 + "\n")
        con.commit()
    except Exception as e:
        print("Database Error:",e)
    finally:
            if cur:
                cur.close()
            if con:
                con.close()


