try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

from libs.utils import newIcon, labelValidator

BB = QDialogButtonBox


class LabelDialog(QDialog):

    def __init__(self, text="Enter object label", parent=None, listItem=None):
        super(LabelDialog, self).__init__(parent)

        self.edit = QLineEdit()
        self.edit.setText(text)
        self.edit.setValidator(labelValidator())
        self.edit.editingFinished.connect(self.postProcess)

        model = QStringListModel()
        model.setStringList(listItem)
        completer = QCompleter()
        completer.setModel(model)
        self.edit.setCompleter(completer)

        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon('done'))
        bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        if listItem is not None and len(listItem) > 0:
            self.listWidget = QListWidget(self)
            for item in listItem:
                self.listWidget.addItem(item)
            self.listWidget.itemClicked.connect(self.listItemClick)
            self.listWidget.itemDoubleClicked.connect(self.listItemDoubleClick)
            layout.addWidget(self.listWidget)

        self.setLayout(layout)

    def validate(self):
        try:
            if self.edit.text().trimmed():
                self.accept()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            if self.edit.text().strip():
                self.accept()

    def postProcess(self):
        try:
            self.edit.setText(self.edit.text().trimmed())
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            self.edit.setText(self.edit.text())

    # wzx：修改窗口弹出的位置，只能在软件区域内弹出
    # wzx：修改窗口样式，为Popup，点击外部区域就可以自动关闭
    def popUp(self, text='', move=True):
        self.edit.setText(text)
        self.edit.setSelection(0, len(text))
        self.edit.setFocus(Qt.PopupFocusReason)
        self.setWindowFlags(Qt.Popup)
        self.parent().canvas.hVertex = None # 避免选中了顶点时，点击外部关闭窗口时顶点瞬移
        if move:
            cursor_pos = QCursor.pos()
            parent_bottomRight = self.parentWidget().geometry()
            if (cursor_pos.x() < parent_bottomRight.x()):
                cursor_pos.setX(parent_bottomRight.x())
            if (cursor_pos.y() < parent_bottomRight.y()):
                cursor_pos.setY(parent_bottomRight.y())
            if (cursor_pos.x() + self.sizeHint().width() > parent_bottomRight.x() + parent_bottomRight.width()):
                cursor_pos.setX(parent_bottomRight.x() + parent_bottomRight.width() - self.sizeHint().width())
            if (cursor_pos.y() + self.sizeHint().height() > parent_bottomRight.y() + parent_bottomRight.height()):
                cursor_pos.setY(parent_bottomRight.y() + parent_bottomRight.height() - self.sizeHint().height())
            # max_x = parent_bottomRight.x() + parent_bottomRight.width() - self.sizeHint().width()
            # max_y = parent_bottomRight.y() + parent_bottomRight.height() - self.sizeHint().height()
            # max_global = self.parentWidget().mapToGlobal(QPoint(max_x, max_y))
            # if cursor_pos.x() > max_global.x():
            #     cursor_pos.setX(max_global.x())
            # if cursor_pos.y() > max_global.y():
            #     cursor_pos.setY(max_global.y())
            self.move(cursor_pos)
        return self.edit.text() if self.exec_() else None

    def listItemClick(self, tQListWidgetItem):
        try:
            text = tQListWidgetItem.text().trimmed()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            text = tQListWidgetItem.text().strip()
        self.edit.setText(text)

    def listItemDoubleClick(self, tQListWidgetItem):
        self.listItemClick(tQListWidgetItem)
        self.validate()
