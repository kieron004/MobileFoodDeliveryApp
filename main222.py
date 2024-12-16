import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import webbrowser

from User_Registration import UserRegistration
from Order_Placement import Cart, OrderPlacement, UserProfile, RestaurantMenu, PaymentMethod
from Payment_Processing import PaymentProcessing
from Restaurant_Browsing import RestaurantDatabase, RestaurantBrowsing
from RestaurantFiltering import RestaurantFilter
# main.py
from FutureOrdersWishlist import FutureOrdersWishlist
from OrderTrackingMethods import OrderTracker

# Utility functions for user data storage
USERS_FILE = "users.json"


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mobile Food Delivery App")
        self.geometry("800x500")

        # Load user registration data from file
        self.user_data = load_users()

        # Initialize core classes
        self.registration = UserRegistration()
        self.registration.users = self.user_data  # Load existing users into registration system

        self.database = RestaurantDatabase()
        self.browsing = RestaurantBrowsing(self.database)

        # Initially no user logged in
        self.logged_in_email = None

        # Create initial frame
        self.current_frame = None
        self.show_startup_frame()

    def show_startup_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = StartupFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_register_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = RegisterFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_login_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def login_user(self, email):
        self.logged_in_email = email
        # After login, show main app frame
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = MainAppFrame(self, email)
        self.current_frame.pack(fill="both", expand=True)


class StartupFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Welcome to the Mobile Food Delivery App", font=("Arial", 16)).pack(pady=30)

        tk.Button(self, text="Register", command=self.go_to_register, width=20).pack(pady=10)
        tk.Button(self, text="Login", command=self.go_to_login, width=20).pack(pady=10)

    def go_to_register(self):
        self.master.show_register_frame()

    def go_to_login(self):
        self.master.show_login_frame()


class RegisterFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Register New User", font=("Arial", 14)).pack(pady=20)

        self.email_entry = self.create_entry("Email:")
        self.pass_entry = self.create_entry("Password:", show="*")
        self.conf_pass_entry = self.create_entry("Confirm Password:", show="*")

        tk.Button(self, text="Register", command=self.register_user).pack(pady=10)
        tk.Button(self, text="Back", command=self.go_back).pack()

    def create_entry(self, label_text, show=None):
        frame = tk.Frame(self)
        frame.pack(pady=5)
        tk.Label(frame, text=label_text, width=15, anchor="e").pack(side="left")
        entry = tk.Entry(frame, show=show)
        entry.pack(side="left")
        return entry

    def register_user(self):
        email = self.email_entry.get()
        password = self.pass_entry.get()
        confirm_password = self.conf_pass_entry.get()

        result = self.master.registration.register(email, password, confirm_password)
        if result["success"]:
            # Save the updated users to file
            save_users(self.master.registration.users)
            messagebox.showinfo("Success", "Registration successful! Please log in.")
            self.master.show_login_frame()
        else:
            messagebox.showerror("Error", result["error"])

    def go_back(self):
        self.master.show_startup_frame()


class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="User Login", font=("Arial", 14)).pack(pady=20)

        self.email_entry = self.create_entry("Email:")
        self.pass_entry = self.create_entry("Password:", show="*")

        tk.Button(self, text="Login", command=self.login).pack(pady=10)
        tk.Button(self, text="Back", command=self.go_back).pack()

    def create_entry(self, label_text, show=None):
        frame = tk.Frame(self)
        frame.pack(pady=5)
        tk.Label(frame, text=label_text, width=15, anchor="e").pack(side="left")
        entry = tk.Entry(frame, show=show)
        entry.pack(side="left")
        return entry

    def login(self):
        email = self.email_entry.get()
        password = self.pass_entry.get()
        # Validate login
        # For simplicity, just check if user exists and password matches
        users = self.master.registration.users
        if email in users and users[email]["password"] == password:
            self.master.login_user(email)
        else:
            messagebox.showerror("Error", "Invalid email or password")

    def go_back(self):
        self.master.show_startup_frame()


