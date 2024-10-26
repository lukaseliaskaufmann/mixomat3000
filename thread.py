from PyQt5 import QtCore

import time

from mfrc522 import SimpleMFRC522
from gpiozero import LED


class Loading_thread(QtCore.QThread):
    """Define a Thread that is capable of reading the RFID card.
    """
    id_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Loading_thread, self).__init__()

    def run(self):
        reader = SimpleMFRC522()
        try:
            while True:
                print("Hold a tag near the reader ...")
                id, _ = reader.read()
                # We sleep a bit just to be sure
                time.sleep(2)
                self.id_signal.emit(str(id))
                return

        except Exception as e:
            # There was an error, we clean the GPIO and send an error
            GPIO.cleanup()
            self.id_signal.emit("Error: {}".format(e))


class Progress_Thread(QtCore.QThread):
    """A thread that implement the process of serving the drink.

    Args:
        time (int): The time taken by the drink to be served
        leds (list[LED]): A list of leds that need to light up.
    """
    progress_signal = QtCore.pyqtSignal(int)

    def __init__(self, time: int, leds: list):
        super(Progress_Thread, self).__init__()
        self.time = time
        self.leds = leds

    def run(self):
        # We light up all the given led
        for led in self.leds:
            led.on()

        # We divide the number of second by 100
        # so we know how much time there's between each percent advancment.
        timing = self.time / 100

        # At the end, we wait for the "quantity" amout of time
        for i in range(101):
            time.sleep(timing)

            # setting value to progress bar
            self.progress_signal.emit(i)

        # We can know turn of all the given led
        for led in self.leds:
            led.off()
