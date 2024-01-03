from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty, QStringListModel,QVariant ,QAbstractListModel,Qt


class Controller(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._label_name = ["Initial Value", "second Value"]
        self._labelNameChanged = pyqtSignal(str)

    # Define a method available to QML

    @pyqtSlot(int,bool)
    def setDaysState(self, index, state):
        print("days_state_list: ", index, " state ", state)
    @pyqtSlot(int,bool)
    def setMonthsState(self, index, state):
        print("months_state_list: ", index, " state ", state)

    @pyqtSlot(int,bool)
    def setDayTimeState(self, index, state):
        print("day_time_state_list: ", index, " state ", state)

    @pyqtSlot(int, bool)
    def setPublicHolidaysState(self, index, state):
        print("public_holidays_state_list: ", index, " state ", state)

    @pyqtSlot(int, bool)
    def setSchoolHolidaysState(self,  index, state):
        print("school_holidays_state_list: ", index, " state ", state)

    @pyqtSlot(int, bool)
    def setFRCState(self, index, state):
        print("frc_state_list: ", index, " state ", state)

    @pyqtSlot(int, bool)
    def setTimeSetState(self, index, state):
        print("time_sets_state_list: ", index, " state ", state)

    @pyqtSlot(int)
    def setClassificationIndex(self, classification_index):
        print("classification_index: ", classification_index)

    @pyqtSlot(int)
    def setSampleSize(self, sample_size):
        print("sample_size: ", sample_size)





    @pyqtProperty(list)
    def labelName(self):
        return self._label_name

    @labelName.setter
    def labelName(self, value):
        if self._label_name != value:
            self._label_name = value
            self._labelNameChanged.emit(value)