class MainAppFrame(tk.Frame):
    def __init__(self, master, user_email):
        super().__init__(master)
        self.future_orders_wishlist = FutureOrdersWishlist()
        tk.Label(self, text=f"Welcome, {user_email}", font=("Arial", 14)).pack(pady=10)

        self.user_email = user_email
        self.database = master.database
        self.browsing = master.browsing

        # 创建用户的profile和购物车
        self.user_profile = UserProfile(delivery_address="123 Main St")
        self.cart = Cart()
        self.restaurant_menu = RestaurantMenu(available_items=["Burger", "Pizza", "Salad"])
        self.order_placement = OrderPlacement(self.cart, self.user_profile, self.restaurant_menu)

        restaurants_data = [
            {"name": "Pasta House", "cuisine": "Italian", "rating": 4.5, "delivery_time": 30, "location": "Downtown"},
            {"name": "Sushi World", "cuisine": "Japanese", "rating": 4.0, "delivery_time": 25, "location": "Uptown"},
            {"name": "Taco Bell", "cuisine": "Mexican", "rating": 3.5, "delivery_time": 45, "location": "Suburb"},
            {"name": "Burger King", "cuisine": "American", "rating": 4.2, "delivery_time": 35,
             "location": "City Center"},
            {"name": "Dragon Wok", "cuisine": "Chinese", "rating": 4.8, "delivery_time": 20, "location": "Midtown"},
        ]
        self.restaurant_filter = RestaurantFilter(restaurants_data)

        # 创建筛选输入框
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)
        tk.Label(search_frame, text="Cuisine:").pack(side="left")
        self.cuisine_var = tk.Entry(search_frame)
        self.cuisine_var.pack(side="left", padx=5)
        tk.Label(search_frame, text="Max Rating:").pack(side="left")
        self.max_rating_var = tk.Entry(search_frame)
        self.max_rating_var.pack(side="left", padx=5)
        tk.Label(search_frame, text="Max Delivery Time:").pack(side="left")
        self.max_delivery_time_var = tk.Entry(search_frame)
        self.max_delivery_time_var.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", command=self.search_restaurants).pack(side="left")

        # 搜索结果显示
        self.results_tree = ttk.Treeview(self, columns=("cuisine", "location", "rating", "delivery_time"),
                                         show="headings")
        self.results_tree.heading("cuisine", text="Cuisine")
        self.results_tree.heading("location", text="Location")
        self.results_tree.heading("rating", text="Rating")
        self.results_tree.heading("delivery_time", text="Delivery Time")
        self.results_tree.pack(pady=10, fill="x")

        # 操作按钮
        action_frame = tk.Frame(self)
        action_frame.pack(pady=5)
        tk.Button(action_frame, text="View All Restaurants", command=self.view_all_restaurants).pack(side="left",
                                                                                                     padx=5)
        tk.Button(action_frame, text="Add Item to Cart", command=self.add_item_to_cart).pack(side="left", padx=5)
        tk.Button(action_frame, text="View Cart", command=self.view_cart).pack(side="left", padx=5)
        tk.Button(action_frame, text="Checkout", command=self.checkout).pack(side="left", padx=5)

        # 新增的“Track Order”按钮
        tk.Button(action_frame, text="Track Order", command=self.track_order).pack(side="left", padx=5)
        # 新增的“增加心愿单”按钮
        tk.Button(action_frame, text="Add to Wishlist", command=self.add_to_wishlist_popup).pack(side="left", padx=5)

    def search_restaurants(self):
        self.results_tree.delete(*self.results_tree.get_children())
        cuisine = self.cuisine_var.get().strip()
        max_rating = self.max_rating_var.get().strip()  # 获取最大评分
        max_delivery_time = self.max_delivery_time_var.get().strip()  # 获取最大配送时间

        # 默认情况下，如果没有填写，则为 None 或合理默认值
        max_rating = float(max_rating) if max_rating else 5.0  # 最大评分默认5
        max_delivery_time = int(max_delivery_time) if max_delivery_time else 60  # 最大配送时间默认60分钟

        # 调用 restaurant browsing 的搜索功能
        results = self.restaurant_filter.search_by_filters(
            cuisine_type=cuisine if cuisine else None,
            max_rating=max_rating,
            max_delivery_time=max_delivery_time
        )
        for r in results:
            self.results_tree.insert("", "end", values=(r["cuisine"], r["location"], r["rating"]))

    def view_all_restaurants(self):
        self.results_tree.delete(*self.results_tree.get_children())
        results = self.database.get_restaurants()
        for r in results:
            self.results_tree.insert("", "end", values=(r["cuisine"], r["location"], r["rating"]))

    def add_item_to_cart(self):
        menu_popup = AddItemPopup(self, self.restaurant_menu, self.cart)
        self.wait_window(menu_popup)

    def view_cart(self):
        cart_view = CartViewPopup(self, self.cart)
        self.wait_window(cart_view)

    def checkout(self):
        validation = self.order_placement.validate_order()
        if not validation["success"]:
            messagebox.showerror("Error", validation["message"])
            return

        checkout_popup = CheckoutPopup(self, self.order_placement)
        self.wait_window(checkout_popup)

    def add_to_wishlist_popup(self):
        """弹出一个新的窗口来让用户选择想要加入心愿单的食物"""
        wishlist_popup = AddToWishlistPopup(self, self.future_orders_wishlist)
        self.wait_window(wishlist_popup)

    def track_order(self):
        # Assume we have order details like ID and starting location
        initial_location = (40.748817, -73.985428)  # Example initial location (New York)
        order_tracker = OrderTracker(order_id="12345", initial_location=initial_location)

        # Simulating updating the order's route
        order_tracker.update_location((40.749817, -73.986428))
        order_tracker.update_location((40.750817, -73.987428))
        order_tracker.update_location((40.751817, -73.988428))

        # Save the map and open it (or you can display the map in a browser)
        order_tracker.save_map("order_12345_map.html")
        messagebox.showinfo("Order Tracking", "Order tracking map has been saved as order_12345_map.html")
        # Open the saved map in the default web browser
        webbrowser.open("order_12345_map.html")


