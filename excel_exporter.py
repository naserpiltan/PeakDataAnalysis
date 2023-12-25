import pandas as pd
import openpyxl
import os
class ExcelExporter:
    def __init__(self, excel_dir_path: str):
        self.__excel_dir_path = excel_dir_path
        self.__excel_file_path = self.__excel_dir_path+"/export.xlsx"
        self.__create_excel_dir()

    def write(self, export_columns_dict):
        # data_frame = pd.DataFrame(export_columns_dict)
        # excel_writer = pd.ExcelWriter(self.__excel_file_path)
        # data_frame.to_excel(excel_writer)
        # excel_writer.save()

        with pd.ExcelWriter(self.__excel_file_path) as writer:
            # writing to the 'Employee' sheet
            data_frame = pd.DataFrame(export_columns_dict)
            data_frame.to_excel(writer, sheet_name='Employee', index=False)
        print('DataFrames are written to Excel File successfully.')

    def __create_excel_dir(self):
        if not os.path.exists(self.__excel_dir_path):
            os.mkdir(self.__excel_dir_path)
            print("Excel file directory in : ", self.__excel_dir_path)
        else:
            print("Excel file directory exists already : ", self.__excel_dir_path)




