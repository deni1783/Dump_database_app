if __name__ == '__main__':
    from PyQt5 import QtWidgets
    from Custom_modules.Main_window_classes.ApplicationLayout import ApplicationLayout
    import sys

    app = QtWidgets.QApplication(sys.argv)

    window = ApplicationLayout()
    window.setWindowTitle('DUMP')
    window.show()
    sys.exit(app.exec_())
