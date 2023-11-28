from typing import List, Tuple, Optional

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot_main.utils.texts.buttons import TextButton
from app.bot_main.utils.texts.buttons import ButtonCode
from app.database.models import BotDB


def text_info(text_button: TextButton) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(
        *[
            text_button.get_button(ButtonCode.edit_text_ru),
            text_button.get_button(ButtonCode.edit_text_en),
            text_button.get_button(ButtonCode.edit_media_url),
            text_button.get_button(ButtonCode.back),
        ], width=1,
    )
    return builder


def export_tools(text_button: TextButton) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(
        *[
            text_button.get_button(ButtonCode.export_csv),
            text_button.get_button(ButtonCode.export_json),
        ], width=2,
    )
    return builder


def main_menu(text_button: TextButton) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(
        *[
            text_button.get_button(ButtonCode.create_bot),
            text_button.get_button(ButtonCode.bot_management),
        ], width=1,
    )

    return builder


def bot_information(text_button: TextButton, bot_db: BotDB) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    if bot_db.is_active:
        on_or_off_bot_callback_data = ButtonCode.shutdown
    else:
        on_or_off_bot_callback_data = ButtonCode.startup

    if bot_db.group_id:
        set_or_edit_group_callback_data = ButtonCode.edit_group
    else:
        set_or_edit_group_callback_data = ButtonCode.set_group

    builder.row(text_button.get_button(set_or_edit_group_callback_data))
    builder.row(
        *[
            text_button.get_button(ButtonCode.user_list),
            text_button.get_button(ButtonCode.text_list),
        ]
    )
    builder.row(
        *[
            text_button.get_button(on_or_off_bot_callback_data),
            text_button.get_button(ButtonCode.delete),
        ]
    )
    builder.row(text_button.get_button(ButtonCode.back))

    return builder


def select_group(text_button: TextButton, bot_username: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    url = (
        f"tg://resolve?domain={bot_username}&admin="
        f"manage_topics+"
        f"post_messages+"
        f"edit_messages+"
        f"delete_messages+"
        f"pin_messages"
        f"&startgroup"
    )
    builder.row(text_button.get_button(ButtonCode.select_group, url=url))
    builder.row(text_button.get_button(ButtonCode.back))
    return builder


def delete(text_button: TextButton) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.add(text_button.get_button(ButtonCode.delete))

    return builder


def skip(text_button: TextButton) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.add(text_button.get_button(ButtonCode.skip))

    return builder


def confirm(text_button: TextButton) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.add(text_button.get_button(ButtonCode.confirm))

    return builder


def back(text_button: TextButton) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.add(text_button.get_button(ButtonCode.back))

    return builder


def back_confirm(text_button: TextButton) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.attach(confirm(text_button))
    builder.attach(back(text_button))
    return builder


class InlineKeyboardPaginator:
    """
    A class that generates an inline keyboard for paginated data.

    Args:
        items (List[Tuple]): A list of tuples containing the data to be displayed in the keyboard.
        row_width (int): The number of buttons to be displayed per row.
        total_pages (int): The total number of pages.
        current_page (int): The current page number.
        data_pattern (str): The pattern to be used for the callback data.
        before_builder (InlineKeyboardBuilder): A builder to be attached before the items and navigation.
        after_builder (InlineKeyboardBuilder): A builder to be attached after the items and navigation.
    """

    first_page_label = "« {}"
    previous_page_label = "‹ {}"
    current_page_label = "· {} ·"
    next_page_label = "{} ›"
    last_page_label = "{} »"

    def __init__(
            self,
            items: List[Tuple],
            current_page: int = 1,
            total_pages: int = 1,
            row_width: int = 1,
            data_pattern: str = "page:{}",
            before_builder: Optional[InlineKeyboardBuilder] = None,
            after_builder: Optional[InlineKeyboardBuilder] = None,
    ) -> None:
        self.items = items
        self.current_page = current_page
        self.total_pages = total_pages
        self.row_width = row_width
        self.data_pattern = data_pattern

        self.builder = InlineKeyboardBuilder()
        self.before_builder = before_builder
        self.after_builder = after_builder

    def _items_builder(self) -> InlineKeyboardBuilder:
        """
        Generate the buttons for the items.
        """
        builder = InlineKeyboardBuilder()

        for key, val in self.items:
            builder.button(text=str(key), callback_data=str(val))
        builder.adjust(self.row_width)

        return builder

    def _navigation_builder(self) -> InlineKeyboardBuilder:
        """
        Generate the buttons for the navigation.
        """
        builder = InlineKeyboardBuilder()
        keyboard_dict = {}

        if self.total_pages > 1:
            if self.total_pages <= 5:
                for page in range(1, self.total_pages + 1):
                    keyboard_dict[page] = page
            else:
                if self.current_page <= 3:
                    page_range = range(1, 4)
                    keyboard_dict[4] = self.next_page_label.format(4)
                    keyboard_dict[self.total_pages] = self.last_page_label.format(self.total_pages)
                elif self.current_page > self.total_pages - 3:
                    keyboard_dict[1] = self.first_page_label.format(1)
                    keyboard_dict[self.total_pages - 3] = self.previous_page_label.format(self.total_pages - 3)
                    page_range = range(self.total_pages - 2, self.total_pages + 1)
                else:
                    keyboard_dict[1] = self.first_page_label.format(1)
                    keyboard_dict[self.current_page - 1] = self.previous_page_label.format(self.current_page - 1)
                    keyboard_dict[self.current_page + 1] = self.next_page_label.format(self.current_page + 1)
                    keyboard_dict[self.total_pages] = self.last_page_label.format(self.total_pages)
                    page_range = [self.current_page]
                for page in page_range:
                    keyboard_dict[page] = page
            keyboard_dict[self.current_page] = self.current_page_label.format(self.current_page)

            for key, val in sorted(keyboard_dict.items()):
                builder.button(text=str(val), callback_data=str(key))
            builder.adjust(5)

        return builder

    def as_markup(self) -> InlineKeyboardMarkup:
        """
        Generate main inline keyboard markup.
        """
        if self.before_builder:
            self.builder.attach(self.before_builder)

        self.builder.attach(self._items_builder())
        self.builder.attach(self._navigation_builder())

        if self.after_builder:
            self.builder.attach(self.after_builder)

        return self.builder.as_markup()