class AddItemPopup(tk.Toplevel):
    def __init__(self, master, menu, cart):
        super().__init__(master)
        self.title("Add Item to Cart")
        self.menu = menu
        self.cart = cart

        tk.Label(self, text="Select an item to add to cart:").pack(pady=10)

        self.item_var = tk.StringVar()
        self.item_var.set(self.menu.available_items[0] if self.menu.available_items else "")
        tk.OptionMenu(self, self.item_var, *self.menu.available_items).pack(pady=5)

        tk.Label(self, text="Quantity:").pack()
        self.qty_entry = tk.Entry(self)
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack(pady=5)

        tk.Button(self, text="Add to Cart", command=self.add_to_cart).pack(pady=10)

    def add_to_cart(self):
        item = self.item_var.get()
        qty = int(self.qty_entry.get())
        price = 10.0  # Static price for simplicity
        msg = self.cart.add_item(item, price, qty)
        messagebox.showinfo("Cart", msg)
        self.destroy()


class CartViewPopup(tk.Toplevel):
    def __init__(self, master, cart):
        super().__init__(master)
        self.title("Cart Items")

        items = cart.view_cart()
        if not items:
            tk.Label(self, text="Your cart is empty").pack(pady=20)
        else:
            for i in items:
                tk.Label(self, text=f"{i['name']} x{i['quantity']} = ${i['subtotal']:.2f}").pack()


