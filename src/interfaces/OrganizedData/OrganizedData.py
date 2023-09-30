import os 
import fileinput
from datetime import date, timedelta, datetime
import pandas as pd
from numpy import zeros
import json
import pickle


from src.functions.is_valid_file_name import is_valid_file_name
from src.functions.get_log_type_by_file_name import get_log_type_by_file_name
from src.functions.parse_line import parse_line
from src.functions.create_hourly_timeline import create_hourly_timeline
from src.functions.normalize_date_to_isoformat import normalize_date_to_isoformat
from src.constants.indexes import INDEX_LOG_LINE
from src.constants.indexes import INDEX_DATE
from src.constants.indexes import INDEX_USER_ID
from src.constants.indexes import INDEX_CLASS
from src.constants.indexes import INDEX_LEVEL
from src.constants.file_name_log_type_correlations import FILE_NAME_AND_LOG_TYPE_CORRELATIONS

class OrganizedData:  
    """
        Only needs the path to the log files. Everything else is set to empty dictionaries/arrays
    """
    def __init__(self, path): 
        self.set_path_to_logs(path)
        self.set_file_name_indexed_data([])
        self.set_datetime_indexed_data({})
        self.set_raw_indexed_data({})
        self.set_user_indexed_data({})
        self.set_all_summaries({})
        
        
    
    """
        Stores the path to logs
    """
    def set_path_to_logs(self, path):
        self.PATH_TO_LOGS = path
       
    """
        Gets the path to the logs
    """ 
    def get_path_to_logs(self):
        return self.PATH_TO_LOGS
    
    """
        Generates the indexed data based on the log type, example: APP_SERVER
    """
    def index_data_by_log_type(self, log_type):
        return_status = True
        path = self.PATH_TO_LOGS
        files_names_of_selected_log_type = self.get_list_of_files_in_path_by_log_type(log_type)
        file_name_indexes = self.get_file_name_indexed_data()
        raw_indexed_data = self.get_raw_indexed_data()
        datetime_indexes = self.get_datetime_indexed_data()
        user_indexes = self.get_user_indexed_data()
        
        for file_name in files_names_of_selected_log_type:  
            if file_name not in file_name_indexes:
                file_name_indexes.append(file_name) 
                
            count = 0  

                
            raw_indexed_data[log_type] = {}
                
            raw_indexed_data[log_type][file_name] = [] 
                
            for lines in fileinput.input([f'{path}//{file_name}']):
                count = count + 1 
                line_temp  = parse_line(lines)
                
                if line_temp['is_valid']:
                    line_temp['parsed_line'][INDEX_LOG_LINE] = count 
                    raw_indexed_data[log_type][file_name].append(line_temp['parsed_line'])   
    
    
        self.set_raw_indexed_data(raw_indexed_data)
        #Indexing Users and Creation Date of the organized data 
        
        datetime_indexes[log_type] = {}
                
        for file_name in raw_indexed_data[log_type]:  
            if len(datetime_indexes[log_type]) > 0:
                for i in range(0, len(datetime_indexes[log_type])):
                    if raw_indexed_data[log_type][file_name][0][INDEX_DATE] < raw_indexed_data[log_type][datetime_indexes[log_type][i]][0][INDEX_DATE]:
                        datetime_indexes[log_type].insert(i, file_name)
                        break
            else:
                datetime_indexes[log_type] = []
                datetime_indexes[log_type].append(file_name)
                
            for index, line in enumerate(raw_indexed_data[log_type][file_name]):  
                if line[INDEX_USER_ID] not in user_indexes:
                    user_indexes[line[INDEX_USER_ID]]  = {}
                if file_name not in user_indexes[line[INDEX_USER_ID]]:
                    user_indexes[line[INDEX_USER_ID]][file_name] = []
                
                user_indexes[line[INDEX_USER_ID]][file_name].append(index)
            
        self.set_user_indexed_data(user_indexes)
        self.set_datetime_indexed_data(datetime_indexes) 
        self.build_summaries_by_log_type(log_type)
    
        return return_status
    
    """
        Gets the list of files for certain type of log type in the path.
        The path is set upon initiation of the object. 
        To decide the type of log, it uses constants to compare to the 
        log file name, example: 'ApplicationServer' for APP_SERVER logs
    """
    def get_list_of_files_in_path_by_log_type(self, log_type):
        list_of_files = []
        path = self.PATH_TO_LOGS
        string_in_file_name = '!-NOTHING-!'
        
        for file_name_in_dictionary in  FILE_NAME_AND_LOG_TYPE_CORRELATIONS:
                if FILE_NAME_AND_LOG_TYPE_CORRELATIONS[file_name_in_dictionary] == log_type:
                    string_in_file_name = file_name_in_dictionary
                    break
        
        for file_name_in_drive in os.listdir(path):
            if string_in_file_name in file_name_in_drive:
                list_of_files.append(file_name_in_drive)
                
        return list_of_files
    
    """
        Summaries are counts of different aspects of the logs,
        like how many times a class was found in the logs
    """
    def build_summaries_by_log_type(self, log_type):
        indexed_data = self.get_raw_indexed_data()
        class_summary = {}
        log_level_summary = {}

        if indexed_data and indexed_data[log_type]:
            for file_name in indexed_data[log_type]:
                for line in indexed_data[log_type][file_name]:
                    if line[INDEX_CLASS] in class_summary:
                        class_summary[line[INDEX_CLASS]] += 1
                    else:
                        class_summary[line[INDEX_CLASS]] = 1
                        
                    if line[INDEX_LEVEL] in log_level_summary:
                        log_level_summary[line[INDEX_LEVEL]] += 1
                    else:
                        log_level_summary[line[INDEX_LEVEL]] = 1
                        
                        
        self.set_summaries(log_type, 'CLASS', class_summary)
        self.set_summaries(log_type, 'LOG_LEVEL', log_level_summary)
        #print(self.get_summaries(log_type, 'LOG_LEVEL'))
        return True
    
    """
        Inits all summaries to whatever value is passed to
    """
    def set_all_summaries(self, summaries):
        self.summaries = summaries
    
    """
        Gets all summaries
    """
    def get_all_summaries(self):
        return self.summaries

    """
        Sets the summary by:
        1 - log_type: The log type the summary will be part of. Example: APP_SERVER, RX, etc
        2 - summary_type: The type of summary, example: CLASS, LOG_LEVEL, etc.
    """
    def set_summaries(self, log_type, summary_type, summaries): 
        if self.summaries.get(log_type) == None:
            self.summaries[log_type] = {}
        self.summaries[log_type][summary_type] = summaries
    
    """
        Gets the summary by:
        1 - log_type: The log type the summary will be part of. Example: APP_SERVER, RX, etc
        2 - summary_type: The type of summary, example: CLASS, LOG_LEVEL, etc.
    """
    def get_summaries(self, log_type, summary_type):
        if self.summaries.get(log_type) == None or self.summaries[log_type].get(summary_type) == None:
            return {}
        else:
            return self.summaries[log_type][summary_type]
    
    """
        The following methods are general getters and setters so we do not
        modify or access data directly from other methods
    """
    def set_raw_indexed_data(self, raw_indexed_data):
        self.raw_indexed_data = raw_indexed_data
    
    def get_raw_indexed_data(self):
        return self.raw_indexed_data
    
    def set_datetime_indexed_data(self, date_indexed_data):
        self.date_indexed_data = date_indexed_data
        
    def get_datetime_indexed_data(self):
        return self.date_indexed_data
    
    def set_file_name_indexed_data(self, file_name_indexes):
        self.file_name_indexes = file_name_indexes
        
    def get_file_name_indexed_data(self):
        return self.file_name_indexes
    
    def set_user_indexed_data(self, user_indexes):
        self.user_indexes = user_indexes
    
    def get_user_indexed_data(self):
        return self.user_indexes
    
    """
        Gets all user Ids that were stored during the indexing step
    """
    def get_all_user_ids(self):
        user_ids = []
        for user in self.get_user_indexed_data():
            user_ids.append(user)
        return user_ids
    
    """
        Return the start and end date by log type, it checks the start and end line
        of each log file to determine what's the start and end date. Useful to graph data
    """
    def get_logs_start_end_date(self, log_type): 
        date_indexed_data = self.get_datetime_indexed_data()
        print(self.date_indexed_data)
        if date_indexed_data and date_indexed_data[log_type] > 0:
            start_file = date_indexed_data[log_type][0]
            end_file = date_indexed_data[log_type][-1:][0] 
            
            start_date = self.raw_indexed_data[log_type][start_file][0]['date']
            end_date = self.raw_indexed_data[log_type][end_file][-1:][0]['date']
            
            return [start_date, end_date]
        else:
            return None
    
    """
        Gets date object passing a string with a date in format '%Y-%m-%d %H:%M:%S'
    """
    def get_datetime_object_from_string(self, str):
        DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
        
        str = str[0: len(str) - 13]
        
        str_obj = datetime.strptime(str , DATETIME_FORMAT)
        
        return str_obj
        
    
    """
        A pandas dataframe is used to graph data using plotly
    """
    def get_pandas_dataframe(self, log_type):
        aux_dates = self.get_logs_start_end_date(log_type)
        start_date = aux_dates[0]
        end_date = aux_dates[1]
        

        dates = create_hourly_timeline(start_date, end_date)
        
        start_date = dates[0]

        columns = {
            'fatal': [], 
            'error': [], 
            'warn': [], 
            'info': [], 
            'perf': [],
            'dbquery': [],
            'debug': [], 
            'trace': []
        }
        
        for log_level in columns:
            columns[log_level] = zeros(len(dates)) 
        
        for file_name in self.raw_indexed_data[log_type]:
            #print(self.raw_indexed_data[log_type][file_name][0])
            for line in self.raw_indexed_data[log_type][file_name]:
                line_date = normalize_date_to_isoformat(line['date'])
                line_level = line['level'].lower()
                #print(f'Line level: {line_level} for date: {line_date} in index: {dates.index(line_date)}')

                columns[line_level][dates.index(line_date)] += 1
                
                #print(columns[line_level][dates.index(line_date)])
        # Iterate over start date until > so we collect all dates and get their
        # ISO representation in a array of Strings
        # while start_date_obj <= end_date_obj:

        #     dates.append(start_date_obj.isoformat())
        #    #print(dates)
            
        #     for file_name in self.date_indexed_data[log_type]: 
        #         for line in self.raw_indexed_data[log_type][file_name]:
        #             a = file_name

        #     start_date_obj += delta
            

        return pd.DataFrame(data=columns,index=dates) 
 
    
    """
        We use the pickle package to write and read dictionaries from a file
    """
    def save_all_data_to_files(self, path_files): 
        with open(path_files + '\\indexed_data.bin', 'wb') as handle:
            pickle.dump(self.get_raw_indexed_data(), handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(path_files + '\\summaries_data.bin', 'wb') as handle:
            pickle.dump(self.get_all_summaries(), handle, protocol=pickle.HIGHEST_PROTOCOL)
            
        with open(path_files + '\\filenames_data.bin', 'wb') as handle:
            pickle.dump(self.get_file_name_indexed_data(), handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(path_files + '\\datetime_data.bin', 'wb') as handle:
            pickle.dump(self.get_datetime_indexed_data(), handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(path_files + '\\user_data.bin', 'wb') as handle:
            pickle.dump(self.get_user_indexed_data(), handle, protocol=pickle.HIGHEST_PROTOCOL)
            
    def load_all_data_from_file(self, file_path):
        path_to_indexed_data = file_path + '/indexed_data.bin'
        path_to_summaries = file_path + '/summaries.bin'
        
        
        print(path_to_indexed_data)
        print(path_to_summaries)
        with open(path_to_indexed_data, 'rb') as handle:
            self.set_raw_indexed_data(pickle.load(handle))
        with open(path_to_summaries, 'rb') as handle:
            self.set_all_summaries(pickle.load(handle))
            
        with open(file_path + '/filenames_data.bin', 'rb') as handle:
            self.set_file_name_indexed_data(pickle.load(handle))
        with open(file_path + '/datetime_data.bin', 'rb') as handle:
            self.set_datetime_indexed_data(pickle.load(handle))
        with open(file_path + '/user_data.bin', 'rb') as handle:
            self.set_user_indexed_data(pickle.load(handle))