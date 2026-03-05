from app.catalog import PIZZAS, SIZES, DRINKS


def format_order(session):

    pizza = session["pizza"]
    size = session["size"]
    qty = session["quantity"]
    drink = session["drink"]
    address = session["address"]

    base_price = PIZZAS[pizza]["price"]
    size_multiplier = SIZES[size]

    pizza_price = base_price * size_multiplier * qty

    drink_price = 0
    if drink:
        drink_price = DRINKS[drink]

    total = pizza_price + drink_price

    text = f"""
🍕 Pedido

Pizza: {pizza}
Tamaño: {size}
Cantidad: {qty}
Bebida: {drink if drink else "ninguna"}

📍 Dirección
{address}

💰 Total aproximado: {round(total,2)}€
"""

    return text