from login import Login
from colorama import Fore, Style, init



ch = '0'

while ch != '4':
    print(Fore.YELLOW + '=' * 40)
    print(Fore.MAGENTA + Style.BRIGHT + 'Welcome to the Delight Cafe 🍔🧋')
    print(Fore.YELLOW + '=' * 40)

    print(Fore.CYAN + """
          1. Admin Login
          2. New User Registration
          3. User Login
          4. Exit
          """)

    ch = input(Fore.LIGHTBLUE_EX + "Enter Your Choice: ")
    l1 = Login()

    if ch == '1':
        l1.admin_login()
    elif ch == '2':
        l1.user_register()
    elif ch == '3':
        l1.user_login()
    elif ch == '4':
        print(Fore.GREEN + 'Thank You....🙏🏻')
        break
    else:
        print(Fore.RED + 'Invalid Choice ❌')
        print(Fore.YELLOW + 'Please enter a valid option.')
