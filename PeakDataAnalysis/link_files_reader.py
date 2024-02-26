import ijson
import pandas as pd
import glob
import pathlib
import os

class LinkFileReader:
    def __init__(self, links_files_folder_path):
        self.__links_files_folder_path = links_files_folder_path
        self.__json_postfix = ".json"
        self.__json_files_list = []
        self.__link_segments_dict = {}

        self.__get_json_files_list()
        self.__read_json_files()

    def __get_json_files_list(self):

        for file in os.listdir(self.__links_files_folder_path):
            if file.endswith(self.__json_postfix):
                file_path = os.path.join(self.__links_files_folder_path, file)
                self.__json_files_list.append(file_path)

    def __read_json_files(self):
        for file_index, file_path in enumerate(self.__json_files_list):
            print("link file path ", file_path, " : ", file_index+1, " / ", len(self.__json_files_list))

            with open(file_path, 'rb') as file:
                root_object = ijson.items(file, '')

                for obj in root_object:
                    routes_list = obj.get('routes')

                    for rout in routes_list:
                        link_id = rout.get('routeName')
                        segments_result = rout.get('segmentResults')

                        self.__link_segments_dict[link_id] = []

                        for segment in segments_result:
                            segment_id = segment.get('segmentId')
                            self.__link_segments_dict[link_id].append(segment_id)

    def get_links_dict(self):
        return self.__link_segments_dict









