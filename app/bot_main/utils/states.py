from aiogram.fsm.state import StatesGroup
from aiogram.fsm.state import State as St


class State(StatesGroup):
    main_menu = St()
    create_bot = St()
    select_group = St()

    bot_list = St()
    bot_info = St()

    user_list = St()
    user_info = St()

    text_list = St()
    text_info = St()
    text_edit_text = St()
    text_edit_text_confirm = St()
    text_edit_media = St()
    text_edit_media_confirm = St()
