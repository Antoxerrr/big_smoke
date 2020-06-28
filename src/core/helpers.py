from telegram import ReplyKeyboardMarkup


def build_menu(
        buttons: list,
        columns: int = 3,
        header_button=None,
        footer_button=None,
        resize_keyboard: bool = True
):
    """Хелпер для удобного построения меню."""
    menu = [buttons[i:i + columns] for i in range(0, len(buttons), columns)]
    if header_button:
        menu.insert(0, [header_button])
    if footer_button:
        menu.append([footer_button])

    return ReplyKeyboardMarkup(menu, resize_keyboard=resize_keyboard)
