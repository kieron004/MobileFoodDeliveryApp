class RestaurantFilter:
    def __init__(self, restaurants):
        self.restaurants = restaurants

    def search_by_filters(self, cuisine_type=None, max_rating=5, max_delivery_time=60):
        """
        Filters the list of restaurants based on the provided filters.

        Args:
            cuisine_type (str): The cuisine type to filter by.
            max_rating (float): The maximum rating for the restaurant.
            max_delivery_time (int): The maximum delivery time (in minutes).

        Returns:
            list: A list of restaurants that match the given filters.
        """
        filtered_restaurants = self.restaurants

        # Apply filters based on cuisine type
        if cuisine_type:
            filtered_restaurants = [r for r in filtered_restaurants if cuisine_type.lower() in r["cuisine"].lower()]

        # Apply filter based on rating
        filtered_restaurants = [r for r in filtered_restaurants if r["rating"] >= max_rating]

        # Apply filter based on delivery time
        filtered_restaurants = [r for r in filtered_restaurants if r["delivery_time"] <= max_delivery_time]

        return filtered_restaurants
