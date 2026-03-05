import telebot
import os
from dotenv import load_dotenv

from app.state import ConversationState
from app.catalog import PIZZAS, SIZES, DRINKS
from app.formatters import format_order

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

sessions = {}


def get_session(chat_id):

    if chat_id not in sessions:
        sessions[chat_id] = {
            "state": ConversationState.ASK_NAME,
            "name": None,
            "pizza": None,
            "size": None,
            "quantity": None,
            "drink": None,
            "address": None
        }

    return sessions[chat_id]


@bot.message_handler(commands=['start'])
def start(message):

    chat_id = message.chat.id
    sessions.pop(chat_id, None)

    sessions[chat_id] = {
        "state": ConversationState.ASK_NAME,
        "name": None,
        "pizza": None,
        "size": None,
        "quantity": None,
        "drink": None,
        "address": None
    }

    bot.reply_to(message, "Hola 🍕 ¿Cómo te llamas?")


@bot.message_handler(func=lambda m: True)
def conversation(message):

    chat_id = message.chat.id
    text = message.text.lower()

    session = get_session(chat_id)
    state = session["state"]

    # PEDIR NOMBRE
    if state == ConversationState.ASK_NAME:

        session["name"] = text.capitalize()
        session["state"] = ConversationState.ASK_PIZZA

        bot.reply_to(
            message,
            f"Encantado {session['name']} 🍕 ¿Qué pizza te apetece?\nOpciones: {', '.join(PIZZAS)}"
        )
        return

    # PEDIR PIZZA
    if state == ConversationState.ASK_PIZZA:

        # preguntas sobre ingredientes
        if "lleva" in text or "ingredientes" in text:

            if "vegetariana" in text:
                bot.reply_to(message, "La pizza vegetariana lleva tomate, mozzarella, champiñones, pimiento y aceitunas.")
                return

            if "margarita" in text:
                bot.reply_to(message, "La margarita lleva tomate, mozzarella y albahaca.")
                return

            if "hawaiana" in text:
                bot.reply_to(message, "La hawaiana lleva jamón y piña.")
                return

            if "pepperoni" in text:
                bot.reply_to(message, "La pepperoni lleva tomate, mozzarella y pepperoni.")
                return

        # detectar pizza aunque haya más palabras
        for pizza in PIZZAS:
            if pizza in text:
                session["pizza"] = pizza
                session["state"] = ConversationState.ASK_SIZE

                bot.reply_to(
                    message,
                    f"Perfecto, una {pizza}. ¿Qué tamaño quieres? individual, mediana o grande"
                )
                return

        bot.reply_to(message, f"No tenemos esa pizza. Opciones: {', '.join(PIZZAS)}")
        return

    # PEDIR TAMAÑO
    if state == ConversationState.ASK_SIZE:

        if text not in SIZES:
            bot.reply_to(message, "Elige: individual, mediana o grande")
            return

        session["size"] = text
        session["state"] = ConversationState.ASK_QUANTITY

        bot.reply_to(message, "¿Cuántas unidades?")
        return

    # CANTIDAD
    if state == ConversationState.ASK_QUANTITY:

        try:
            qty = int(text)
        except:
            if text in ["una", "uno"]:
                qty = 1
            else:
                bot.reply_to(message, "Dime un número")
                return

        session["quantity"] = qty
        session["state"] = ConversationState.ASK_DRINK

        bot.reply_to(
            message,
            "¿Quieres alguna bebida?\n"
            f"Bebidas: {', '.join(DRINKS.keys())} o escribe 'no'"
        )
        return

    # BEBIDA
    if state == ConversationState.ASK_DRINK:

        if text == "no":
            session["drink"] = None

        elif text == "cuales hay":
            bot.reply_to(
                message,
                f"Bebidas disponibles: {', '.join(DRINKS.keys())}"
            )
            return

        elif text in DRINKS:
            session["drink"] = text

        else:
            bot.reply_to(message, "Elige una bebida válida o escribe 'no'")
            return

        session["state"] = ConversationState.ASK_ADDRESS

        bot.reply_to(message, "¿Cuál es tu dirección de entrega?")
        return

    # DIRECCIÓN
    if state == ConversationState.ASK_ADDRESS:

        session["address"] = message.text
        session["state"] = ConversationState.CONFIRM

        bot.reply_to(message, format_order(session) + "\n\n¿Confirmamos? (sí/no)")
        return

    # CONFIRMAR
    if state == ConversationState.CONFIRM:

        if text in ["si", "sí"]:
            bot.reply_to(message, "🍕 Pedido confirmado. ¡En camino!")
            sessions.pop(chat_id)

        else:
            bot.reply_to(message, "Pedido cancelado.")
            sessions.pop(chat_id)

        return


print("🤖 Bot iniciado")

bot.infinity_polling()