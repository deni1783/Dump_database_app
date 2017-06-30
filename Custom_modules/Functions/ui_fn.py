def clear_widget(obj):
    """
    Полность очищает виджет
    :param obj: Объект виджета
    :return: None
    """
    for i in reversed(range(obj.count())):
        obj.itemAt(i).widget().setParent(None)