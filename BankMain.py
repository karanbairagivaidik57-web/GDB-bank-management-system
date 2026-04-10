from admin import admin_login
from BankMenu import menu
from BankingService import customer_banking
def main():
    while True:
        try:
            menu()
            ch=int(input("Enter Choice :"))
            match(ch):
                case 1:
                    admin_login()
                case 2:
                    customer_banking()
                case _:
                    print("Your Choice is Invalid ")
        except ValueError:
            print("Don't enter alpha numeric and spaces")
main()
