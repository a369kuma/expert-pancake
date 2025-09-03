import math

class Warehouse:
    def __init__(self, city: str, country: str, coordinates: list, stock: int):
        self.city = city
        self.country = country
        self.coordinates = coordinates
        self.stock = stock

class Buyer:
    def __init__(self, city: str, country: str, coordinates: list, order_quantity: int):
        self.city = city
        self.country = country
        self.coordinates = coordinates
        self.order_quantity = order_quantity

class DeliveryStrategy:
    def __init__(self, closest_to_buyer: bool, within_country: bool, stock_availability: bool):
        self.closest_to_buyer = closest_to_buyer
        self.within_country = within_country
        self.stock_availability = stock_availability

class Order:
    def __init__(self, buyer: Buyer, product: str, quantity: int):
        self.buyer = buyer
        self.product = product
        self.quantity = quantity

def get_warehouse_in_country(order: Order, warehouses: list):
    return [warehouse for warehouse in warehouses if warehouse.country == order.buyer.country]

def get_warehouse_closest_to_buyer(order: Order, warehouses: list):
    buyer_location = order.buyer.coordinates
    closest_warehouse = None
    min_distance = float('inf')

    for warehouse in warehouses:
        distance = math.sqrt((warehouse.coordinates[0] - buyer_location[0])**2 
                             + (warehouse.coordinates[1] - buyer_location[1])**2)

        if distance < min_distance:
            min_distance = distance
            closest_warehouse = warehouse

    return closest_warehouse

def get_best_fulfillment_location(order: Order, warehouses: list):
    return [warehouse for warehouse in warehouses if warehouse.stock >= order.quantity]

def get_warehouse_with_stock_available(order: Order, warehouses: list):
    return [warehouse for warehouse in warehouses if warehouse.stock >= order.quantity]

def get_fulfillment_location(strategy: DeliveryStrategy, order: Order, warehouses: list):
    stock_available = get_warehouse_with_stock_available(order, warehouses)

    warehouses_in_country = get_warehouse_in_country(order, stock_available) if strategy.within_country else stock_available
   
    closest_warehouse = get_warehouse_closest_to_buyer(order, warehouses_in_country) if strategy.closest_to_buyer else warehouses_in_country
    if closest_warehouse:
        return closest_warehouse
    return " "

def get_fulfillment_location_with_priority(self, order: Order, warehouse: list, priority: list):
    filtered_warehouses = warehouse

    if not filtered_warehouses:
        return " "

    if filtered_warehouses:
        return filtered_warehouses[0]
    return " "






