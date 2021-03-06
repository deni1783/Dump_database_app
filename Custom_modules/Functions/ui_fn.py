from PyQt5 import QtWidgets, QtCore

def clear_widget(obj):
    """
    Полность очищает виджет
    :param obj: Объект виджета
    :return: None
    """
    for i in reversed(range(obj.count())):
        obj.itemAt(i).widget().setParent(None)


def move_widget_to_center(widget):
    """
    Функция выравниваем переданный виджет по центру экрана

    :param widget: виджет для центрирования
    :return: None
    """
    qr = widget.frameGeometry()
    cp = QtWidgets.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    widget.move(qr.topLeft())


def show_error_msg_window(error_title: str, message_text: str, parent=None):
    """
    Функция показывает окно вывода ошибки

    :param error_title: Заголовок окна
    :param message_text: Текст ошибки
    :param parent: Родитель в котором создавать окно
    :return: QErrorMessage.show()
    """
    error_msg = QtWidgets.QErrorMessage(parent)

    # Центрируем окно
    move_widget_to_center(error_msg)

    error_msg.setWindowTitle(error_title)
    error_msg.showMessage(message_text)
    error_msg.setWindowFlags(error_msg.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
    error_msg.show()



def change_cursor(cursor_type: str):
    """
    Изменение фнешнего вида курсора
    :param cursor_type: тип курсора: wait, normal
    :return: None
    """
    if cursor_type == 'wait':
        # Изменяем курсор в песочные часы
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
    elif cursor_type == 'normal':
        # Возвращаем обычный курсор
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)