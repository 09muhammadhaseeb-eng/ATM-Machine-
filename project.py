"""Console version of the ATM Machine (same logic as the Streamlit app)."""
balance = 5000
pin = "1234"
name = "Muhammad Haseeb"
account_number = "1234567890"

if input("Enter PIN: ") == pin:
    while True:
        print("\nATM MACHINE")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Account Details")
        print("5. Exit")

        choice = input("\nChoose: ")

        if choice == "1":
            print(f"Balance: Rs.{balance}")
        elif choice == "2":
            amount = float(input("Enter amount: Rs."))
            balance += amount
            print(f"Deposited: Rs.{amount}")
            print(f"New Balance: Rs.{balance}")
        elif choice == "3":
            amount = float(input("Enter amount: Rs."))
            if amount <= balance:
                balance -= amount
                print(f"Withdrawn: Rs.{amount}")
                print(f"Remaining Balance: Rs.{balance}")
            else:
                print("Insufficient balance.")
        elif choice == "4":
            print(f"Name: {name}")
            print(f"Account Number: {account_number}")
        elif choice == "5":
            print("Thank you for using the ATM.")
            break
        else:
            print("Invalid choice.")
else:
    print("Wrong PIN.")
