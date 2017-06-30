from Custom_modules.Main_window_classes.DialectListBox import DialectListBox


class ApplicationLayout(DialectListBox):
    def __init__(self, parent=None):
        DialectListBox.__init__(self, parent)
        self.setLayout(self.dialects_list_vbox)