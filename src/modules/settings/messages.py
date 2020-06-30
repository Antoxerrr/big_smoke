from smoking.modes_map import modes_map

MAIN_MENU_MESSAGE = 'Главное меню'
CHOOSE_MODE_MESSAGE = 'Выберите режим работы программы.'
ARE_YOU_SURE_MESSAGE = 'Вы уверены?'
SETTINGS_MESSAGE = 'Настройки'
PROGRAM_STOPPED_MESSAGE = (
    'Работа программы остановлена и весь прогресс сброшен.'
)
PROGRAM_STOPPING_CANCELED_MESSAGE = 'Остановка работы программы отменена.'
MODE_IS_SET_SUCCESS_MESSAGE = 'Новый режим успешно установлен **(%s)**'


def build_mode_is_set_message(mode_id):
    mode = modes_map.get(mode_id)
    if mode:
        return MODE_IS_SET_SUCCESS_MESSAGE % mode.name
