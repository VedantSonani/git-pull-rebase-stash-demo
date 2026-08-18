def format_message(message):
    return message.strip().upper()


def calculate_total(price, quantity):
    return price * quantity


def is_valid_quantity(quantity):
    return quantity > 0