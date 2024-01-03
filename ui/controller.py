from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty, QStringListModel,QVariant ,QAbstractListModel,Qt


class Controller(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        init_value = bool(0)
        self._label_name = ["Initial Value", "second Value"]
        self._labelNameChanged = pyqtSignal(str)
        self.__days_indexes = [init_value]*7  # number of days
        self.__months_indexes = [init_value]*12  # number of months
        self.__day_time_indexes = [init_value]*2  # am-pm
        self.__public_holidays_indexes = [init_value]*13 #number of public holidays
        self.__school_holidays_indexes = [init_value]*9
        self.__frc_indexes = [init_value]*10
        self.__time_sets_indexes = [init_value]*20
        self.__classification_index = 0
        self.__sample_size_value = 0

    # Define a method available to QML

    @pyqtSlot(int,bool)
    def setDaysState(self, index, state):
        print("days_state_list: ", index, " state ", state)
        self.__days_indexes[index] = state
    @pyqtSlot(int,bool)
    def setMonthsState(self, index, state):
        print("months_state_list: ", index, " state ", state)
        self.__months_indexes[index] = state

    @pyqtSlot(int,bool)
    def setDayTimeState(self, index, state):
        print("day_time_state_list: ", index, " state ", state)
        self.__day_time_indexes[index] = state
        print("list ",self.__day_time_indexes)

    @pyqtSlot(int, bool)
    def setPublicHolidaysState(self, index, state):
        print("public_holidays_state_list: ", index, " state ", state)
        self.__public_holidays_indexes[index] = state

    @pyqtSlot(int, bool)
    def setSchoolHolidaysState(self,  index, state):
        print("school_holidays_state_list: ", index, " state ", state)
        self.__school_holidays_indexes[index] = state

    @pyqtSlot(int, bool)
    def setFRCState(self, index, state):
        print("frc_state_list: ", index, " state ", state)
        self.__frc_indexes[index] = state

    @pyqtSlot(int, bool)
    def setTimeSetState(self, index, state):
        print("time_sets_state_list: ", index, " state ", state)
        self.__time_sets_indexes[index] = state

    @pyqtSlot(int)
    def setClassificationIndex(self, classification_index):
        print("classification_index: ", classification_index)
        self.__classification_index = classification_index

    @pyqtSlot(int)
    def setSampleSize(self, sample_size):
        print("sample_size: ", sample_size)
        self.__sample_size_value = sample_size

    @pyqtProperty(list)
    def labelName(self):
        return self._label_name

    @labelName.setter
    def labelName(self, value):
        if self._label_name != value:
            self._label_name = value
            self._labelNameChanged.emit(value)

