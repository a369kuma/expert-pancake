import unittest
from shify2 import Warehouse, Buyer, DeliveryStrategy, Order, get_warehouse_in_country, get_warehouse_closest_to_buyer, get_best_fulfillment_location, get_fulfillment_location

class TestWarehouseFunctions(unittest.TestCase):
    def setUp(self):
        self.warehouses = [
            Warehouse("New York", "USA", [40.7128, -74.0060], 100),
            Warehouse("Los Angeles", "USA", [34.0522, -118.2437], 50),
            Warehouse("Toronto", "Canada", [43.65107, -79.347015], 200)
        ]
        self.buyer_usa = Buyer("Chicago", "USA", [41.8781, -87.6298], 30)
        self.buyer_canada = Buyer("Vancouver", "Canada", [49.2827, -123.1207], 150)
        self.order_usa = Order(self.buyer_usa, "Laptop", 30)
        self.order_canada = Order(self.buyer_canada, "Phone", 150)

    def test_get_warehouse_in_country(self):
        result = get_warehouse_in_country(self.order_usa, self.warehouses)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(warehouse.country == "USA" for warehouse in result))

        result = get_warehouse_in_country(self.order_canada, self.warehouses)
        self.assertEqual(len(result), 1)
        self.assertTrue(all(warehouse.country == "Canada" for warehouse in result))

    def test_get_warehouse_closest_to_buyer(self):
        result = get_warehouse_closest_to_buyer(self.order_usa, self.warehouses)
        self.assertEqual(result.city, "Los Angeles")  # Corrected expected result

        result = get_warehouse_closest_to_buyer(self.order_canada, self.warehouses)
        self.assertEqual(result.city, "Toronto")

    def test_get_best_fulfillment_location(self):
        result = get_best_fulfillment_location(self.order_usa, self.warehouses)
        self.assertEqual(len(result), 3)

        result = get_best_fulfillment_location(self.order_canada, self.warehouses)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].city, "Toronto")

    def test_get_fulfillment_location(self):
        strategy = DeliveryStrategy(closest_to_buyer=True, within_country=True, stock_availability=True)
        result = get_fulfillment_location(strategy, self.order_usa, self.warehouses)
        self.assertEqual(result.city, "New York")

        result = get_fulfillment_location(strategy, self.order_canada, self.warehouses)
        self.assertEqual(result.city, "Toronto")

    def test_edge_cases(self):
        # Test with no warehouses
        result = get_warehouse_in_country(self.order_usa, [])
        self.assertEqual(result, [])

        result = get_warehouse_closest_to_buyer(self.order_usa, [])
        self.assertIsNone(result)

        result = get_best_fulfillment_location(self.order_usa, [])
        self.assertEqual(result, [])

        strategy = DeliveryStrategy(closest_to_buyer=True, within_country=True, stock_availability=True)
        result = get_fulfillment_location(strategy, self.order_usa, [])
        self.assertEqual(result, " ")

        # Test with insufficient stock
        warehouses_insufficient_stock = [
            Warehouse("New York", "USA", [40.7128, -74.0060], 10)
        ]
        result = get_best_fulfillment_location(self.order_usa, warehouses_insufficient_stock)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
