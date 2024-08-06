
from typing import Any, Dict, Tuple

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from bots_comands import (
    stop_nested,
    end_describing, 
    save_input, 
    ask_for_input, 
    select_feature,
    work_schedule,
    end_second_level,
    select_gender,
    select_level,
    adding_self,
    end,
    stop,
    show_data,
    start,
    numbers
)  

import logging


    # Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
    # set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

with open('token/token.txt', "r") as my_file:
    TOKEN = my_file.read()
    # State definitions for top level conversation - 
    # Определения состояния для разговора на высшем уровне
#SELECTING_ACTION, ADDING_MEMBER, ADDING_SELF, DESCRIBING_SELF = map(chr, range(4))
# SELECTING_ACTION, ADDING_SELF, DESCRIBING_SELF = map(chr, range(3))
SELECTING_ACTION, ADDING_SELF, DESCRIBING_SELF, WORK_SCHEDULE, NUMBERS = map(chr, range(5))
    # State definitions for second level conversation 
    # Определения состояний для диалога второго уровня
SELECTING_LEVEL, SELECTING_GENDER = map(chr, range(4, 6))
    # State definitions for descriptions conversation 
    #  Определения состояний для диалога описаний
SELECTING_FEATURE, TYPING = map(chr, range(6, 8))
    # Meta states
STOPPING, SHOWING = map(chr, range(8, 10))
    # Shortcut for ConversationHandler.END  
    # Ярлык для обработчика разговоров.КОНЕЦ
END = ConversationHandler.END

# Different constants for this example Константы 
(
    PARENTS,
    CHILDREN,
    SELF,
    GENDER,
    MALE,
    # FEMALE,
    AGE,
    NAME,
    START_OVER,
    FEATURES,
    CURRENT_FEATURE,
    CURRENT_LEVEL,
    ADDING_MEMBER,
) = map(chr, range(10, 22))  

def main() -> None:
    """Run the bot."""
    application = Application.builder().token(TOKEN).build()
        # Set up third level ConversationHandler (collecting features)
        #Настройка обработчика разговоров третьего уровня (сбор функций)
    description_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                select_feature, pattern="^" + str(MALE) + "$|^" #+ str(FEMALE) + "$"
            )
        ],
        states={
            SELECTING_FEATURE: [
                CallbackQueryHandler(ask_for_input, pattern="^(?!" + str(END) + ").*$")
            ],
            TYPING: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_input)],
        },
        fallbacks=[
            CallbackQueryHandler(end_describing, pattern="^" + str(END) + "$"),
            CommandHandler("stop", stop_nested),
        ],
        map_to_parent={
                # Return to second level menu
                #Вернуться к меню второго уровня
             END: SELECTING_LEVEL,
                # End conversation altogether
                # Закончите разговор вообще
            STOPPING: STOPPING,
        },
    )

        # Set up second level ConversationHandler (adding a person)
        # Настройка обработчика разговоров второго уровня (добавление пользователя)
    add_member_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(select_level, pattern="^" + str(ADDING_MEMBER) + "$")],
        states={
            SELECTING_LEVEL: [
                CallbackQueryHandler(select_gender, pattern=f"^{PARENTS}$|^{CHILDREN}$")
            ],
            SELECTING_GENDER: [description_conv],
        },
        fallbacks=[
            CallbackQueryHandler(show_data, pattern="^" + str(SHOWING) + "$"),
            CallbackQueryHandler(end_second_level, pattern="^" + str(END) + "$"),
            CommandHandler("stop", stop_nested),
        ],
        map_to_parent={
                # After showing data return to top level menu
                # После отображения данных вернитесь в меню верхнего уровня
            SHOWING: SHOWING,
                # Return to top level menu
                # Вернуться к меню верхнего уровня
            END: SELECTING_ACTION,
                # End conversation altogether
                # Закончите разговор вообще
            STOPPING: END,
        },
    )

        # Set up top level ConversationHandler (selecting action)
        # Настройка обработчика разговоров верхнего уровня (выбор действия)
        # Because the states of the third level conversation map to the ones of the second level
        # Потому что состояния разговора третьего уровня соответствуют состояниям разговора второго уровня
        # conversation, we need to make sure the top level conversation can also handle them
        # разговор, мы должны убедиться, что разговор на высшем уровне также может справиться с ними
    selection_handlers = [
        add_member_conv, 
        CallbackQueryHandler(numbers, pattern="^" + str(NUMBERS) + "$"),
        CallbackQueryHandler(work_schedule, pattern="^" + str(WORK_SCHEDULE) + "$"),
        CallbackQueryHandler(show_data, pattern="^" + str(SHOWING) + "$"),
        CallbackQueryHandler(adding_self, pattern="^" + str(ADDING_SELF) + "$"),
        CallbackQueryHandler(end_second_level, pattern="^" + str(SELECTING_ACTION) + "$"),
        CallbackQueryHandler(end, pattern="^" + str(END) + "$"),
    ]
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SHOWING: [CallbackQueryHandler(start, pattern="^" + str(END) + "$")],
            SELECTING_ACTION: selection_handlers,
            SELECTING_LEVEL: selection_handlers,
            DESCRIBING_SELF: [description_conv],
            STOPPING: [CommandHandler("start", start)],
        },
        fallbacks=[CommandHandler("stop", stop)],
    )

    application.add_handler(conv_handler)
        # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


# if __name__ == "__main__":
#     main()