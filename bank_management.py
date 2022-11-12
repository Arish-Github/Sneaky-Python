import mysql.connector as sql
import tabulate as tbl

connector = sql.connect(host="localhost", user="root", passwd="qwerty", database="op_db")
cursor = connector.cursor()


def more_ops():
    more = input("\nWant to do more operations? (y/n): ").lower()
    if more == 'y':
        ask_choices()
    elif more == 'n':
        connector.close()
    else:
        print("Enter y/n")
        more_ops()


def view_user_profile():
    acc_no = int(input("Enter the account number: "))
    cursor.execute("select account_number from bank_management")
    account_numbers = cursor.fetchall()

    abc = []
    for i in account_numbers:
        abc.append(i[0])

    if acc_no in abc:
        cursor.execute(f"select * from bank_management where account_number = {acc_no}")
        data = cursor.fetchall()

        acc_details = tbl.tabulate(data,
                                   headers=['Account NUmber', 'Name', 'Gender', 'Age', 'DOB', 'Aadhar Number',
                                            'Address', 'Phone Number', 'Account Balance'])

        print(acc_details)

    else:
        print(f"The account number {acc_no} does not exist. Try again!!\n")
        view_user_profile()

    more_ops()


def view_all():
    cursor.execute("select * from bank_management")
    data = cursor.fetchall()

    table = tbl.tabulate(data,
                         headers=['Account NUmber', 'Name', 'Gender', 'Age', 'DOB', 'Aadhar Number', 'Address',
                                  'Phone Number', 'Account Balance'])
    print(table)

    more_ops()


def add_account():
    name = input("Enter your full name: ")
    gender = input("Enter you gender (M/F): ")
    age = int(input("Enter your age: "))
    dob = input("Enter your date of birth (YYYY-MM-DD): ")
    aadhar = int(input("Enter your aadhar card number: "))
    address = input("Enter your residential address: ")
    phone = int(input("Enter your phone number: "))
    money_added = int(input("Amount of money added while opening account: "))

    cursor.execute("select max(account_number) from bank_management")
    new_account_no = cursor.fetchall()[0][0] + 1

    cursor.execute(
        f"insert into bank_management values({new_account_no}, '{name}', '{gender}', {age}, '{dob}', {aadhar}, '{address}', {phone}, {money_added})")
    print(f"Account added successfully!!\nYour account number is: {new_account_no}")

    more_ops()


def remove_account():
    acc_no = int(input("\nEnter the account number of the account to be removed: "))
    cursor.execute("select account_number from bank_management")
    accounts = cursor.fetchall()
    accounts_again = []
    for i in accounts:
        accounts_again.append(i[0])

    if acc_no in accounts_again:
        confirmation = input("Are you sure you want to remove this account? (y/n): ")
        if confirmation == 'y':
            cursor.execute(f"delete from bank_management where Account_Number = {acc_no}")
            print(f"Account with account number {acc_no} has been removed.\n")
        elif confirmation == 'n':
            print("Okay, not removing that account for now...")
        else:
            print("You can only enter either y or n...\nTry again")
            remove_account()
    else:
        print(f"The account number {acc_no} does not exist.\nTry again...")
        remove_account()

    more_ops()


def update_account_info():
    acc_no = int(input("Enter the account number of the account you want to update: "))
    cursor.execute("select account_number from bank_management")
    data = cursor.fetchall()
    accounts = []
    for i in data:
        accounts.append(i[0])
    if acc_no in accounts:
        what = int(input("""Enter what you want to update: 
                         1. Name
                         2. Gender
                         3. Age
                         4. DOB
                         5. Aadhar Number
                         6. Address
                         7. Phone Number"""))
        if what == 1:
            name = input("Enter the corrected name: ")
            cursor.execute(f"update bank_management set Name = {name} where account_number = {acc_no}")
            print("Updated successfully...")
        elif what == 2:
            gender = input("Enter the corrected gender (M/F): ")
            cursor.execute(f"update bank_management set gender = {gender} where account_number = {acc_no}")
            print("Updated successfully...")
        elif what == 3:
            age = int(input("Enter the corrected age: "))
            cursor.execute(f"update bank_management set age = {age} where account_number = {acc_no}")
            print("Updated successfully...")
        elif what == 4:
            dob = input("Enter the corrected DOB (YYYY-MM-DD): ")
            cursor.execute(f"update bank_management set DOB = {dob} where account_number = {acc_no}")
            print("Updated successfully...")
        elif what == 5:
            ad_no = int(input("Enter the corrected aadhar number: "))
            cursor.execute(f"update bank_management set Aadhar_Number = {ad_no} where account_number = {acc_no}")
            print("Updated successfully...")
        elif what == 6:
            address = input("Enter the corrected address: ")
            cursor.execute(f"update bank_management set Address = {address} where account_number = {acc_no}")
            print("Updated successfully...")
        elif what == 7:
            phone = int(input("Enter the corrected phone number: "))
            cursor.execute(f"update bank_management set Phone_Number = {phone} where account_number = {acc_no}")
            print("Updated successfully...")

    else:
        print(f"The account number {acc_no} does not exist.\nTry again!!")
        update_account_info()

    more_ops()


def check_balance():
    acc_no = int(input("Enter the account number: "))
    cursor.execute(f"select account_balance from bank_management where account_number = {acc_no}")
    balance = cursor.fetchall()[0][0]
    print(f"The account balance for the account with account number {acc_no} is {balance}")

    more_ops()


def ask_choices():
    print('''
    1. View a User Profile
    2. View all accounts
    3. Add account
    4. Remove account
    5. Update account info
    6. Check account balance
    ''')

    choice = int(input("Enter what you want to do\n(only a number)\n--> "))
    if choice == 1:
        view_user_profile()
    elif choice == 2:
        view_all()
    elif choice == 3:
        add_account()
    elif choice == 4:
        remove_account()
    elif choice == 5:
        update_account_info()
    elif choice == 6:
        check_balance()
    else:
        print("You have to enter a number between 1 and 6")
        ask_choices()


ask_choices()
