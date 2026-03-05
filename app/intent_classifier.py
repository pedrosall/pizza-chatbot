def classify_intent(text):

    text = text.lower()

    if "precio" in text or "cuanto vale" in text:
        return "price_question"

    if "que lleva" in text or "ingredientes" in text:
        return "ingredients_question"

    if "bebidas" in text or "que bebidas" in text:
        return "drink_list"

    if "pizza" in text:
        return "pizza_order"

    if text in ["no"]:
        return "no"

    return "unknown"