class CheckoutPopup(tk.Toplevel):
    def __init__(self, master, order_placement):
        super().__init__(master)
        self.title("Checkout")
        self.order_placement = order_placement

        order_data = order_placement.proceed_to_checkout()
        tk.Label(self, text="Review your order:", font=("Arial", 12)).pack(pady=10)

        # Show items
        for item in order_data["items"]:
            tk.Label(self, text=f"{item['name']} x{item['quantity']} = ${item['subtotal']:.2f}").pack()

        total = order_data["total_info"]
        tk.Label(self, text=f"Subtotal: ${total['subtotal']:.2f}").pack()
        tk.Label(self, text=f"Tax: ${total['tax']:.2f}").pack()
        tk.Label(self, text=f"Delivery Fee: ${total['delivery_fee']:.2f}").pack()
        tk.Label(self, text=f"Total: ${total['total']:.2f}").pack()

        tk.Label(self, text=f"Delivery Address: {order_data['delivery_address']}").pack(pady=5)

        # Payment method selection
        tk.Label(self, text="Payment Method:").pack(pady=5)
        self.payment_method = tk.StringVar()
        self.payment_method.set("credit_card")
        tk.Radiobutton(self, text="Credit Card", variable=self.payment_method, value="credit_card").pack()
        tk.Radiobutton(self, text="Paypal", variable=self.payment_method, value="paypal").pack()
        tk.Radiobutton(self, text="split payments", variable=self.payment_method, value="split payments").pack()
        tk.Radiobutton(self, text="gift cards", variable=self.payment_method, value="gift cards").pack()

        tk.Label(self, text="For credit card enter a 16-digit card number:").pack(pady=5)
        self.card_entry = tk.Entry(self)
        self.card_entry.insert(0, "1234567812345678")
        self.card_entry.pack(pady=5)

        tk.Button(self, text="Confirm Order", command=self.confirm_order).pack(pady=10)

    def confirm_order(self):
        # Process order confirmation with the given payment method
        payment_method_obj = PaymentMethod()  # Mock payment method handling in the old code
        # Actually, we have PaymentProcessing class. Let's just rely on PaymentMethod for simplicity here.
        # If you wanted to use PaymentProcessing, you could do so by integrating it as well.
        # For now, we'll simulate PaymentMethod.process_payment by checking if total > 0.
        # In a full scenario, integrate PaymentProcessing similarly.

        payment_method = self.payment_method.get()

        if payment_method == "split payments":
            self.open_split_payment_window()
        else:

            # Confirm the order
            result = self.order_placement.confirm_order(payment_method_obj)
            if result["success"]:
                messagebox.showinfo("Order Confirmed",
                                    f"Order ID: {result['order_id']}\nEstimated Delivery: {result['estimated_delivery']}")
                self.destroy()
            else:
                messagebox.showerror("Error", result["message"])

    def open_split_payment_window(self):
        # Create a new window for splitting payment
        split_window = tk.Toplevel(self)
        split_window.title("Split Payment")

        tk.Label(split_window, text="Enter number of people to split payment:").pack(pady=5)
        self.num_people_entry = tk.Entry(split_window)
        self.num_people_entry.pack(pady=5)

        self.split_amount_label = tk.Label(split_window, text="Each person's share: $0.00")
        self.split_amount_label.pack(pady=5)

        tk.Button(split_window, text="Calculate", command=self.calculate_split_payment).pack(pady=10)
        # Add a submit button for confirming the payment
        tk.Button(split_window, text="Submit Order", command=self.submit_order).pack(pady=10)

    def submit_order(self):
        # Simulate order submission and show success message
        payment_method_obj = PaymentMethod()
        result = self.order_placement.confirm_order(payment_method_obj)
        if result["success"]:
            messagebox.showinfo("Order Confirmed",
                                f"Order ID: {result['order_id']}\nEstimated Delivery: {result['estimated_delivery']}")
            self.destroy()
        else:
            messagebox.showerror("Error", result["message"])


    def calculate_split_payment(self):
        # Get the number of people and total amount
        try:
            num_people = int(self.num_people_entry.get())
            if num_people <= 0:
                messagebox.showerror("Invalid Input", "Number of people must be greater than zero.")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for people.")
            return

        # Calculate split amount
        order_data = self.order_placement.proceed_to_checkout()
        total_amount = order_data["total_info"]["total"]
        split_amount = total_amount / num_people

        # Update the label with the calculated split amount
        self.split_amount_label.config(text=f"Each person's share: ${split_amount:.2f}")



class TrackOrderPopup(tk.Toplevel):
    def __init__(self, master, map_filename):
        super().__init__(master)
        self.title("Track Order")

        # Show the HTML map file in the default browser
        webbrowser.open(map_filename)

        tk.Label(self, text="Order Tracking Map").pack(pady=20)
        tk.Button(self, text="Close", command=self.destroy).pack(pady=10)


class AddToWishlistPopup(tk.Toplevel):
    def __init__(self, master, wishlist):
        super().__init__(master)
        self.title("Add Item to Wishlist")
        self.wishlist = wishlist

        tk.Label(self, text="Select an item to add to wishlist:").pack(pady=10)

        self.item_var = tk.StringVar()
        self.item_var.set("Burger")  # Default value for item
        tk.OptionMenu(self, self.item_var, "Burger", "Pizza", "Salad").pack(pady=5)

        tk.Label(self, text="Quantity:").pack()
        self.qty_entry = tk.Entry(self)
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack(pady=5)

        tk.Button(self, text="Add to Wishlist", command=self.add_to_wishlist).pack(pady=10)

    def add_to_wishlist(self):
        item = self.item_var.get()
        quantity = int(self.qty_entry.get())
        price = 10.0  # Static price for simplicity

        msg = self.wishlist.add_to_wishlist(item, price, quantity)
        messagebox.showinfo("Wishlist", msg)
        self.destroy()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
