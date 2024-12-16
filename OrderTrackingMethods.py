import folium
from folium.plugins import MarkerCluster
from geopy.distance import geodesic

class OrderTracker:
    def __init__(self, order_id, initial_location, order_route=[]):
        """
        初始化订单追踪器，包含订单ID，起始位置，以及订单路径（位置更新的列表）。
        :param order_id: 订单的唯一ID
        :param initial_location: 订单的起始位置 (latitude, longitude)
        :param order_route: 一个列表，包含订单路径上的每个位置 [(lat, lon), ...]
        """
        self.order_id = order_id
        self.initial_location = initial_location
        self.order_route = order_route

    def create_map(self):
        """
        创建一个交互式地图，展示订单的路径和当前位置。
        :return: folium.Map 对象
        """
        # 创建一个基于初始位置的地图
        order_map = folium.Map(location=self.initial_location, zoom_start=14)

        # 添加初始位置标记
        folium.Marker(self.initial_location, popup=f"Order {self.order_id} Started").add_to(order_map)

        # 添加路径标记（每次更新的地点）
        marker_cluster = MarkerCluster().add_to(order_map)
        for idx, location in enumerate(self.order_route):
            folium.Marker(location, popup=f"Order {self.order_id} - Stop {idx+1}").add_to(marker_cluster)

        # 返回地图对象
        return order_map

    def update_location(self, new_location):
        """
        更新订单当前位置并将其添加到路径中。
        :param new_location: 新位置 (lat, lon)
        """
        self.order_route.append(new_location)

    def get_distance_from_start(self):
        """
        计算订单从起始位置到当前位置的距离。
        :return: 返回距离（单位：公里）
        """
        if not self.order_route:
            return 0.0
        return geodesic(self.initial_location, self.order_route[-1]).kilometers

    def save_map(self, map_filename="order_map.html"):
        """
        将创建的地图保存为HTML文件，方便浏览器查看。
        :param map_filename: 保存地图的文件名
        """
        order_map = self.create_map()
        order_map.save(map_filename)

# 示例用法
if __name__ == "__main__":
    # 初始化订单追踪器，订单ID和起始位置 (纬度，经度)
    initial_location = (40.748817, -73.985428)  # 示例: 纽约市（帝国大厦）
    order_tracker = OrderTracker(order_id="12345", initial_location=initial_location)

    # 模拟订单路径更新
    order_tracker.update_location((40.749817, -73.986428))  # 更新1: 订单稍微移动
    order_tracker.update_location((40.750817, -73.987428))  # 更新2: 订单进一步移动
    order_tracker.update_location((40.751817, -73.988428))  # 更新3: 订单接近目的地

    # 保存地图为HTML文件
    order_tracker.save_map("order_12345_map.html")

    print(f"Distance from start: {order_tracker.get_distance_from_start()} km")
