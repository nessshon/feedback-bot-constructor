from ._init_value import InitValue
from ._language_code import LanguageCode


class MessageCode(InitValue):
    in_development: str

    main_menu: str
    send_token: str
    select_group: str
    group_connected: str
    group_waiting: str
    group_disconnected: str

    bot_list: str
    bot_info: str

    user_list: str
    user_info: str

    text_list: str
    text_info: str
    text_edit_text: str
    text_edit_text_confirm: str
    text_edit_media: str
    text_edit_media_confirm: str


class TextMessage:
    """
    Class representing a text message.
    """
    data = {
        LanguageCode.en: {
            MessageCode.in_development: "🚧 Feature in Development",

            MessageCode.main_menu: "🏠 Main Menu",
            MessageCode.send_token: "🤖 Create a New Bot",
            MessageCode.select_group: "👥 Select a Group",

            # Групповые сообщения
            MessageCode.group_connected: "✅ The group '{group_title}' has been successfully connected "
                                         "to your bot @{bot_username}!",
            MessageCode.group_waiting: "⌛ The group '{group_title}' is not currently connected "
                                       "to your bot @{bot_username}! "
                                       "Please grant the bot administrator rights.",
            MessageCode.group_disconnected: "❌ The group '{group_title}' has been disconnected "
                                            "from your bot @{bot_username}!",

            # Сообщения о боте
            MessageCode.bot_list: "🤖 List of Bots:",
            MessageCode.bot_info: "🤖 Bot Information",

            # Сообщения о пользователях
            MessageCode.user_list: "👤 List of Users:",
            MessageCode.user_info: "👤 User Information",

            # Сообщения о тексте
            MessageCode.text_list: "📜 List of Messages:",
            MessageCode.text_info: "📜 Message Information",
            MessageCode.text_edit_text: "✏️ Edit Message Text\n\n"
                                        "Current text:\n"
                                        "{old_text}\n\n"
                                        "Please send the new text:",
            MessageCode.text_edit_text_confirm: "✅ Confirm Edit Message Text\n\n"
                                                "New text:\n"
                                                "{new_text}\n\n"
                                                "Confirm?",
            MessageCode.text_edit_media: "🖼️ Edit Message Media\n\n"
                                         "Current media URL:\n"
                                         "{old_media}\n",
            MessageCode.text_edit_media_confirm: "✅ Confirm Edit Message Media\n\n"
                                                 "New media URL:\n"
                                                 "{new_media_url}\n\n"
                                                 "Confirm?",
        },
        LanguageCode.ru: {
            MessageCode.in_development: "🚧 Функция в разработке",

            MessageCode.main_menu: "🏠 Главное меню",
            MessageCode.send_token: "🤖 Создать нового бота",
            MessageCode.select_group: "👥 Выбрать группу",

            # Групповые сообщения
            MessageCode.group_connected: "✅ Группа '{group_title}' успешно подключена к вашему боту @{bot_username}!",
            MessageCode.group_waiting: "⌛ Группа '{group_title}' в данный момент не подключена "
                                       "к вашему боту @{bot_username}! "
                                       "Пожалуйста, предоставьте боту права администратора.",
            MessageCode.group_disconnected: "❌ Группа '{group_title}' была отключена от вашего бота @{bot_username}!",

            # Сообщения о боте
            MessageCode.bot_list: "🤖 Список ботов:",
            MessageCode.bot_info: "🤖 Информация о боте",

            # Сообщения о пользователях
            MessageCode.user_list: "👤 Список пользователей:",
            MessageCode.user_info: "👤 Информация о пользователе",

            # Сообщения о тексте
            MessageCode.text_list: "📜 Список сообщений:",
            MessageCode.text_info: "📜 Информация о сообщении",
            MessageCode.text_edit_text: "✏️ Редактировать текст сообщения\n\n"
                                        "Текущий текст:\n"
                                        "{old_text}\n\n"
                                        "Пожалуйста, отправьте новый текст:",
            MessageCode.text_edit_text_confirm: "✅ Подтвердить редактирование текста сообщения\n\n"
                                                "Новый текст:\n"
                                                "{new_text}\n\n"
                                                "Подтвердить?",
            MessageCode.text_edit_media: "🖼️ Редактировать медиафайл сообщения\n\n"
                                         "Текущая ссылка на медиафайл:\n"
                                         "{old_media}\n",
            MessageCode.text_edit_media_confirm: "✅ Подтвердить редактирование медиафайла сообщения\n\n"
                                                 "Новая ссылка на медиафайл:\n"
                                                 "{new_media_url}\n\n"
                                                 "Подтвердить?",
        },
    }

    def __init__(self, language_code: str) -> None:
        """
        Initialize the TextMessage object.

        :param language_code: The language code for the text message.
        """
        self.language_code = language_code

    def get(self, code: str) -> str:
        """
        Returns the text corresponding to the given code.

        :param code: The code for which the text is to be retrieved.
        :return: The text corresponding to the given code.
        """
        return self.data[self.language_code][code]
