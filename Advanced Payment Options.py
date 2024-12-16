# payment_processing.py

class PaymentProcessing:
    def __init__(self):
        """
        Initializes the PaymentProcessing class with available payment gateways.
        """
        self.available_gateways = ["credit_card", "paypal", "gift_card"]  # 添加礼品卡支付选项

    def validate_payment_method(self, payment_method, payment_details):
        """
        Validates the selected payment method and its associated details.
        """
        # Check if the payment method is supported.
        if payment_method not in self.available_gateways:
            raise ValueError("Invalid payment method")

        if payment_method == "credit_card":
            if not self.validate_credit_card(payment_details):
                raise ValueError("Invalid credit card details")
        elif payment_method == "gift_card":
            if not self.validate_gift_card(payment_details):
                raise ValueError("Invalid gift card details")

        return True

    def validate_credit_card(self, details):
        """
        Validates the credit card details (e.g., card number, expiry date, CVV).
        """
        card_number = details.get("card_number", "")
        expiry_date = details.get("expiry_date", "")
        cvv = details.get("cvv", "")
        if len(card_number) != 16 or len(cvv) != 3:
            return False
        return True

    def validate_gift_card(self, details):
        """
        Validates the gift card details (e.g., card number, pin).
        """
        card_number = details.get("card_number", "")
        pin = details.get("pin", "")
        # Basic validation: Check if the card number is valid (for simplicity).
        if len(card_number) != 16 or len(pin) != 4:
            return False
        return True

    def process_payment(self, order, payment_methods):
        """
        Processes the payment for an order, supporting split payments and gift cards.

        Args:
            order (dict): The order details, including total amount.
            payment_methods (list): A list of dictionaries, each representing a payment method (credit_card, gift_card, etc.).

        Returns:
            str: A message indicating whether the payment was successful or failed.
        """
        total_amount = order["total_amount"]
        amount_remaining = total_amount

        for payment_method in payment_methods:
            method = payment_method["method"]
            details = payment_method["details"]

            # Validate payment method before proceeding
            self.validate_payment_method(method, details)

            if method == "credit_card":
                # Simulate payment with the provided credit card
                payment_response = self.mock_payment_gateway(method, details, payment_method["amount"])
            elif method == "gift_card":
                # Simulate gift card payment
                payment_response = self.mock_gift_card_payment(method, details, payment_method["amount"])

            if payment_response["status"] != "success":
                return f"Payment failed for {method}, please try again."

            amount_remaining -= payment_method["amount"]

            # If the entire amount has been paid, break out of the loop
            if amount_remaining <= 0:
                break

        # If the remaining amount is greater than zero, payment has not been completed
        if amount_remaining > 0:
            return "Payment failed, remaining balance needs to be paid."

        return "Payment successful, Order confirmed"

    def mock_payment_gateway(self, method, details, amount):
        """
        Simulates the interaction with a payment gateway for processing payments (e.g., credit card).
        """
        # Simulate card decline for a specific card number
        if method == "credit_card" and details["card_number"] == "1111222233334444":
            return {"status": "failure", "message": "Card declined"}
        return {"status": "success", "transaction_id": "abc123"}

    def mock_gift_card_payment(self, method, details, amount):
        """
        Simulates the interaction with a gift card payment system.
        """
        # Simulate gift card balance check
        if details[
            "card_number"] == "9876543210987654" and amount > 50:  # Simulating a gift card with a max balance of 50
            return {"status": "failure", "message": "Insufficient balance"}
        return {"status": "success", "transaction_id": "giftcard123"}
