from PyQt5 import QtWidgets, QtGui, QtCore
import theme


class Button(QtWidgets.QPushButton):
    """A class that implement a "standard" button.

    Args:
        text (str): The text that need to be shown on the button.
    """

    def __init__(self, text: str) -> None:
        super().__init__()
        self.setText(text)
        self.setStyleSheet(theme.BUTTON)
        self.setFixedHeight(30)
      
        
class Exit_Button(Button):
    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.setStyleSheet(theme.EXIT_BUTTON)
        self.setFixedHeight(70)


class Slider(QtWidgets.QSlider):
    """A class that implement a "standard" slider.

    Args:
        minimum (int, optional): The minimum value of the slider. Defaults to 0.
        maximum (int, optional): The maximum value of the slider. Defaults to 25.
    """

    def __init__(self, minimum: int = 0, maximum: int = 25) -> None:
        super().__init__()
        self.setStyleSheet(theme.SLIDER)
        self.setMinimum(minimum)
        self.setMaximum(maximum)


class Double_Slider(QtWidgets.QWidget):
    """A class that implement a slider duo with his own logic.

    Args:
        parent (Tab): A Tab object.
    """

    def __init__(self, parent) -> None:
        super().__init__()
        self.par = parent
        self.values = {"sl1": 0, "sl2": 0}
        self.init_ui()

    def init_ui(self):
        """Initialize the UI
        """
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        layout = QtWidgets.QHBoxLayout()

        self.slider1 = Slider()
        self.slider1.setObjectName("sl1")
        self.slider1.valueChanged.connect(self.check_value)

        self.slider2 = Slider()
        self.slider2.setObjectName("sl2")
        self.slider2.valueChanged.connect(self.check_value)

        layout.addWidget(self.slider1)
        layout.addWidget(self.slider2)
        self.setLayout(layout)

    def get_other_value(self, current: str) -> int:
        """Get the value of the other slider based on the name of the current.

        Args:
            current (str): The name of the current slider.

        Returns:
            int: The value of the other slider.
        """
        possibilities = list(self.values.keys())
        # This line is a bit useless but we want to be sure
        possibilities.remove(current)

        other = possibilities[0]

        return self.values[other]

    def check_value(self):
        """Check the value of both sliders and see if they don't conflict.
        """
        slider = self.sender()
        slider_name = slider.objectName()

        # Get the value of both slider
        slider_value = slider.value()
        other_slider_value = self.get_other_value(slider_name)

        maximum_quantity = slider.maximum()

        # If the "total" quantity is <= to the maximum quantity, the current slider can change is value up.
        if (slider_value + other_slider_value) <= maximum_quantity:
            self.values[slider_name] = slider_value
        else:
            # That's not the case, we calculate the maximum achievable value for the current slider based
            # on the maximum quantity and the other slider value
            slider_max = maximum_quantity - other_slider_value
            slider.setValue(slider_max)
        # Update the little glass on the screen
        self.par.change_glass()


class Dropdown(QtWidgets.QComboBox):
    """A class that implement a "standard" dropdown.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet(theme.DROPDOWN)


class ProgressBar(QtWidgets.QProgressBar):
    """A class that implement a "standard" progress bar.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet(theme.PROGRESSBAR)


class Centered_label(QtWidgets.QLabel):
    """A class that implement a "standard" label with is content centered.

    Args:
        text (str, optional): Text that we want to display. Defaults to None.
        font (QtGui.QFont, optional): A possible custom font. Defaults to None.
    """

    def __init__(self, text: str = None, font: QtGui.QFont = None) -> None:
        super().__init__()
        self.setText(text)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        if font is not None:
            self.setFont(font)


