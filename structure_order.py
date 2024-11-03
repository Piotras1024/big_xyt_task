# order.py

class Order:
    # Class variables to store all orders
    orders_by_id = {}
    buy_orders = {}   # price -> list of orders
    sell_orders = {}  # price -> list of orders

    def __init__(self, order_id, order_type, action, price=None, quantity=None):
        self.order_id = order_id        # int
        self.order_type = order_type    # 'Buy' or 'Sell'
        self.action = action            # 'Add' or 'Remove'
        self.price = price              # float, can be None for 'Remove'
        self.quantity = quantity        # float with two decimal places, can be None for 'Remove'

    def __str__(self):
        if self.quantity is not None:
            return (f"Order ID: {self.order_id}, Type: {self.order_type}, Action: {self.action}, "
                    f"Price: {self.price}, Quantity: {self.quantity:.2f}")
        else:
            return (f"Order ID: {self.order_id}, Type: {self.order_type}, Action: {self.action}")

    @classmethod
    def process_order(cls, order):
        current_order_id = order.order_id
        order_type = order.order_type
        action = order.action
        price = order.price
        quantity = order.quantity

        if action == 'Add':
            # Add order to orders_by_id
            if current_order_id in cls.orders_by_id:
                print(f"Order ID {current_order_id} already exists. Cannot add a duplicate.")
                return False  # Indicate failure
            cls.orders_by_id[current_order_id] = order

            # Update buy_orders or sell_orders
            if order_type == 'Buy':
                if price not in cls.buy_orders:
                    cls.buy_orders[price] = []
                cls.buy_orders[price].append(order)
            else:  # 'Sell'
                if price not in cls.sell_orders:
                    cls.sell_orders[price] = []
                cls.sell_orders[price].append(order)

        elif action == 'Remove':
            # Check if the order exists
            if current_order_id in cls.orders_by_id:
                existing_order = cls.orders_by_id[current_order_id]
                # Check if the order type matches
                if existing_order.order_type == order_type:
                    # Remove the order from orders_by_id
                    del cls.orders_by_id[current_order_id]

                    # Remove the order from buy_orders or sell_orders
                    if existing_order.order_type == 'Buy':
                        orders_at_price = cls.buy_orders.get(existing_order.price, [])
                        orders_at_price = [o for o in orders_at_price if o.order_id != current_order_id]
                        if not orders_at_price:
                            del cls.buy_orders[existing_order.price]
                        else:
                            cls.buy_orders[existing_order.price] = orders_at_price
                    else:  # 'Sell'
                        orders_at_price = cls.sell_orders.get(existing_order.price, [])
                        orders_at_price = [o for o in orders_at_price if o.order_id != current_order_id]
                        if not orders_at_price:
                            del cls.sell_orders[existing_order.price]
                        else:
                            cls.sell_orders[existing_order.price] = orders_at_price
                else:
                    print(f"Order type does not match for Order ID {current_order_id}. Cannot remove.")
                    return False  # Indicate failure
            else:
                print(f"Order ID {current_order_id} not found for removal.")
                return False  # Indicate failure

        # Display best buy and sell orders
        print(f"\nAfter processing order {current_order_id}:")
        cls.display_best_orders()
        return True  # Indicate success

    @classmethod
    def display_best_orders(cls):
        # Best buy order: lowest price, if multiple then highest quantity
        if cls.buy_orders:
            min_buy_price = min(cls.buy_orders.keys())
            orders_at_min_price = cls.buy_orders[min_buy_price]
            best_buy_order = max(orders_at_min_price, key=lambda o: o.quantity)
            print(f"Best buy order - Price: {best_buy_order.price}, Quantity: {best_buy_order.quantity:.2f}")
        else:
            print("No buy orders")

        # Best sell order: highest price, if multiple then highest quantity
        if cls.sell_orders:
            max_sell_price = max(cls.sell_orders.keys())
            orders_at_max_price = cls.sell_orders[max_sell_price]
            best_sell_order = max(orders_at_max_price, key=lambda o: o.quantity)
            print(f"Best sell order - Price: {best_sell_order.price}, Quantity: {best_sell_order.quantity:.2f}")
        else:
            print("No sell orders")
        print()  # Blank line for readability

    @classmethod
    def list_transactions(cls):
        if not cls.orders_by_id:
            print("No available transactions.")
        else:
            print("\nCurrent transactions:")
            for order_id_key in sorted(cls.orders_by_id.keys()):
                order = cls.orders_by_id[order_id_key]
                print(order)
            print()  # Blank line for readability
