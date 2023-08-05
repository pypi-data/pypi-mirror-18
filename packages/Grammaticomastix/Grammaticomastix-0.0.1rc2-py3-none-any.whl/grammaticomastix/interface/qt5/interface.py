import grammaticomastix.logger
import sys
LOGGER = grammaticomastix.logger.get_logger(__name__)

#///////////////////////////////////////////////////////////////////////////////
def main_qt5():
    LOGGER.debug("main_qt5()")

    try:
        from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QGridLayout
    except BaseException as exception:
        LOGGER.error("Can't load PyQt5; Python error =%s", exception)
        sys.exit(-1)

    class Form(QWidget):
        def __init__(self, parent=None):
            super(Form, self).__init__(parent)

            nameLabel = QLabel("Name:")
            self.nameLine = QLineEdit()
            self.submitButton = QPushButton("&amp;Submit")

            buttonLayout1 = QVBoxLayout()
            buttonLayout1.addWidget(nameLabel)
            buttonLayout1.addWidget(self.nameLine)
            buttonLayout1.addWidget(self.submitButton)

            self.submitButton.clicked.connect(self.submitContact)

            mainLayout = QGridLayout()
            #mainLayout.addWidget(nameLabel, 0, 0)
            mainLayout.addLayout(buttonLayout1, 0, 1)

            self.setLayout(mainLayout)
            self.setWindowTitle("Hello Qt")

        def submitContact(self):
            name = self.nameLine.text()

            if name == "":
                QMessageBox.information(self, "Empty Field",
                                        "Please enter a name and address.")
                return
            else:
                QMessageBox.information(self, "Success!",
                                        "Hello %s!" % name)
    
    app = QApplication(sys.argv)

    screen = Form()
    screen.show()
    sys.exit(app.exec_())
