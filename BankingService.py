from Deposit import deposit
from Pin_Generate import pin_generate
from Withdraw import withdraw
from FundTransfer import fund_transfer
from TransactionHistory import transaction
from Pin_Update import pin_update
from CheckBalance import check_balance
def customer_banking():
    while True:
        print("\n" + "╔" + "═" * 45 + "╗")
        print(f"║{'GDB BANK - CUSTOMER SELF-SERVICE':^45}║")
        print("╠" + "═" * 45 + "╣")
        print("║ 1. 💰 Cash Deposit                        ║")
        print("║ 2. 💸 Cash Withdrawal                     ║")
        print("║ 3. 🔄 Fund Transfer                       ║")
        print("║ 4. 📜 Mini Statement (Last Transactions)  ║")
        print("║ 5. 🆕 Generate New PIN (First Time)       ║")
        print("║ 6. 🔑 Change Security PIN                 ║")
        print("║ 7. 🏦 Check Current Balance               ║")
        print("║ 8. 🚪 Exit & Remove Card                  ║")
        print("╚" + "═" * 45 + "╝")
        try:
            ch = input("Enter System Choice [1-4]: ").strip()
            if ch=='1':
                deposit()
            elif ch=='2':
                withdraw()
            elif ch=='3':
                fund_transfer()
            elif ch=='4':
                transaction()
            elif ch=='5':
                pin_generate()
            elif ch=='6':
                pin_update()
            elif ch=='7':
                check_balance()
            elif ch=='8':
                print("")
                return
            else:
                print("Enter Valid choice")
        except ValueError:
             print("\n[!] Error: Please enter a numeric value.")