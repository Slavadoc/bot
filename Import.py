from typing import Any, Dict, Tuple

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
#SELECTING_ACTION, ADDING_SELF, DESCRIBING_SELF = map(chr, range(3))
DESCRIBING_SELF = ""
CURRENT_LEVEL = ""
SELF = ""
MALE = ""

async def adding_self(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Add information about yourself."""
    context.user_data[CURRENT_LEVEL] = SELF
    
    text = "Хорошо, пожалуйста, расскажи мне о себе."
    button = InlineKeyboardButton(text="Добавить информцию", callback_data=str(MALE))
    keyboard = InlineKeyboardMarkup.from_button(button)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return DESCRIBING_SELF