class Drink_Glass(QtWidgets.QLabel):
    """A class that implement the little drinking glass for the Tab2.
    """

    def __init__(self) -> None:
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the UI
        """
        self.lay = QtWidgets.QGridLayout()
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.setSpacing(0)

        glass = Centered_label()
        glass.setStyleSheet(theme.GLASS)

        self.soft = Centered_label()
        self.soft.setStyleSheet(theme.SOFT)

        self.alcoholic = Centered_label()
        self.alcoholic.setStyleSheet(theme.ALCOHOLIC)

        self.lay.addWidget(glass, 0, 0, 110, 100)
        self.lay.addWidget(self.soft)
        self.lay.addWidget(self.alcoholic)

        self.setLayout(self.lay)

    def change_layout_from_value(self, values_dict: dict):
        """Change the appearance of the drinking glass based on the quantity.

        Args:
            values_dict (dict): A dict containing info about the quantity.
        """
        sl1 = values_dict["sl1"]
        sl2 = values_dict["sl2"]

        self.soft.setParent(None)
        self.alcoholic.setParent(None)

        alcohol_quantity = sl1 * 4
        soft_quantity = sl2 * 4

        alcohol_start = 100 - alcohol_quantity + 7
        soft_start = 100 - soft_quantity - alcohol_quantity + 7

        self.soft = Centered_label("{} cl".format(sl2))
        # adapt the theme, so we don't see a border radius when it's on top of the alcoholic drink
        if alcohol_quantity > 0:
            self.soft.setStyleSheet(theme.SOFT)
        else:
            self.soft.setStyleSheet(theme.SOFT_ONLY)

        self.alcoholic = Centered_label("{} cl".format(sl1))
        self.alcoholic.setStyleSheet(theme.ALCOHOLIC)

        # The 5 and 90 value are hardcoded to make the display nice.
        if alcohol_quantity > 0:
            self.lay.addWidget(self.alcoholic, alcohol_start,
                               5, alcohol_quantity, 90)
        if soft_quantity > 0:
            self.lay.addWidget(self.soft, soft_start, 5, soft_quantity, 90)


class Pump(QtWidgets.QWidget):
    """An object that implement a single Pump and her logic.

    Args:
        options (list[str]): The option that need to be listed for the pump.
        title (str): The title for this pump.
        font (QtGui.QFont, optional): An optionnal font. Defaults to None.
    """

    def __init__(
        self,
        options: list[str],
        title: str,
        font: QtGui.QFont = None,
    ) -> None:
        super().__init__()
        self.current_selected_item = options[0]
        self.changing = False
        self.init_ui(title, options, font)

    def init_ui(self, title: str, options: list[str], font: QtGui.QFont):
        """Initialize the UI

        Args:
            title (str): The title for this pump.
            options (list[str]): The option that need to be listed for the pump.
            font (QtGui.QFont): An optionnal font.
        """
        lay = QtWidgets.QVBoxLayout()
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)

        title = Centered_label(title, font)

        self.dropdown = Dropdown()
        self.dropdown.addItems(options)
        self.dropdown.currentIndexChanged.connect(self.changing_item)

        lay.addWidget(title)
        lay.addWidget(self.dropdown)

        self.setLayout(lay)

    def change_selected_item(self, item_name: str):
        """Change the selected item to the given "item_name"

        Args:
            item_name (str): The "new" selected item.
        """
        # The variable 'changing' is used as a switch to avoid reccurersion due to the
        # currentIndexChanged signal
        self.changing = True

        self.dropdown.setCurrentText(item_name)
        self.current_selected_item = item_name

        self.changing = False

    def changing_item(self, index: int):
        """Organize the changing of the item.

        Args:
            index (int): The index of the newly selected item
        """
        # This if statement avoid recursion
        if not self.changing:
            wanted_selected_item = self.dropdown.itemText(index)
            # Change the other label
            self.parent().change_other_dropdown(
                self, self.current_selected_item, wanted_selected_item
            )


class Multiple_Pump(QtWidgets.QWidget):
    """A widget tab implement multiple pump with their logic.

    Args:
        parent (Tab): A Tab object.
        pin_for_pump (dict[Pump]): A dict containing the number match with their Pump object.
    """

    def __init__(self, parent, pin_for_pump: dict[Pump]) -> None:
        super().__init__(parent=parent)

        self.pin_for_pump = pin_for_pump
        self.init_ui()

    def init_ui(self):
        """Initialize the UI
        """
        self.lay = QtWidgets.QGridLayout()

        pump1 = self.pin_for_pump["17"]
        pump1.setParent(self)
        pump2 = self.pin_for_pump["18"]
        pump2.setParent(self)
        pump3 = self.pin_for_pump["19"]
        pump3.setParent(self)
        pump4 = self.pin_for_pump["20"]
        pump4.setParent(self)
        pump5 = self.pin_for_pump["21"]
        pump5.setParent(self)
        pump6 = self.pin_for_pump["22"]
        pump6.setParent(self)

        self.lay.addWidget(pump1, 0, 0)
        self.lay.addWidget(pump2, 0, 1)
        self.lay.addWidget(pump3, 1, 0)
        self.lay.addWidget(pump4, 1, 1)
        self.lay.addWidget(pump5, 2, 0)
        self.lay.addWidget(pump6, 2, 1)

        self.setLayout(self.lay)

    def change_other_dropdown(
        self, sender_pump: Pump, current_selected_item: str, wanted_selected_item: str
    ):
        """Change the other dropdown selected item to avoid conflict

        Args:
            sender_pump (Pump): The "sender" Pump.
            current_selected_item (str): The currently selected item of the Pump.
            wanted_selected_item (str): The item we want this Pump to select.
        """

        new_pump = None
        for pump in self.pin_for_pump.values():
            if pump.current_selected_item == wanted_selected_item:
                new_pump = pump
                break

        # The sender pump can now change to the item she wanted
        sender_pump.change_selected_item(wanted_selected_item)
        # The other pump will have the previously selected item from the sender pump
        new_pump.change_selected_item(current_selected_item)

        self.parent().par.save_config()


class Password(QtWidgets.QWidget):
    """A widget that implements a password field
    """

    def __init__(self) -> None:
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the UI
        """
        self.setFixedSize(QtCore.QSize(300, 100))
        font = QtGui.QFont("Arial", 20)

        lay = QtWidgets.QVBoxLayout()

        title = Centered_label("Password", font)

        self.input_field = QtWidgets.QLineEdit()
        self.input_field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.input_field.setStyleSheet(theme.PASSWORD)

        lay.addWidget(title)
        lay.addWidget(self.input_field)

        self.setLayout(lay)
