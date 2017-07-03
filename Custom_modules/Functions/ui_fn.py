from PyQt5 import QtWidgets

def clear_widget(obj):
    """
    Полность очищает виджет
    :param obj: Объект виджета
    :return: None
    """
    for i in reversed(range(obj.count())):
        obj.itemAt(i).widget().setParent(None)



def show_error_msg_window(error_title: str, message_text: str, parent=None):
    """
    Функция показывает окно вывода ошибки

    :param error_title: Заголовок окна
    :param message_text: Текст ошибки
    :param parent: Родитель в котором создавать окно
    :return: QErrorMessage.show()
    """
    error_msg = QtWidgets.QErrorMessage(parent)
    error_msg.setWindowTitle(error_title)
    error_msg.showMessage(message_text)
    error_msg.show()
