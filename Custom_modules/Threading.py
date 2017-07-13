from PyQt5 import QtCore

"""
    Класс для запуска переданной функции в отдельном потоке
    В качестве параметра функции передается каждый элемент из list_of_commands
"""
class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)
    code = None
    stdout = None
    stderr = None

    def __init__(self, list_of_commands, func, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.list_of_commands = list_of_commands
        self.func = func

    def run(self):
        for cmd in self.list_of_commands:
            self.mysignal.emit(cmd)
            self.func(cmd)


"""
    Класс для запуска переданной функции в отдельном потоке
    В качестве параметра функции передается каждый элемент (command) из obj_of_commands
    key нужен для отображения логирования
    
    obj_of_commands = {
        key: command
    }
"""
class MyThreadObj(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)
    code = None
    stdout = None
    stderr = None

    def __init__(self, obj_of_commands, func, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.obj_of_commands = obj_of_commands
        self.func = func

    def run(self):
        for cmd in self.obj_of_commands:
            self.mysignal.emit(cmd)
            self.func(self.obj_of_commands[cmd])
