
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

from import_data import import_data
   # State definitions for top level conversation - 
    # Определения состояния для разговора на высшем уровне
#SELECTING_ACTION, ADDING_MEMBER, ADDING_SELF, DESCRIBING_SELF = map(chr, range(4))
SELECTING_ACTION, ADDING_SELF, DESCRIBING_SELF, WORK_SCHEDULE , NUMBERS= map(chr, range(5))
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

    # Different constants for this example
(
    PARENTS,
    CHILDREN,
    SELF,
    GENDER,
    MALE,
    FEMALE,
    AGE,
    NAME,
    START_OVER,
    FEATURES,
    CURRENT_FEATURE,
    CURRENT_LEVEL,
    # WORK_SCHEDULE
) = map(chr, range(10, 22))

from import_data_visitors import import_data_visitors
    # Helper
# def _name_switcher(level: str) -> Tuple[str, str]:
#     if level == PARENTS:
#         return "Father", "Mother"
#     return "Brother", "Sister"


    # Top level conversation callbacks
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    text = (
        "Вы можете добавить информацию о себе, \n1)  для получения информация"
        " о вашей записи,\n2) запроса звонка из клиники, \n3) получение актуальной информации. "
        "\n Чтобы прервать, просто введите /stop."
    )
    # сартовые кнопки 
    buttons = [
        [
            InlineKeyboardButton(text="Добавьте себя", callback_data=str(ADDING_SELF)),
            InlineKeyboardButton(text="Наш сайт", url="https://alfamed.info/"),
        ],
                [
            InlineKeyboardButton(text="Адреса и график работы офисов", callback_data=str(WORK_SCHEDULE)),
            InlineKeyboardButton(text="Номера клиник", callback_data=str(NUMBERS)),
        ],
        [
            InlineKeyboardButton(text="Показывать данные", callback_data=str(SHOWING)),
            #окончание работы с программой
            InlineKeyboardButton(text="Закончить диалог", callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
        # Если мы начинаем все сначала, нам не нужно отправлять новое сообщение
    if context.user_data.get(START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        await update.message.reply_text(
            "Сеть медицинских центров АльфаМед приветствует Вас! Наш  телефон 8 (812) 200-42-42"
        )
        await update.message.reply_text(text=text, reply_markup=keyboard)
    import_data_visitors(update.message.from_user)
    context.user_data[START_OVER] = False
    return SELECTING_ACTION


async def adding_self(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Add information about yourself."""
    context.user_data[CURRENT_LEVEL] = SELF
    
    text = "Хорошо, пожалуйста, расскажи мне о себе."
    button = InlineKeyboardButton(text="Добавить информцию", callback_data=str(MALE))
    keyboard = InlineKeyboardMarkup.from_button(button)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return DESCRIBING_SELF
#
async def numbers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = ("Кудрово\nТел. 455-33-52, 921-61-00  "
            "\nКупчино\nТел. 771-50-81, 921-41-00"
            "\nМурино\n Тел. 245-01-72, 940-94-07"
            "\nКолпино\n Тел. 460-99-00, (921) 912-03-00"
            "\nБеговая \n Тел. 493-78-30, 980-00-06"
            "\nАвтово  \n Тел. 753-77-57, +7(953) 375-82-74"
            "\nЧерная речка \n Тел. (921)900-90-42"
            "\nУдельная \n Тел. 304-70-20, 988-70-20"
            "\nРыбацкое \n Тел. 679-59-79, (911) 926-04-40"
            "\nБелы Куна \n Тел. 705-09-32, 921-00-88")
    # text += f"\n\nРодители:{pretty_print(user_data, PARENTS)}"
    # text += f"\n\nДети:{pretty_print(user_data, CHILDREN)}"
    buttons = [[InlineKeyboardButton(text="Вернуться", callback_data=str(SELECTING_ACTION))]]
    # buttons = [[InlineKeyboardButton(text="Сделано", callback_data=str(SELECTING_ACTION))]]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    # возвращает данные в начало 
    # async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    #     context.user_data[START_OVER] = True
    #     await start(update, context)

    # return END
    # context.user_data[START_OVER] = True

    # return WORK_SCHEDULE
#
async def work_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = ("г. Кудрово, Европейский пр., 8 , \n ежедневно 08:00-21:00"
            "\nул. Купчинская, д. 21, корпус 1 ,\n ежедневно 09:00-21:00"
            "\nг. Мурино  Охтинская ал., д. 16 , \n ежедневно 08:00-21:00"
            "\nг. Колпино ул. Пролетарская, д. 46 ,\n ежедневно 9:00-21:00"
            "\nм. Беговая ул. Туристcкая, д. 24/42 ,\n ежедневно 09:00-21:00"
            "\nм. Автово ул. Маршала Казакова, д. 9, к. 1 , \n ПН–СБ с 9.00-21.00; ВСК с 9.00-15.00 "
            "\nм. Черная речка ул. Белоостровская, д. 10/1 ,\n ежедневно 09:00-21:00"
            "\nм. Удельная Земский пер., д. 11 кор. 1 ,\n ПН, ВТ, СР, ЧТ - 09:00 до 21:00"
            "\n ПТ - выходной \n СБ, ВС - 09:00 до 17:00"
            "\nм. Рыбацкое \n ул. Караваевская ул. Караваевская, д. 22 ,\n ежедневно 09:00-21:00"
            "\nул. Белы Куна, д. 6, корпус 1 ,\n ежедневно 09:00-21:00")
    # text += f"\n\nРодители:{pretty_print(user_data, PARENTS)}"
    # text += f"\n\nДети:{pretty_print(user_data, CHILDREN)}"
    buttons = [[InlineKeyboardButton(text="Вернуться", callback_data=str(SELECTING_ACTION))]]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    # user_data[START_OVER] = True

    # return WORK_SCHEDULE

async def show_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Pretty print gathered data."""

    def pretty_print(data: Dict[str, Any], level: str) -> str:
        people = data.get(level)
        if not people:
            return "\nПока никакой информации."

        return_str = ""
        if level == SELF:
            for person in data[level]:
                return_str += f"\nИмя: {person.get(NAME, '-')}, Телефон: {person.get(AGE, '-')}"
        # else:
            # male, female = _name_switcher(level)

            # for person in data[level]:
            #     gender = female if person[GENDER] == FEMALE else male
            #     return_str += (
            #         f"\n{gender}: Имя: {person.get(NAME, '-')}, Возраст: {person.get(AGE, '-')}"
            #     )
        return return_str

    user_data = context.user_data
    text = f"О себе:{pretty_print(user_data, SELF)}"
    # text += f"\n\nРодители:{pretty_print(user_data, PARENTS)}"
    # text += f"\n\nДети:{pretty_print(user_data, CHILDREN)}"

    buttons = [[InlineKeyboardButton(text="Обратно", callback_data=str(END))]]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    user_data[START_OVER] = True

    return SHOWING

    # Second level conversation callbacks второй уровень отета 

async def select_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Choose to add a parent or a child."""
    text = "You may add a parent or a child. Also you can show the gathered data or go back."
    buttons = [
        [
            InlineKeyboardButton(text="Добавить родителя", callback_data=str(PARENTS)),
            # InlineKeyboardButton(text="Добавить ребенка", callback_data=str(CHILDREN)),
        ],
        [
            InlineKeyboardButton(text="Показать данные", callback_data=str(SHOWING)),
            InlineKeyboardButton(text="Обратно", callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return SELECTING_LEVEL

async def select_gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Choose to add mother or father."""
    level = update.callback_query.data
    context.user_data[CURRENT_LEVEL] = level

    text = "Пожалуйста, выберите, кого добавить."

    # male, female = _name_switcher(level)

    buttons = [
        [
            # InlineKeyboardButton(text=f"Добавить {male}", callback_data=str(MALE)),
            # InlineKeyboardButton(text=f"Добавить {female}", callback_data=str(FEMALE)),
        ],
        [
            InlineKeyboardButton(text="Показать данные", callback_data=str(SHOWING)),
            InlineKeyboardButton(text="Обратно", callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return SELECTING_GENDER

async def end_second_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Return to top level conversation."""
    # Вернемся к разговору на высшем уровне
    context.user_data[START_OVER] = True
    await start(update, context)

    # return END


    # Third level callbacks

async def select_feature(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select a feature to update for the person."""
    buttons = [
        [
            InlineKeyboardButton(text="Имя", callback_data=str(NAME)),
            InlineKeyboardButton(text="Ваш телефон", callback_data=str(AGE)),
            InlineKeyboardButton(text="Сохранить", callback_data=str(END)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

        # If we collect features for a new person, clear the cache and save the gender
        #  Если мы собираем данные для нового человека, очистите кэш и сохраните пол
    if not context.user_data.get(START_OVER):
        context.user_data[FEATURES] = {GENDER: update.callback_query.data}
        text = "Пожалуйста, выберите функцию для обновления."

        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
        # But after we do that, we need to send a new message
        # Но после того, как мы это сделаем, нам нужно будет отправить новое сообщение
    else:
        text = "Понял! Пожалуйста, выберите функцию для обновления"
        await update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False
    return SELECTING_FEATURE

async def ask_for_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Prompt user to input data for selected feature."""
    # Предложите пользователю ввести данные для выбранной функции.
    context.user_data[CURRENT_FEATURE] = update.callback_query.data
    text = "Ладно, расскажи мне."

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)

    return TYPING

async def save_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Save input for feature and return to feature selection."""
    # Сохраните вводимые данные для объекта и вернитесь к выбору объекта
    user_data = context.user_data
    user_data[FEATURES][user_data[CURRENT_FEATURE]] = update.message.text

    user_data[START_OVER] = True

    return await select_feature(update, context)

async def end_describing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End gathering of features and return to parent conversation."""
    # Завершите сбор функций и вернитесь к родительскому разговору.
    user_data = context.user_data
    level = user_data[CURRENT_LEVEL]
    if not user_data.get(level):
        user_data[level] = []
    user_data[level].append(user_data[FEATURES])
        # Print upper level menu 
        # Меню верхнего уровня печати
    if level == SELF:
        user_data[START_OVER] = True
        await start(update, context)
    else:
        await select_level(update, context)
    # нажатие кнопки сохранить
    import_data(user_data)
    print('end_describing')
    return END

async def stop_nested(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    # "Полностью завершите диалог из вложенного диалога.
    """Completely end conversation from within nested conversation."""
    await update.message.reply_text("Okay, bye.")

    return STOPPING

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End Conversation by command."""
    # Завершите разговор командой
    text = ("Увидимся позже!"
           "\Если хотите снова начать диалог введите /start")
    await update.message.reply_text(text =text)

    return END


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End conversation from InlineKeyboardButton."""
    #Завершить разговор с помощью встроенной клавиатуры
    await update.callback_query.answer()

    text = ("Увидимся позже!"
           "\Если хотите снова начать диалог введите /start")
    await update.callback_query.edit_message_text(text=text)

    return END

