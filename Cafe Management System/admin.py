import json
from colorama import Fore, Style, init
from prettytable import PrettyTable



class Admin:
    def __init__(self):
        self.menu_file = 'Cafe Management System/Data/menu.json'
        self.order_file = 'Cafe Management System/Data/orders.json'
        self.feedback_file = 'Cafe Management System/Data/feedback.json'
        self.payment_file = 'Cafe Management System/Data/payment.json'

    def admin_menu(self):
        while True:
            print(Fore.CYAN + "\n      --- Admin Menu ---" + Style.RESET_ALL)
            print(Fore.YELLOW + """
            1. Add Item
            2. Update Item
            3. Delete Item
            4. View Orders
            5. View Feedback
            6. Payment Details
            7. Logout
            """ + Style.RESET_ALL)


            choice = input(Fore.GREEN + "Enter your choice: " + Style.RESET_ALL)

            if choice == '1':
                self.add_item()
            elif choice == '2':
                self.update_item()
            elif choice == '3':
                self.delete_item()
            elif choice == '4':
                self.view_orders()
            elif choice == '5':
                self.view_feedback()
            elif choice == '6':
                self.see_payment()
            elif choice == '7':
                print(Fore.CYAN + "Logging out Admin..." + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + "Invalid choice! Try again." + Style.RESET_ALL)

### File handling

    def read_json(self, file):
        try:
            with open(file, 'r') as fp:
                return json.load(fp)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
        except Exception:
            return {}

    def write_json(self, file, data):
        with open(file, 'w') as fp:
            json.dump(data, fp, indent=4)

### Admin Functions

    def add_item(self):
        menu = self.read_json(self.menu_file)

        while True:
            item = input(Fore.YELLOW + "Enter item name: " + Style.RESET_ALL).strip()

            if not item:
                print(Fore.RED + "Item name cannot be empty! ❌" + Style.RESET_ALL)
                continue

            if item.isdigit():
                print(Fore.RED + "Item name cannot be only numbers! ❌" + Style.RESET_ALL)
                continue

            if item in menu:
                print(Fore.RED + f"'{item}' already exists in menu! ❌" + Style.RESET_ALL)
                continue

            break

        while True:
            price_input = input(Fore.YELLOW + "Enter item price: " + Style.RESET_ALL)

            if not price_input.isdigit():
                print(Fore.RED + "Price must be a valid positive number! ❌" + Style.RESET_ALL)
                continue

            price = int(price_input)

            if price <= 0:
                print(Fore.RED + "Price must be greater than 0! ❌" + Style.RESET_ALL)
                continue

            break

        menu[item] = price
        self.write_json(self.menu_file, menu)

        print(Fore.GREEN + f"{item} added successfully! ✔️" + Style.RESET_ALL)


    def update_item(self):
        menu = self.read_json(self.menu_file)

        while True:
            item = input(Fore.YELLOW + "Enter item to update price: " + Style.RESET_ALL).strip()

            if not item:
                print(Fore.RED + "Item name cannot be empty! ❌" + Style.RESET_ALL)
                continue

            if item not in menu:
                print(Fore.RED + f"'{item}' not found in menu! ❌" + Style.RESET_ALL)
                return

            break

        while True:
            price_input = input(Fore.YELLOW + f"Enter new price for {item}: " + Style.RESET_ALL)

            if not price_input.isdigit():
                print(Fore.RED + "Price must be a valid positive number! ❌" + Style.RESET_ALL)
                continue

            price = int(price_input)

            if price <= 0:
                print(Fore.RED + "Price must be greater than 0! ❌" + Style.RESET_ALL)
                continue

            break

        menu[item] = price
        self.write_json(self.menu_file, menu)

        print(Fore.GREEN + f"{item} price updated successfully! ✔️" + Style.RESET_ALL)


    def delete_item(self):
        menu = self.read_json(self.menu_file)

        item = input(Fore.YELLOW + "Enter item to delete: " + Style.RESET_ALL)

        if item in menu:
            del menu[item]
            self.write_json(self.menu_file, menu)
            print(Fore.GREEN + f"{item} deleted successfully!" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"{item} not found." + Style.RESET_ALL)



    def view_orders(self):
        try:
            orders = self.read_json(self.order_file)

            if not orders:
                print(Fore.RED + "\nNo orders found!" + Style.RESET_ALL)
                return

            print(Fore.CYAN + "\n----- All Orders -----" + Style.RESET_ALL)

    
            table = PrettyTable()
            table.field_names = ["Username", "Items Ordered", "Total Bill (₹)"]

            
            for order in orders:
            
                items_list = "\n".join(
                    [f"{item['item']} x {item['qty']}" for item in order["orders"]]
                )

                table.add_row([
                    order["username"],
                    items_list,
                    order["total"]
                ])

            table.align = "l"
            print(Fore.YELLOW + str(table) + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"\nError reading orders: {e}" + Style.RESET_ALL)




    def view_feedback(self):
        try:
            data = self.read_json(self.feedback_file)

            if not data:
                print(Fore.RED + "\nNo feedbacks found." + Style.RESET_ALL)
                return

            print(Fore.CYAN + "\n----- All Feedbacks -----" + Style.RESET_ALL)

            
            table = PrettyTable()
            table.field_names = ["Username", "Feedback"]

        
            for fb in data:
                table.add_row([
                    fb["username"],
                    fb["feedback"]
                ])

            table.align = "l"
            print(Fore.YELLOW + str(table) + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"\nError reading feedback: {e}" + Style.RESET_ALL)




    def see_payment(self):
        try:
            payment = self.read_json(self.payment_file)

            if not payment:
                print(Fore.RED + "\nNo payments found." + Style.RESET_ALL)
                return

            print(Fore.CYAN + "\n----- Payment Details -----" + Style.RESET_ALL)

            
            table = PrettyTable()
            table.field_names = [
                "Username", "Subtotal (₹)", "GST (5%) (₹)",
                "Total (₹)", "Method", "Status", "Date"
            ]

        
            for pay in payment:
                table.add_row([
                    pay.get('username'),
                    pay.get('subtotal'),
                    pay.get('gst_5_percent'),
                    pay.get('total_amount'),
                    pay.get('method'),
                    pay.get('status'),
                    pay.get('date')
                ])

        
            table.align = "l"
            print(Fore.YELLOW + str(table) + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"\nError reading payment file: {e}" + Style.RESET_ALL)


if __name__ == '__main__':
    a1 = Admin()
    a1.admin_menu()
