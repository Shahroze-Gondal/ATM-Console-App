import json
from colorama import Fore
from colorama import Style

# data = [{'Id': 1, "name": "Shahroze", 'Account_No': 12345, "Pin": 1156, "Amount": 10000},
#         {'Id': 2, "name": "Usama", 'Account_No': 23456, "Pin": 0000, "Amount": 11000},
#         {'Id': 3, "name": "Nadeem", 'Account_No': 10001, "Pin": 1000, "Amount": 12000},
#         {'Id': 4, "name": "Jawad", 'Account_No': 10101, "Pin": 1001, "Amount": 13000}
#         ]
#
# with open("Account.json", "w") as outfile:
#     json.dump(data, outfile)
print(f"{Fore.MAGENTA}-----Welcome to ATM!----- {Style.RESET_ALL}")


class ATM:
    def __init__(self):
        self.account_no = 0
        self.pin = 0
        self.person_data = ''
        self.data = ''
        self.transfer_account = 0
        self.delete_account = 0
        self.balance = 0
        self.my_balance = 0
        self.decision = 0

    def verify(self):
        with open('Account.json') as file:
            parse_json = json.load(file)
            self.data = parse_json
            for idx, x in enumerate(parse_json):
                if int(self.account_no) == x['account_no'] and int(self.pin) == x['pin']:
                    print('Credentials matched')
                    self.person_data = x
                    if x['is_active']:
                        if x['is_admin']:
                            print(f"{Fore.RED}-----Admin signed in-----!{Style.RESET_ALL}")
                            return self.choose_option_admin()
                        else:
                            print(f"{Fore.RED}-----User signed in-----!{Style.RESET_ALL}")
                            return self.choose_option()
                    else:
                        print('We are really sorry man! Your account has been deactivated')
                        return ''
            print('Credentials did not match')
            print('Please Enter Credentials again: ')
            return self.input()

    def input(self):
        self.account_no = input(f"{Fore.YELLOW}Enter account number: {Style.RESET_ALL}")
        self.pin = input(f"{Fore.YELLOW}Enter pin: {Style.RESET_ALL}")
        self.verify()

    def choose_option(self):
        options = ['balance inquiry', 'cash withdraw', 'money transfer', 'changing pin', 'deposit']
        for idx, x in enumerate(options):
            print(f"{Fore.LIGHTCYAN_EX}Enter {idx+1} for {x} {Style.RESET_ALL}")
        selected_option = input('Enter option: ')
        if selected_option == "1":
            self.balance_inquiry()
        elif selected_option == '2':
            self.cash_withdraw()
        elif selected_option == '3':
            self.money_transfer()
        elif selected_option == '4':
            self.change_pin()
        elif selected_option == '5':
            self.deposit()
        else:
            print('Enter valid option :')
            choose_option(self)

    def balance_inquiry(self):
        print(f"Your ramaining balance is {self.person_data['amount']}")
        return self.take_decision()

    def cash_withdraw(self):
        withdraw_amount = int(input('Enter amount to withdraw: '))
        while withdraw_amount < 500 or withdraw_amount > 20000:
            withdraw_amount = int(input('Please enter amount to withdraw between 500 and 20000: '))
        with open("Account.json", "r") as jsonFile:
            data = json.load(jsonFile)
        for idx, x in enumerate(data):
            if self.person_data == data[idx]:
                data[idx]["amount"] -= withdraw_amount
                self.person_data['amount'] = data[idx]["amount"]
        print(f"Your new balance is {self.person_data['amount']}")
        with open("Account.json", "w") as jsonFile:
            json.dump(data, jsonFile)
        return self.take_decision()

    def deposit(self):
        dep_amount = int(input('Please enter the amount you want to deposit: '))
        while dep_amount < 500 or dep_amount > 1000000:
            dep_amount = int(input('Please enter deposit amount between 500 and 10000: '))

        with open("Account.json", "r") as jsonFile:
            data = json.load(jsonFile)
        for idx, x in enumerate(data):
            if self.person_data == data[idx]:
                data[idx]["amount"] += dep_amount
                self.person_data['amount'] = data[idx]["amount"]
        print(f"Your new balance is {self.person_data['amount']}")
        with open("Account.json", "w") as jsonFile:
            json.dump(data, jsonFile)
        return self.take_decision()

    def change_pin(self):
        old_pin = int(input('Enter your old pin'))
        while old_pin != self.person_data['pin']:
            print('Please enter correct pin')
            old_pin = int(input('Enter your old pin'))
        # if old_pin == self.person_data['pin']:
        new_pin = int(input('Enter new pin : '))
        while new_pin <= 1000 or new_pin >= 10000:
            print('Your pin must be 4 digit number')
            new_pin = int(input('Enter new pin : '))
        with open("Account.json", "r") as jsonFile:
            data = json.load(jsonFile)
        for idx, x in enumerate(data):
            if self.person_data == data[idx]:
                data[idx]["pin"] = new_pin
                self.person_data['pin'] = new_pin
        print(f"Your new pin is {self.person_data['pin']}")
        with open("Account.json", "w") as jsonFile:
            json.dump(data, jsonFile)
        return self.take_decision()

    def money_transfer(self):
        self.transfer_account = int(input(f"Enter the account number to which you want to transfer the money:"))
        self.my_balance

        def account_validate_transfer():
            for idx, x in enumerate(self.data):
                if self.transfer_account == self.data[idx]['account_no']:
                    if self.transfer_account != self.person_data['account_no']:
                        transfer_amount = int(input(f'{Fore.YELLOW}Please enter the amount you want to transfer: {Style.RESET_ALL}'))
                        with open("Account.json", "r") as jsonFile:
                            data = json.load(jsonFile)
                        for index, n in enumerate(data):
                            if self.person_data == data[index]:
                                data[index]["amount"] -= transfer_amount
                                self.person_data['amount'] = data[index]["amount"]
                        data[idx]["amount"] += transfer_amount
                        print(f"{transfer_amount} transferred to Account Number: {data[idx]['account_no']}")
                        print(f"{Fore.GREEN}Your remaining balance is: {self.person_data['amount']}{Style.RESET_ALL}")
                        with open("Account.json", "w") as jsonFile:
                            json.dump(data, jsonFile)
                        return ''
                    self.transfer_account = int(input(f'{Fore.YELLOW}Please Enter account other than yourself:{Style.RESET_ALL} '))
                    return account_validate_transfer()
            self.transfer_account = int(input(f'{Fore.YELLOW}Please enter valid account number: {Style.RESET_ALL}'))
            return account_validate_transfer()
        account_validate_transfer()
        return self.take_decision()

    def take_decision(self):
        self.decision = int(input('Press 0 to continue: '))
        if self.decision == 0:
            if self.person_data['is_admin']:
                return self.choose_option_admin()
            else:
                return self.choose_option()

    def choose_option_admin(self):
        admin_options = ['create account', 'delete account', 'activate and deactivate']
        for idx, x in enumerate(admin_options):
            print(f"{Fore.LIGHTCYAN_EX}Enter {idx} for {x}{Style.RESET_ALL}")
        adm_selected_option = int(input(f'Please enter option: '))
        if adm_selected_option == 0:
            self.create_account()
        elif adm_selected_option == 1:
            self.delete_p_account()
        elif adm_selected_option == 2:
            self.activate_deactivate()

    def create_account(self):
        duplicate = True
        while duplicate:
            duplicate = False
            print('Please Enter unique values for id and account number')
            new_person_id = int(input(f"{Fore.YELLOW}Enter new person id:{Style.RESET_ALL}"))
            new_person_ac_no = int(input(f"{Fore.YELLOW}Enter new person account number:{Style.RESET_ALL}"))
            for i in range(len(self.data)):
                if new_person_ac_no == self.data[i]['id'] or new_person_ac_no == self.data[i]['account_no']:
                    duplicate = True
            if duplicate:
                print('You entered duplicate value values! Please Enter unique values for id and account number')
        is_admin = False
        new_person_name = input(f"{Fore.YELLOW}Enter new person name:{Style.RESET_ALL}")
        new_person_pin = int(input(f"{Fore.YELLOW}Enter new person pin{Style.RESET_ALL}"))
        while new_person_pin <= 1000 or new_person_pin >= 10000:
            print(f'{Fore.RED}Your pin must be 4 digit number{Style.RESET_ALL}')
            new_person_pin = int(input('Enter valid pin : '))
        new_person_amount = int(input("Enter new person amount"))
        person = {'id': new_person_id, 'name': new_person_name,
                  'account_no': new_person_ac_no, 'pin': new_person_pin,
                  'amount': new_person_amount, 'is_admin': is_admin, 'is_active': True}
        with open('Account.json', 'r') as file:
            parse_json = json.load(file)
            parse_json.append(person)
        with open("Account.json", "w") as jsonFile:
            json.dump(parse_json, jsonFile)
        print(f"{Fore.GREEN}New Person data is {parse_json[len(parse_json)-1]}{Style.RESET_ALL}")
        return self.take_decision()

    def delete_p_account(self):
        self.delete_account = int(input(f'{Fore.YELLOW}Enter valid account number: {Style.RESET_ALL}'))
        while self.delete_account == self.person_data['account_no']:
            self.delete_account = int(input(f'{Fore.YELLOW}Enter account other than yourself:{Style.RESET_ALL}'))
        for idx, x in enumerate(self.data):
            if self.delete_account == x['account_no']:
                with open('Account.json', 'r') as file:
                    parse_json = json.load(file)
                    deleted_account = parse_json.pop(idx)
                with open("Account.json", "w") as jsonFile:
                    json.dump(parse_json, jsonFile)
                print(f"{Fore.GREEN}Person having account number {deleted_account['account_no']} has been deleted{Style.RESET_ALL}")
                return self.take_decision()
        return self.delete_p_account()

    def activate_deactivate(self):
        activate_deactivate_options = ['activate', 'de_activate']
        for idx, x in enumerate(activate_deactivate_options):
            print(f"{Fore.LIGHTCYAN_EX}Enter {idx} for {x}:{Style.RESET_ALL} ")
        selected_option = int(input("Enter option: "))
        ac_no = int(input(f"{Fore.YELLOW}Please enter valid account number{Style.RESET_ALL}"))
        while ac_no == self.person_data['account_no']:
            ac_no = int(input(f'{Fore.YELLOW}Please enter account number other than yourself{Style.RESET_ALL}'))
        if selected_option == 0:
            for idx, x in enumerate(self.data):
                if ac_no == x['account_no']:
                    if x['is_active']:
                        print(f'{Fore.RED}Account number {ac_no} is already activated{Style.RESET_ALL}')
                        return self.take_decision()
                    else:
                        with open('Account.json', 'r') as file:
                            parse_json = json.load(file)
                            parse_json[idx]['is_active'] = True
                        with open("Account.json", "w") as jsonFile:
                            json.dump(parse_json, jsonFile)
                        print(f"{Fore.GREEN}Account number {parse_json[idx]['account_no']} has been activated{Style.RESET_ALL}")
                        return self.take_decision()
            return self.activate_deactivate()
        elif selected_option == 1:
            for idx, x in enumerate(self.data):
                if ac_no == x['account_no']:
                    if x['is_active']:
                        with open('Account.json', 'r') as file:
                            parse_json = json.load(file)
                            parse_json[idx]['is_active'] = False
                        with open("Account.json", "w") as jsonFile:
                            json.dump(parse_json, jsonFile)
                        print(f"{Fore.GREEN}Account number {parse_json[idx]['account_no']} has been deactivated{Style.RESET_ALL}")
                        return self.take_decision()
                    else:
                        print(f'{Fore.GREEN}Account number {ac_no} is already deactivated{Style.RESET_ALL}')
                        return self.take_decision()
            return self.activate_deactivate()


atm1 = ATM()
atm1.input()
