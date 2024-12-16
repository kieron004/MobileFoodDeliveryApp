# FutureOrdersWishlist.py

class FutureOrdersWishlist:
    """
    管理用户的未来订单愿望清单。用户可以添加、删除或查看他们的未来愿望订单。
    """

    def __init__(self):
        self.wishlist = []

    def add_to_wishlist(self, item, price, quantity):
        """
        添加商品到未来订单愿望清单。

        参数：
            item (str): 商品名称。
            price (float): 商品单价。
            quantity (int): 商品数量。
        """
        self.wishlist.append({"item": item, "price": price, "quantity": quantity, "subtotal": price * quantity})
        return f"{item} have been added to the wish list for future orders。"

    def remove_from_wishlist(self, item):
        """
        从未来订单愿望清单中移除指定商品。

        参数：
            item (str): 商品名称。
        """
        for i in self.wishlist:
            if i["item"] == item:
                self.wishlist.remove(i)
                return f"{item} 已从愿望清单中移除。"
        return f"{item} 不在愿望清单中。"

    def view_wishlist(self):
        """
        查看当前未来订单愿望清单。

        返回：
            list: 当前愿望清单的所有商品信息。
        """
        return self.wishlist

    def clear_wishlist(self):
        """
        清空未来订单愿望清单。
        """
        self.wishlist.clear()
        return "愿望清单已清空。"
