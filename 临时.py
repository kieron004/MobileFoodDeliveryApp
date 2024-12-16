class MainAppFrame(tk.Frame):
    def __init__(self, master, user_email):
        super().__init__(master)
        tk.Label(self, text=f"Welcome, {user_email}", font=("Arial", 14)).pack(pady=10)

        self.user_email = user_email
        self.database = master.database
        self.browsing = master.browsing

        # Create user's profile and cart
        self.user_profile = UserProfile(delivery_address="123 Main St")
        self.cart = Cart()
        self.restaurant_menu = RestaurantMenu(available_items=["Burger", "Pizza", "Salad"])
        self.order_placement = OrderPlacement(self.cart, self.user_profile, self.restaurant_menu)
        self.restaurant_filter = RestaurantFilter(restaurants_data)
        # 创建用户的愿望清单
        self.future_orders_wishlist = FutureOrdersWishlist()

        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)

        # Search Frame
        # Filters: Cuisine, Rating, Delivery Speed
        tk.Label(search_frame, text="Cuisine:").pack(side="left")
        self.cuisine_var = tk.Entry(search_frame)
        self.cuisine_var.pack(side="left", padx=5)

        tk.Label(search_frame, text="Max Rating:").pack(side="left")
        self.max_rating_var = tk.Entry(search_frame)
        self.max_rating_var.pack(side="left", padx=5)

        tk.Label(search_frame, text="Max Delivery Time:").pack(side="left")
        self.max_delivery_var = tk.Entry(search_frame)
        self.max_delivery_var.pack(side="left", padx=5)

        tk.Button(search_frame, text="Search", command=self.search_restaurants).pack(side="left", padx=5)

        # Results Treeview
        self.results_tree = ttk.Treeview(self, columns=("cuisine", "location", "rating"), show="headings")
        self.results_tree.heading("cuisine", text="Cuisine")
        self.results_tree.heading("location", text="Location")
        self.results_tree.heading("rating", text="Rating")
        self.results_tree.pack(pady=10, fill="x")

        # Buttons for actions
        action_frame = tk.Frame(self)
        action_frame.pack(pady=5)
        tk.Button(action_frame, text="View All Restaurants", command=self.view_all_restaurants).pack(side="left", padx=5)
        tk.Button(action_frame, text="Add Item to Cart", command=self.add_item_to_cart).pack(side="left", padx=5)
        tk.Button(action_frame, text="View Cart", command=self.view_cart).pack(side="left", padx=5)
        tk.Button(action_frame, text="Checkout", command=self.checkout).pack(side="left", padx=5)

    def search_restaurants(self):
        self.results_tree.delete(*self.results_tree.get_children())
        cuisine = self.cuisine_var.get().strip()
        results = self.browsing.search_by_filters(cuisine_type=cuisine if cuisine else None)
        try:
            max_rating = float(self.max_rating_var.get().strip()) if self.max_rating_var.get().strip() else 5
            max_delivery_time = int(self.max_delivery_var.get().strip()) if self.max_delivery_var.get().strip() else 60
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for rating and delivery time.")
            return

        # Apply filters
        filtered_restaurants = self.restaurant_filter.apply_filters(
            cuisine_type=cuisine,
            max_rating=max_rating,
            max_time=max_delivery_time
        )
        for r in results:
            self.results_tree.insert("", "end", values=(r["cuisine"], r["location"], r["rating"]))

    def view_all_restaurants(self):
        self.results_tree.delete(*self.results_tree.get_children())
        results = self.database.get_restaurants()
        for r in results:
            self.results_tree.insert("", "end", values=(r["cuisine"], r["location"], r["rating"]))

    def add_item_to_cart(self):
        # For simplicity, let's assume user always adds "Pizza"
        # A more sophisticated approach: Let user select from menu items.
        # We will show a small popup to choose items.
        menu_popup = AddItemPopup(self, self.restaurant_menu, self.cart)
        self.wait_window(menu_popup)

    def view_cart(self):
        cart_view = CartViewPopup(self, self.cart)
        self.wait_window(cart_view)

    def checkout(self):
        # Validate order and proceed if valid
        validation = self.order_placement.validate_order()
        if not validation["success"]:
            messagebox.showerror("Error", validation["message"])
            return

        # Show Checkout Popup
        checkout_popup = CheckoutPopup(self, self.order_placement)
        self.wait_window(checkout_popup)

