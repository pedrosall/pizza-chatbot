from enum import Enum


class ConversationState(Enum):

    ASK_NAME = 1
    ASK_PIZZA = 2
    ASK_SIZE = 3
    ASK_QUANTITY = 4
    ASK_DRINK = 5
    ASK_ADDRESS = 6
    CONFIRM = 7