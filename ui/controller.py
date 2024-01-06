from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty, QStringListModel,QVariant ,QAbstractListModel,Qt , QUrl
import json_manager

class Controller(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        init_value = bool(True)
        self._label_name = ["Initial Value", "second Value"]
        self._labelNameChanged = pyqtSignal(str)
        self.__days_indexes = [init_value]*7  # number of days
        self.__months_indexes = [init_value]*12  # number of months
        self.__day_time_indexes = [init_value]*2  # am-pm
        self.__public_holidays_indexes = [False]*9 #number of public holidays
        self.__school_holidays_indexes = [False]*9
        self.__frc_indexes = [init_value]*9

        self.__speed_percentile_time_sets_indexes_am = [init_value] * 20
        self.__speed_percentile_time_sets_indexes_pm = [init_value] * 20
        self.__sample_size_time_sets_indexes_am = [init_value] * 20
        self.__sample_size_time_sets_indexes_pm = [init_value] * 20

        self.__classification_index = 0
        self.__sample_size_value = 0
        self.__speed_percentile_diff_thresh = 0
        self.__sample_size_check_Index = 0
        self.__jsons_folders_path = ""
        self.__jsonManager = None


    # Define a method available to QML

    @pyqtSlot()
    def startExport(self):

        print("Export is being done")
        self.__jsonManager = json_manager.JsonManager(self.__jsons_folders_path)

        self.__jsonManager.set_lists(self.__days_indexes,
                                     self.__months_indexes,
                                     self.__day_time_indexes,
                                     self.__public_holidays_indexes,
                                     self.__school_holidays_indexes,
                                     self.__frc_indexes,
                                     self.__speed_percentile_time_sets_indexes_am,
                                     self.__speed_percentile_time_sets_indexes_pm,
                                     self.__speed_percentile_diff_thresh,
                                     self.__sample_size_time_sets_indexes_am,
                                     self.__sample_size_time_sets_indexes_pm,
                                     self.__sample_size_check_Index,
                                     self.__classification_index,
                                     self.__sample_size_value)
        self.__jsonManager.read_json_files()

    @pyqtSlot(str)
    def setJSONSFolderPath(self, folder_path):
        url = QUrl(folder_path)
        self.__jsons_folders_path = url.toLocalFile()
        print("jsons path ", self.__jsons_folders_path)

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
    def setSpeedPercentileTimeSetStateAM(self, index, state):
        print("setSpeedPercentileTimeSetStateAM: ", index, " state ", state)
        self.__speed_percentile_time_sets_indexes_am[index] = state

    @pyqtSlot(int, bool)
    def setSpeedPercentileTimeSetStatePM(self, index, state):
        print("setSpeedPercentileTimeSetStatePM: ", index, " state ", state)
        self.__speed_percentile_time_sets_indexes_pm[index] = state

    @pyqtSlot(int, bool)
    def setSampleSizeTimeSetStateAM(self, index, state):
        print("setSampleSizeTimeSetStateAM: ", index, " state ", state)
        self.__sample_size_time_sets_indexes_am[index] = state

    @pyqtSlot(int, bool)
    def setSampleSizeTimeSetStatePM(self, index, state):
        print("setSampleSizeTimeSetStatePM: ", index, " state ", state)
        self.__sample_size_time_sets_indexes_pm[index] = state

    @pyqtSlot(int)
    def setClassificationIndex(self, classification_index):
        print("classification_index: ", classification_index)
        self.__classification_index = classification_index

    @pyqtSlot(int)
    def setSampleSizeCheckIndex(self, sample_size_check_Index):
        print("sample_size_check_Index: ", sample_size_check_Index)
        self.__sample_size_check_Index = sample_size_check_Index

    @pyqtSlot(int)
    def setSampleSize(self, sample_size):
        print("sample_size: ", sample_size)
        self.__sample_size_value = sample_size

    @pyqtSlot(int)
    def setSpeedPercentileThreshold(self, speed_percentile):
        print("speed percentile thresh: ", speed_percentile)
        self.__speed_percentile_diff_thresh = speed_percentile

    @pyqtProperty(list)
    def labelName(self):
        return self._label_name

    @labelName.setter
    def labelName(self, value):
        if self._label_name != value:
            self._label_name = value
            self._labelNameChanged.emit(value)

