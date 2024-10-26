import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import json

from gpiozero import LED
import theme
import widgets
import thread


class Vertical_Tabs(QtWidgets.QWidget):
    """A class implementing vertical tabs.

    Args:
        user_info (tuple[str, float]): A tuple containing all the needed user info.
    """

    def __init__(self, user_info: tuple[str, float], leds: list[LED]) -> None:
        super().__init__()
        (self.user_id,
         self.user_name,
         self.user_points) = user_info

        # The differents tabs
        self.CONTENTS = {
            "HOME": Home(self),
            "1": Tab1(self),
            "2": Tab2(self),
            "3": Tab3(self),
            "4": Tab4(self),
            "EXIT": Exit(),
        }
        font = QtGui.QFont("Arial", 15)

        # We get a list of the current config as a base_list of names for the drinks.
        base_list = self.get_config()

        big_list = []
        # This part will make 6 list, each when starting with a different element,
        # vodka for the 1, Bacardi for the 2, etc etc
        for _ in range(len(base_list)):
            big_list.append(base_list.copy())
            first_elem = base_list.pop(0)
            base_list.append(first_elem)

        # Each pump number as his own Pump attached to it. Each Pump as one of the 6 list generated above.
        self.pin_for_pump = {
            "17": widgets.Pump(big_list[0], "Pumpe 1", font),
            "18": widgets.Pump(big_list[1], "Pumpe 2", font),
            "19": widgets.Pump(big_list[2], "Pumpe 3", font),
            "20": widgets.Pump(big_list[3], "Pumpe 4", font),
            "21": widgets.Pump(big_list[4], "Pumpe 5", font),
            "22": widgets.Pump(big_list[5], "Pumpe 6", font),
        }
        # Match the pump number with his led
        self.pin_for_led = leds

        self.setObjectName("Vertical_Tab")
        self.init_ui()

    def init_ui(self):
        """Initialize the UI
        """
        self.lay = QtWidgets.QHBoxLayout()
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.setSpacing(0)

        tab_bar = Tab_Bar(self, ["HOME", "1", "2", "3", "4", "spacer", "EXIT"])
        tab_bar.setFixedSize(QtCore.QSize(60, 480))

        tab = self.CONTENTS["HOME"]

        self.lay.addWidget(tab_bar)
        self.lay.addWidget(tab)

        self.setLayout(self.lay)

    def change_tab(self, tab):
        """Change the current tab to the given tab.

        Args:
            tab (Tab): A Tab object.
        """
        widget = self.lay.itemAt(1).widget()
        widget.setParent(None)

        self.lay.addWidget(tab)
        self.update()

    def match_item_with_pump_number(self, items: list[str]) -> list[str]:
        """Get the pump number related to the current selected drinks.

        Args:
            items (list[str]): List of string representing the drinks to find. 

        Returns:
            list[str]: A list of string representing the pump number of each drinks. 
        """
        pumps_number = []
        for item in items:
            for key, pump in self.pin_for_pump.items():
                if pump.current_selected_item == item:
                    pumps_number.append(key)
                    break
        return pumps_number

    def save_config(self):
        """Save the current config of the different pumps
        """
        readable_dict = self.pin_for_pump.copy()
        for key, pump in readable_dict.items():
            pump = pump.current_selected_item
            readable_dict[key] = pump
        with open("pump_config.txt", "w", encoding="utf-8") as config:
            json.dump(readable_dict, config, ensure_ascii=False, indent=4)

    def get_config(self) -> list[str]:
        """Get the current config of each pump

        Returns:
            [list[str]: A list of string representing the names of each drinks in order.
        """
        with open("pump_config.txt", "r", encoding="utf-8") as config:
            drinks = json.load(config)
        return list(drinks.values())

    def change_points(self, amount):
        """Change the amount of points of the user and the display of those points.

        Args:
            amount (int | float): The amount of points to add/remove.
        """
        self.user_points += amount
        self.CONTENTS["HOME"].points.setText(str(self.user_points))
        self.CONTENTS["4"].points.setText(str(self.user_points))
        self.save_accepted()

    def save_accepted(self):
        """Check if the given id is in the DB.
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

        clean_accepted = []
        for line in valid_lines:
            if str(self.user_id) in line:
                line[2] = str(self.user_points)

            new = ", ".join(line)+"\n"
            clean_accepted.append(new)

        with open("accepted_id.txt", "w") as file:
            file.writelines(clean_accepted)


class Tab_Bar(QtWidgets.QLabel):
    """An implementation of a Tab Bar.

    Args:
        parent (Vertical_Tabs): A Vertical_Tabs object.
        layout_list (list[str]): A list of string representing the layout of the tab bar.
    """

    def __init__(self, parent: Vertical_Tabs, layout_list: list[str]) -> None:
        super().__init__(parent=parent)
        self.layout_list = layout_list
        self.init_ui()

    def init_ui(self):
        """Initialize the UI
        """
        self.lay = QtWidgets.QVBoxLayout()
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.setSpacing(0)

        self.make_layout()

        self.setLayout(self.lay)

    def make_layout(self):
        """Make the layout of the tab bar.
        """
        for elem in self.layout_list:
            # Here we want a spacer in the layout so we put an empty element
            if elem.lower() == "spacer":
                widget = QtWidgets.QLabel()
            else:
                widget = Tab_Button(self, elem, self.parent().CONTENTS[elem])

            self.lay.addWidget(widget)


class Tab_Button(QtWidgets.QPushButton):
    """A button linking the tab bar to the actual wanted tab.

    Args:
        parent (Tab_Bar): A Tab_Bar object.
        text (str): A string object representing the text to display on the button
        tab_content (Tab): A Tab object (or child).
    """

    def __init__(self, parent: Tab_Bar, text: str, tab_content) -> None:
        super().__init__(parent=parent)
        self.text = text
        self.init_ui()
        self.tab_content = tab_content
        self.clicked.connect(
            lambda: self.parent().parent().change_tab(self.tab_content)
        )

    def init_ui(self):
        """Initialize the UI
        """
        self.setText(self.text)
        self.setFixedSize(QtCore.QSize(60, 60))
        self.setFlat(True)
        self.setStyleSheet(theme.TAB_BUTTON)


class Tab(QtWidgets.QWidget):
    """An abstract class representing a Tab object.
    """

    def __init__(self) -> None:
        super().__init__()


class Home(Tab):
    """The Home tab.

    Args:
        parent (Vertical_Tabs): A Vertical_Tabs object
    """

    def __init__(self, parent: Vertical_Tabs) -> None:
        super().__init__()
        self.par = parent
        self.init_ui()

    def init_ui(self):
        """Initialize the UI
        """
        font = QtGui.QFont("Arial", 35)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = widgets.Centered_label("HOME", font)

        user = widgets.Centered_label("{} {}".format(
            self.par.user_name, self.par.user_id), font)

        self.points = widgets.Centered_label(str(self.par.user_points), font)

        layout.addWidget(title)
        layout.addWidget(user)
        layout.addWidget(self.points)

        self.setLayout(layout)


class Tab1(Tab):
    """The first tab.

    Args:
        parent (Vertical_Tabs): A Vertical_Tabs object
    """

    def __init__(self, parent: Vertical_Tabs) -> None:
        super().__init__()
        self.par = parent
        self.init_ui()

    def init_ui(self):
        """Initialize the UI
        """
        layout = QtWidgets.QGridLayout()

        self.dropdown = widgets.Dropdown()
        self.dropdown.addItems(["Vodka Cola", "Bacardi Cola", "Fanta Korn"])

        self.progress = widgets.ProgressBar()

        self.button = widgets.Button("Start")
        self.button.clicked.connect(self.start)

        layout.addWidget(self.dropdown, 0, 0, 1, 10)
        layout.addWidget(self.progress, 1, 0, 1, 8)
        layout.addWidget(self.button, 1, 8, 1, 2)

        self.setLayout(layout)

    def start(self):
        """Start the process of serving the drink
        """
        # Disable the button so we can't click it before the process is finished
        self.button.setEnabled(False)

        ingredients = {"Bacardi Cola": ["Bacardi", "Coca Cola"],
                       "Fanta Korn": ["Fanta", "Vodka"],
                       "Vodka Cola": ["Vodka", "Coca Cola"]}

        current_mixed = self.dropdown.currentText()
        # The current selected drink
        items = ingredients[current_mixed]
        # Get the pump related to this drink
        pump_number = self.parent().match_item_with_pump_number(items)
        pump_alcohol_number = pump_number[0]
        pump_soft_number = pump_number[1]

        # Match the pumps with their leds
        leds_dict = self.par.pin_for_led
        leds = [leds_dict[pump_alcohol_number], leds_dict[pump_soft_number]]

        # Remove 25 points for the drink
        self.par.change_points(-25)

        # Start serving the drink
        self.thread = thread.Progress_Thread(25, leds)
        self.thread.start()
        self.thread.progress_signal.connect(self.make_progress)
        self.thread.finished.connect(lambda: self.button.setEnabled(True))

    def make_progress(self, percentages: int):
        """Display the progress on the progress bar

        Args:
            percentages (int): The percentage of completion
        """
        self.progress.setValue(percentages)


class Tab2(Tab):
    """The second tab.

    Args:
        parent (Vertical_Tabs): A Vertical_Tabs object
    """

    def __init__(self, parent: Vertical_Tabs) -> None:
        super().__init__()
        self.par = parent
        self.init_ui()

    def init_ui(self):
        """Initialize the UI
        """
        layout = QtWidgets.QGridLayout()

        self.dropdown_alcohol = widgets.Dropdown()
        self.dropdown_alcohol.addItems(["Vodka", "Bacardi", "Lelet"])

        self.dropdown_soft = widgets.Dropdown()
        self.dropdown_soft.addItems(["Coca Cola", "Orange Juice", "Fanta"])

        self.sliders_duo = widgets.Double_Slider(self)

        self.glass = widgets.Drink_Glass()

        self.progress = widgets.ProgressBar()

        self.button = widgets.Button("Start")
        self.button.clicked.connect(self.start)

        layout.addWidget(self.dropdown_alcohol, 0, 0, 1, 5)
        layout.addWidget(self.dropdown_soft, 1, 0, 1, 5)
        layout.addWidget(self.sliders_duo, 2, 0, 4, 5)
        layout.addWidget(self.glass, 1, 6, 4, 3)
        layout.addWidget(self.progress, 6, 0, 1, 8)
        layout.addWidget(self.button, 6, 8, 1, 2)

        self.setLayout(layout)

        self.change_glass()

    def change_glass(self):
        """Change the appearance of the glass based on the amount of drinks
        """
        values = self.sliders_duo.values

        self.glass.change_layout_from_value(values)

    def start(self):
        """Start the process of serving the drink
        """
        # Disable the button so we can't click it before the process is finished
        self.button.setEnabled(False)

        # The current selected drinks
        items = [self.dropdown_alcohol.currentText(
        ), self.dropdown_soft.currentText()]
        # Get the pumps related to those drinks
        pump_number = self.par.match_item_with_pump_number(items)

        pump_alcohol_number = pump_number[0]
        pump_soft_number = pump_number[1]

        # Match the pumps with their leds
        leds_dict = self.par.pin_for_led
        leds = [leds_dict[pump_alcohol_number], leds_dict[pump_soft_number]]

        # The values taken from the 2 sliders
        values = list(self.sliders_duo.values.values())

        # Calculate the point cost based on the values
        points_cost = (values[0]*-1) + ((values[1]/10)*-1)
        self.par.change_points(points_cost)

        # Get the max quantity of the two drinks
        quantity = max(values)

        # Start serving the drinks
        self.thread = thread.Progress_Thread(quantity, leds)
        self.thread.start()
        self.thread.progress_signal.connect(self.make_progress)
        self.thread.finished.connect(lambda: self.button.setEnabled(True))

    def make_progress(self, percentages: int):
        """Display the progress on the progress bar

        Args:
            percentages (int): The percentage of completion
        """
        self.progress.setValue(percentages)


class Tab3(Tab):
    """The third tab.

    Args:
        parent (Vertical_Tabs): A Vertical_Tabs object
    """

    def __init__(self, parent: Vertical_Tabs) -> None:
        super().__init__()
        # I can't simply use setParent here because this widget would be display on
        # all the other tab
        self.par = parent
        self.init_ui()

    def init_ui(self):
        """Initialize the UI
        """
        self.lay = QtWidgets.QGridLayout()

        self.password = widgets.Password()
        self.password.input_field.returnPressed.connect(self.check_password)

        self.lay.addWidget(self.password)

        self.setLayout(self.lay)

    def check_password(self):
        """Check if the inputed password is the same as the correct one. Unlock the tab if it is.
        """
        correct = "1234"
        password = self.password.input_field.text()

        if password == correct:
            self.set_real_layout()
        else:
            self.password.input_field.selectAll()

    def set_real_layout(self):
        """Set the "real" layout of the tab
        """
        self.password.setParent(None)

        self.pumps = widgets.Multiple_Pump(self, self.par.pin_for_pump)

        spacer = QtWidgets.QWidget()

        self.button = widgets.Button("Spuelen")
        self.button.clicked.connect(self.clean)

        self.lay.addWidget(self.pumps, 0, 0, 2, 2)
        self.lay.addWidget(spacer, 2, 0, 1, 1)
        self.lay.addWidget(self.button, 2, 1, 2, 1)

    def clean(self):
        self.button.setEnabled(False)

        # We get all the leds
        leds = list(self.par.pin_for_led.values())

        # Start cleaning the pump
        self.thread = thread.Progress_Thread(10, leds)
        self.thread.start()
        self.thread.finished.connect(lambda: self.button.setEnabled(True))


class Tab4(Tab):
    """The fourth tab.

    Args:
        parent (Vertical_Tabs): A Vertical_Tabs object
    """

    def __init__(self, parent: Vertical_Tabs) -> None:
        super().__init__()
        self.par = parent
        self.init_ui()

    def init_ui(self):
        """Initialize the UI
        """

        self.lay = QtWidgets.QGridLayout()

        self.password = widgets.Password()
        self.password.input_field.returnPressed.connect(self.check_password)

        font = QtGui.QFont("Arial", 35)
        self.points = widgets.Centered_label(str(self.par.user_points), font)

        self.lay.addWidget(self.password)

        self.setLayout(self.lay)

    def check_password(self):
        """Check if the inputed password is the same as the correct one. Unlock the tab if it is.
        """
        correct = "1234"
        password = self.password.input_field.text()

        if password == correct:
            self.set_real_layout()
        else:
            self.password.input_field.selectAll()

    def set_real_layout(self):
        """Set the "real" layout of the tab
        """
        self.password.setParent(None)

        font = QtGui.QFont("Arial", 35)

        title = widgets.Centered_label("RFID POINT", font)

        button = widgets.Button("Punkte ändern")
        button.setFixedSize(QtCore.QSize(600, 60))
        button.clicked.connect(self.recharge_points)

        self.lay.addWidget(title)
        self.lay.addWidget(self.points)
        self.lay.addWidget(button)

    def recharge_points(self):
        """Recharge the user points base on the inputed points
        """
        value, ok = QtWidgets.QInputDialog.getInt(self, 'Recharge Points',
                                                  'How much points do you want:', min=0, max=1000)

        if ok:
            self.par.change_points(value)

    def save_accepted(self):
        """Check if the given id is in the DB.
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

        clean_accepted = []
        for line in valid_lines:
            if str(self.par.user_id) in line:
                line[2] = str(self.par.user_points)
                break
            new = ", ".join(line)+"\n"
            clean_accepted.append(new)

        with open("accepted_id.txt", "w") as file:
            file.writelines(clean_accepted)


class Exit(Tab):
    """The exit tab.

    Args:
        parent (Vertical_Tabs): A Vertical_Tabs object
    """

    def __init__(self) -> None:
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the UI
        """
        font = QtGui.QFont("Arial", 60)
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        question = widgets.Centered_label(
            "Do you really\n want to logout ?", font)

        button = widgets.Button("YES")
        button.setFixedSize(QtCore.QSize(600, 60))
        button.clicked.connect(self.exit)

        layout.addWidget(question)
        layout.addWidget(button)

        self.setLayout(layout)

    def exit(self):
        # Acces the main window set_loading() method
        self.parent().parent().set_loading()
