from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty, QStringListModel,QVariant ,QAbstractListModel,Qt , QUrl
from numpy.ma.core import take
from PyQt6 import QtCore

import json_manager
import threading

class Controller(QObject):
    _labelNameChanged = QtCore.pyqtSignal(str)

    processIsBeingDone = QtCore.pyqtSignal(bool)
    progressValueChanged = QtCore.pyqtSignal(int)
    exportFinished = QtCore.pyqtSignal()
    urlIsEmpty = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        init_value = bool(True)
        self._label_name = ["Initial Value", "second Value"]


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
        self.__process_is_being_done_flag = False
        self.__process_thread = threading.Thread(target=self.__start_processing)


    # Define a method available to QML

    def __start_processing(self):

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
        self.__process_is_being_done_flag = False
        self.exportFinished.emit()

    @pyqtSlot()
    def startExport(self):

        if self.__process_is_being_done_flag:
            print("Process is being done, pleas be patient till it finishes.")
            self.processIsBeingDone.emit(True)
            return

        if len(self.__jsons_folders_path) == 0:
            self.urlIsEmpty.emit()
            return

        print("Export is being done")
        self.processIsBeingDone.emit(False)
        self.__process_is_being_done_flag = True
        self.__jsonManager = json_manager.JsonManager(self.__jsons_folders_path)
        self.__jsonManager.progress_value_changed.connect(self.progressValueChanged)

        self.__process_thread = threading.Thread(target=self.__start_processing)
        self.__process_thread.daemon = True
        self.__process_thread.start()

    # def progress_value_changed(self, val):
    #     self.progressValueChanged.emit(val)

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

