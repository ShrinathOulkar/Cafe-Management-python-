import json
from datetime import datetime
from colorama import Fore, Back, Style, init
from prettytable import PrettyTable



class User:
    def __init__(self, username):
        self.username = username
        self.menu_file = 'Cafe Management System/Data/menu.json'
        self.order_file = 'Cafe Management System/Data/orders.json'
        self.feedback_file = 'Cafe Management System/Data/feedback.json'
        self.payment_file = 'Cafe Management System/Data/payment.json'

        self.menu_data = self.read_json(self.menu_file)
        self.order_data = self.read_json(self.order_file)
        self.feedback_data = self.read_json(self.feedback_file)
        
    def user_menu(self):
        while True:
            print(Fore.CYAN + f"\n    --- Welcome {self.username} ---")
            print(Fore.YELLOW + """
            1. View Menu
            2. Place Order
            3. My Orders
            4. Give Feedback
            5. Exit
            """ + Style.RESET_ALL)


            choice = input(Fore.LIGHTBLUE_EX + "Enter your choice: ")

            if choice == '1':
                self.view_menu()
                
            elif choice == '2': 
                self.place_order()
            
            elif choice == '3':
                self.my_orders()
                
            elif choice == '4':
                self.give_feedback()
                
            elif choice == '5':
                print(Fore.GREEN + "Thank You ...🙏🏻")
                print(Fore.CYAN + f"Please visit again {self.username}")
                break
            else:
                print(Fore.RED + "Invalid choice! Try again.")

    # File Handling
    def read_json(self, file):
        try:
            with open(file, 'r') as fp:
                return json.load(fp)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
            
    def write_json(self, file, data):
        try:
            with open(file, 'w') as fp:
                json.dump(data, fp, indent=4)
        except Exception as e:
            print(Fore.RED + 'Error:', e)

    #  User Functions 
    def view_menu(self):
        menu = self.menu_data
        if not menu:
            print(Fore.RED + "⚠️ Menu is Empty")
            return {}

        print(Fore.YELLOW + "-" * 37 + Style.RESET_ALL)
        print(Fore.MAGENTA + "     --- Delight Cafe ---       " + Style.RESET_ALL)
        print(Fore.YELLOW + "\n========== Cafe Menu ==========" + Style.RESET_ALL)

        print(f"{'No.':<5}{'Item Name':<20}{'Price (₹)':>10}")
        print(Fore.YELLOW + "-" * 37 + Style.RESET_ALL)

        item_color = Fore.BLUE   

        for i, (item, price) in enumerate(menu.items(), start=1):
            print(
                f"{Fore.YELLOW}{i:<5}"             
                f"{item_color}{item:<20}"          
                f"{Fore.CYAN}{price:>10}"           
                + Style.RESET_ALL                  
            )

        print(Fore.YELLOW + "-" * 37 + Style.RESET_ALL)
        print(Fore.LIGHTBLUE_EX + "Select the item number to order." + Style.RESET_ALL)

        return menu


    
    def place_order(self):
        menu = self.menu_data
        if not menu:
            print(Fore.RED + "⚠️ Menu is empty!")
            return

        self.view_menu()
        
        orders = []
        total = 0

        while True:
            try:
                item_no = int(input("Enter item number (0 to finish): "))
            except ValueError:
                print(Fore.RED + " Invalid input! Please enter a number.❌")
                continue

            if item_no == 0:
                break

            menu_list = list(menu.items())

            if 1 <= item_no <= len(menu_list):
                item_name, price = menu_list[item_no - 1]
                try:
                    qty = int(input(f"Enter quantity for {item_name}: "))
                except ValueError:
                    print(Fore.RED + " Invalid quantity! Try again.❌")
                    continue

                cost = price * qty
                total += cost
                orders.append({"item": item_name, "qty": qty, "cost": cost})
            else:
                print(Fore.RED + "Invalid item number! Try again.")

        if not orders:
            print(Fore.RED + "No items ordered.")
            return

        # print(Fore.YELLOW + "\n------- Your Order Summary -------")
        # print(f"{'Item Name':<20}{'Quantity':>10}")
        # print(Fore.YELLOW + "_" * 30)

        # for order in orders:
        #     print(f"{order['item']:<20}{order['qty']:>5}")
    
        # print(Fore.YELLOW + "_" * 30)
        print()
    
        all_orders = self.read_json(self.order_file)
        
        
        new_order = {
            "username": self.username,
            "orders": orders,
            "total": total,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")   # ⭐ add date here
        }


        all_orders.append(new_order)
        self.write_json(self.order_file, all_orders)

        print(Fore.GREEN + "Order saved successfully! ✅ ")
        
        
        # self.view_bill()
        
        self.make_payment()
        

    def view_bill(self):
        all_orders = self.read_json(self.order_file)
        if not all_orders:
            print(Fore.RED + " No orders found.❌")
            return None

        user_order = [order for order in all_orders if order["username"] == self.username]
            
        if not user_order:
            print(Fore.RED + "No order found for this user.❌ ")
            return None

        user_order = user_order[-1]

        print(Fore.MAGENTA + "\n================= Your Bill =================")
        print(f"{'Item Name':<20}{'Qty':>10}{'Cost (₹)':>15}")
        print(Fore.YELLOW + "-" * 45)

        subtotal = 0
        for item in user_order["orders"]:
            print(f"{item['item']:<20}{item['qty']:>10}{item['cost']:>15.2f}")
            subtotal += item['cost']

        gst = subtotal * 0.05
        grand_total = subtotal + gst

        print(Fore.YELLOW + "-" * 45)
        print(f"{'Subtotal:':<30}{Fore.CYAN} ₹{subtotal:.2f}")
        print(f"{'GST (5%):':<30}{Fore.CYAN} ₹{gst:.2f}")
        print(f"{'Total Amount:':<30}{Fore.GREEN} ₹{grand_total:.2f}")
        print(Fore.YELLOW + "=" * 45)

        return subtotal, gst, grand_total

    def make_payment(self):
        result = self.view_bill()
        if not result:
            return

        subtotal, gst_amount, final_total = result

        while True:  
            print(Fore.MAGENTA + "\n--- Payment Section ---")
            print(Fore.CYAN + f"Total Payable: ₹{final_total:.2f}")
            print("\nSelect payment method:")
            print("1. Cash")
            print("2. Card")
            print("3. UPI")

            choice = input(Fore.LIGHTBLUE_EX + "Enter your choice (1-3): ")

            payment_method = ""
            payment_status = "Failed"
            change = 0.0

            
            if choice == "1":
                payment_method = "Cash"
                payment_status = "Successful"
                print(Fore.GREEN + "Cash Payment Successful! ✔" + Style.RESET_ALL)

        
            elif choice == "2":
                payment_method = "Card"
                card = input("Enter card number (14 digits): ")

                if not card.isdigit() or len(card) != 14:
                    print(Fore.RED + "Invalid card number! Must be 14 digits. ❌")
                    print(Fore.YELLOW + "Please try again...\n")
                    continue  

                print(Fore.YELLOW + f"Processing card ending with {card[-4:]}...")
                payment_status = "Successful"
                print(Fore.GREEN + "Payment successful! ✅ ")

            
            elif choice == "3":
                payment_method = "UPI"
                upi = input("Enter your UPI Number (10 digits): ")

    
                if not (upi.isdigit() and len(upi) == 10):
                    print(Fore.RED + "Invalid UPI Number! It must contain exactly 10 digits. ❌")
                    print(Fore.YELLOW + "Please try again...\n")
                    continue


                print(Fore.YELLOW + f"Processing payment from {upi}...")
                payment_status = "Successful"
                print(Fore.GREEN + "Payment successful! ✅ ")

            else:
                print(Fore.RED + "Invalid option. Please try again. ❌")
                continue  

            
            if payment_status == "Successful":
                break

        

        all_payments = self.read_json(self.payment_file)
        new_payment = {
            "username": self.username,
            "subtotal": round(subtotal, 2),
            "gst_5_percent": round(gst_amount, 2),
            "total_amount": round(final_total, 2),
            "method": payment_method,
            "status": payment_status,
            "change_returned": round(change, 2),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        all_payments.append(new_payment)
        self.write_json(self.payment_file, all_payments)

        print(Fore.GREEN + "\n💾 Payment details saved successfully ...")

    
    

    def give_feedback(self):
        feedback_all = self.feedback_data or []
        feedback = input(Fore.LIGHTBLUE_EX + "Enter your feedback: ")
        new_feedback = {"username": self.username, "feedback": feedback}
        feedback_all.append(new_feedback)
        self.write_json(self.feedback_file, feedback_all)
        print(Fore.GREEN + "Thank you for your feedback!✅")

    def my_orders(self):
        print(Fore.CYAN + "\n====== My Orders ======" + Style.RESET_ALL)

        all_orders = self.read_json(self.order_file)

        # Get ALL orders of this user
        user_orders = [order for order in all_orders if order["username"] == self.username]

        if not user_orders:
            print(Fore.RED + "⚠️ You have no orders yet.")
            return

        print(Fore.YELLOW + f"\nTotal Orders Found: {len(user_orders)}\n")

        for order_index, order in enumerate(user_orders, start=1):
            print(Fore.MAGENTA + f"\n========== Order {order_index} ==========")
            print(Fore.CYAN + f"Date: {order.get('date', 'Not Available')}")
            print(Fore.YELLOW + "----------------------------------------")

            
            print(f"{Fore.GREEN}{'No.':<5}{'Item Name':<20}{'Qty':<8}{'Cost (₹)':<10}")
            print(Fore.YELLOW + "-" * 45)

            
            for i, item in enumerate(order["orders"], start=1):
                print(
                    f"{Fore.CYAN}{i:<5}"
                    f"{item['item']:<20}"
                    f"{item['qty']:<8}"
                    f"₹{item['cost']:<10}"
                )

            print(Fore.YELLOW + "-" * 45)
            print(Fore.GREEN + f"Order Total: ₹{order['total']}")
            print(Fore.YELLOW + "-" * 45)



if __name__ == "__main__":
    u1 = User('yash')
    u1.user_menu()
