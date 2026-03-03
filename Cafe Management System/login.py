import json
from admin import Admin
from user import User
import getpass
from colorama import Fore, Style, init



class Login:
    def __init__(self):
        self.user_file = 'Cafe Management System/Data/login_details.json'
        self.admin_name = "Admin"
        self.admin_pass = "1234"

    def admin_login(self):
        print(Fore.CYAN + "\n--- Admin Login ---" + Style.RESET_ALL)
        name = input(Fore.YELLOW + "Enter Admin name: " + Style.RESET_ALL)
        pwd = getpass.getpass(Fore.YELLOW + "Enter password: " + Style.RESET_ALL)

        if name == self.admin_name and pwd == self.admin_pass:
            print(Fore.GREEN + "Admin logged in successfully!" + Style.RESET_ALL)
            admin = Admin()
            admin.admin_menu()
        else:
            print(Fore.RED + "Invalid admin credentials!" + Style.RESET_ALL)

    def user_login(self):
        print(Fore.CYAN + "\n--- User Section ---" + Style.RESET_ALL)
        name = input(Fore.YELLOW + "Enter your username: " + Style.RESET_ALL)
        pwd = getpass.getpass(Fore.YELLOW + "Enter your password: " + Style.RESET_ALL)

        users = self.read_users()

        if name in users and users[name] == pwd:
            print(Fore.GREEN + f"Welcome {name}! Login successful." + Style.RESET_ALL)
            user = User(name)
            user.user_menu()
        else:
            print(Fore.RED + "User not found! Please register first." + Style.RESET_ALL)
            self.user_register()

    def user_register(self):
        print(Fore.CYAN + "\n--- New User Registration ---" + Style.RESET_ALL)
        name = input(Fore.YELLOW + "Enter new username: " + Style.RESET_ALL)
        pwd = input(Fore.YELLOW + "Enter password: " + Style.RESET_ALL)

        users = self.read_users()

        if name in users:
            print(Fore.RED + "User already exists! Please login." + Style.RESET_ALL)
        else:
            users[name] = pwd
            self.write_users(users)
            print(Fore.GREEN + "Registration successful! Please login again." + Style.RESET_ALL)

    def read_users(self):
        try:
            with open(self.user_file, 'r') as fp:
                return json.load(fp)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def write_users(self, data):
        with open(self.user_file, 'w') as fp:
            json.dump(data, fp, indent=4)

if __name__ == "__main__":
    l1 = Login()
    l1.admin_login()
