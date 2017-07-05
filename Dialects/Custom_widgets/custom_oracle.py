from PyQt5 import QtWidgets

def add_custom_settings(parent_vbox_object):
    test_lbl = QtWidgets.QLabel('test lbl for Oracle')
    parent_vbox_object.addWidget(test_lbl)