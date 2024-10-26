import sys
from PyQt5 import QtWidgets, QtGui
import widgets


class Loading(QtWidgets.QWidget):
    """A class that implement a little gif with possible message for the loading screen.
    """

    def __init__(self) -> None:
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the UI
        """
        title_font = QtGui.QFont("Arial", 40)
        message_font = QtGui.QFont("Arial", 20)

        layout = QtWidgets.QGridLayout()

        title = widgets.Centered_label("MIXOMAT 3000", title_font)
        
        exit_button = widgets.Exit_Button("EXIT")
        exit_button.clicked.connect(self.exit_app)

        loading_label = widgets.Centered_label()

        self.error_message = widgets.Centered_label("", message_font)

        message = widgets.Centered_label("RFID login", message_font)

        moviee = QtGui.QMovie('./icons/loading-shake.gif')
        loading_label.setMovie(moviee)
        moviee.start()

        layout.addWidget(title,0,0,1,9)
        layout.addWidget(exit_button,0,9,1,1)
        layout.addWidget(loading_label,1,0,6,10)
        layout.addWidget(self.error_message,7,0,1,10)
        layout.addWidget(message,8,0,1,10)

        self.setLayout(layout)
        
    def exit_app(self):
        sys.exit(0)
