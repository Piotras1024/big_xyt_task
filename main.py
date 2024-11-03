# main.py

from structure_order import Order

# Initial data
initial_data = [
    "001, Buy,  Add, 20.00, 100",
    "002, Sell,  Add, 25.00, 200",
    "003, Buy,  Add, 23.00, 50",
    "004, Buy,  Add, 23.00, 70",
    "003, Buy,  Remove",
    "005, Sell , Add, 28.00, 100"
]

# Processing initial data
for line in initial_data:
    # Split and strip the line to get the fields
    parts = [part.strip() for part in line.split(',')]
    order_id_str = parts[0]
    order_type = parts[1]
    action = parts[2]

    # Parse order_id as integer, removing leading zeros
    order_id_parsed = int(order_id_str.lstrip('0'))

    if action == 'Add':
        price = float(parts[3])
        quantity = float(parts[4])  # Quantity as float
        # Create an Order object
        order = Order(order_id_parsed, order_type, action, price, quantity)
    elif action == 'Remove':
        # Create an Order object without price and quantity
        order = Order(order_id_parsed, order_type, action)
    else:
        print(f"Unknown action: {action}")
        continue

    # Process the order
    Order.process_order(order)

# Interactive input loop
print("Type list to see all transactions You can now enter new transactions.")
print('Type "exit" at any prompt to quit.\n')

while True:
    try:
        # Input Order ID with new prompt
        order_id_input = input('You can now enter new transactions. Enter Order ID: ').strip()
        if order_id_input.lower() == 'exit':
            break
        if order_id_input.lower() == 'list':
            Order.list_transactions()
            continue  # Go back to the start of the loop

        # Parse order_id as integer
        order_id_parsed = int(order_id_input)

        # Input Order Type
        order_type = input("Enter order type (Buy/Sell): ").strip()
        if order_type.lower() == 'exit':
            break
        if order_type not in ('Buy', 'Sell'):
            print("Invalid order type. Please enter 'Buy' or 'Sell'.")
            continue

        # Input Action
        action = input("Enter action (Add/Remove): ").strip()
        if action.lower() == 'exit':
            break
        if action not in ('Add', 'Remove'):
            print("Invalid action. Please enter 'Add' or 'Remove'.")
            continue

        if action == 'Add':
            # Input Price
            price_input = input("Enter price: ").strip()
            if price_input.lower() == 'exit':
                break
            price = float(price_input)

            # Input Quantity
            quantity_input = input("Enter quantity: ").strip()
            if quantity_input.lower() == 'exit':
                break
            quantity = float(quantity_input)  # Quantity as float

            # Create an Order object
            order = Order(order_id_parsed, order_type, action, price, quantity)
        elif action == 'Remove':
            # No need to input Price and Quantity
            # Create an Order object without price and quantity
            order = Order(order_id_parsed, order_type, action)

        # Process the order
        success = Order.process_order(order)

        # Confirmation message
        if success:
            print(f"Transaction {order_id_parsed} has been processed.\n")
        else:
            print(f"Transaction {order_id_parsed} failed.\n")

    except ValueError as e:
        print(f"Invalid input: {e}. Please try again.\n")
    except Exception as e:
        print(f"An error occurred: {e}. Please try again.\n")
