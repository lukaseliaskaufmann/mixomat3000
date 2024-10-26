from PyQt5 import QtWidgets, QtGui
from gpiozero import LED
import loading
import tabs
import theme
import thread


def check_accepted_id(id: str) -> tuple[bool, str]:
    """Check if the given id is in the DB.

    Args:
        id (str): A string representation of the id.

    Returns:
        tuple[bool, str]: A boolean representation of the succes and the name related to the id.
    """
    with open("accepted_id.txt", "r") as file:
        lines = file.readlines()

    valid_lines = []
    # Clean up the DB in case there're blank lines in it
    for line in lines:
        line = line.replace("\n", "")
        if "," in line:
            line = line.split(",")
            valid_lines.append(line)

    for line in valid_lines:
        if id in line:
            return True, line[1].strip(), float(line[2].strip())

    return False, ""


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

        self.leds = {
            "17": LED(17),
            "18": LED(18),
            "19": LED(19),
            "20": LED(20),
            "21": LED(21),
            "22": LED(22),
        }

    def init_ui(self) -> None:
        """Initialize the UI
        """
        self.setObjectName("main")

        self.showFullScreen()
        self.setStyleSheet(theme.BACKGROUND)
        self.set_loading()

        self.show()

    def read_RFID(self):
        """Launch the thread responsible to read the RFID card
        """
        self.thread = thread.Loading_thread()
        self.thread.start()
        self.thread.id_signal.connect(self.check_id)

    def check_id(self, id: str):
        """Check the given id and unlock the app if needed.

        Args:
            id (str): A string representation of the id.
        """
        valid, name, base_points = check_accepted_id(id)
        if "Error" in id:
            # There was an error while reading the card
            self.loading_screen.error_message.setText(id)
            self.read_RFID()
        elif not valid:
            # The ID is not in the DB
            self.loading_screen.error_message.setText(
                "Error: {} not accepted".format(id))
            self.read_RFID()
        else:
            self.login((id, name, base_points))

    def set_loading(self):
        self.main = loading.Loading()
        self.setCentralWidget(self.main)
        self.read_RFID()

    def login(self, user_info: tuple[str]):
        self.main = tabs.Vertical_Tabs(user_info, self.leds)
        self.setCentralWidget(self.main)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """Redirect the button close event if we are inside the app.
        """
        main_object = self.centralWidget()
        # This means we are inside the app, so we redirect the user to the exit tab.
        if main_object.objectName() == "Vertical_Tab":
            event.ignore()
            main_object.change_tab(main_object.CONTENTS["EXIT"])
        else:
            # We are not in the app so we just close the window
            event.accept()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
