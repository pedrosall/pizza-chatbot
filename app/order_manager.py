from catalog import PIZZAS, BEBIDAS


def answer_price(text):

    for pizza in PIZZAS:
        if pizza in text:
            precios = PIZZAS[pizza]["precio"]
            return f"La pizza {pizza} cuesta: individual {precios['individual']}€, mediana {precios['mediana']}€, grande {precios['grande']}€"

    for bebida in BEBIDAS:
        if bebida in text:
            return f"La {bebida} cuesta {BEBIDAS[bebida]}€"

    return "¿De qué producto quieres saber el precio?"