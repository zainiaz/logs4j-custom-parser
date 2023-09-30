# import module
import fileinput
import time
import os
import sys
 

allowed_extensions = (
    '.1', '.2', '.3', '.4', '.5', '.6', '.7', '.8', '.9', '.10',
    '.11', '.12', '.13', '.14', '.15', '.16', '.17', '.18', '.19', '.20',
    '.21', '.22', '.23', '.24', '.25', '.26', '.27', '.28', '.29', '.30',
    '.31', '.32', '.33', '.34', '.35', '.36', '.37', '.38', '.39', '.40',
    '.41', '.42', '.43', '.44', '.45', '.46', '.47', '.48', '.49', '.50',
    '.51', '.52', '.53', '.54', '.55', '.56', '.57', '.58', '.59', '.60',
    '.61', '.62', '.63', '.64', '.65', '.66', '.67', '.68', '.69', '.70',
    '.71', '.72', '.73', '.74', '.75', '.76', '.77', '.78', '.79', '.80',
    '.81', '.82', '.83', '.84', '.85', '.86', '.87', '.88', '.89', '.90',
    '.91', '.92', '.93', '.94', '.95', '.96', '.97', '.98', '.99', '.100',
    'log')



INDEX_DATE = 0
INDEX_LEVEL = 1
INDEX_THREAD = 2
INDEX_PROCESS_ID = 3
INDEX_PARENT_PROCESS_ID = 4
INDEX_USER_ID = 5
INDEX_USER_SESSION = 6
INDEX_USER_IP = 7
INDEX_CLASS = 8
INDEX_METHOD = 9
INDEX_MESSAGE = 10
 
log_names = ['ApplicationServer.log', 'rx']

dictionary_def = {
    'ApplicationServer.log': 'APP_SERVER' ,
    'rx': 'RX'
}

organized_data = {
    'APP_SERVER': {},
    'RX': {}
}

date_indexes = {
    'APP_SERVER': [],
    'RX': []
}

users_indexes = {  }

file_name_indexes = []

 
 
path = './/test'
dir_list = os.listdir(path) 

total_count = 0
total_time =  0 


print('Reading Data. Please wait...')
for file_name in dir_list:
    #matched_substrings = [substring in file_name for substring in log_names]
    matched_substring = [substring for substring in log_names if substring in file_name]
    #print(matched_substrings)
    if file_name.lower().endswith(allowed_extensions) and any(matched_substring) and 'connpool' not in file_name:
        file_index = 0 
        if file_name not in file_name_indexes:
            file_name_indexes.append(file_name)
            file_index = len(file_name_indexes) - 1 
        
        count = 0
        start = time.time()  
        log_type = dictionary_def[matched_substring[0]] 
        organized_data[log_type][file_name] = []
        
        for lines in fileinput.input([f'{path}//{file_name}']):
            count = count + 1
            split_line = lines.split(' <@> ')
            if len(split_line) >= 11: 
                organized_data[log_type][file_name].append({})
                line_index = len(organized_data[log_type][file_name]) - 1
                
                organized_data[log_type][file_name][line_index]['date'] = split_line[INDEX_DATE]
                organized_data[log_type][file_name][line_index]['level'] = split_line[INDEX_LEVEL]
                organized_data[log_type][file_name][line_index]['thread'] = split_line[INDEX_THREAD]
                organized_data[log_type][file_name][line_index]['process'] = split_line[INDEX_PROCESS_ID]
                organized_data[log_type][file_name][line_index]['parentProcess'] = split_line[INDEX_PARENT_PROCESS_ID]
                organized_data[log_type][file_name][line_index]['userId'] = split_line[INDEX_USER_ID]
                organized_data[log_type][file_name][line_index]['userSession'] = split_line[INDEX_USER_SESSION]
                organized_data[log_type][file_name][line_index]['userIp'] = split_line[INDEX_USER_IP]
                organized_data[log_type][file_name][line_index]['class'] = split_line[INDEX_CLASS]
                organized_data[log_type][file_name][line_index]['method'] = split_line[INDEX_METHOD]
                organized_data[log_type][file_name][line_index]['message'] = split_line[INDEX_MESSAGE]
                organized_data[log_type][file_name][line_index]['logLine'] = count
                
                
        end = time.time()
        
        total_time += (end-start)
        total_count += count
        
        #print(f"--- Execution time [{file_name}]: {end-start}") 
        
#print(f"Total Execution time: {total_time}") 

print('Indexing creation dates. Please wait')

for log_type in organized_data:
    for file_name in organized_data[log_type]:
        print(file_name)
        if len(date_indexes[log_type]) > 0:
            for i in range(0, len(date_indexes[log_type])):
                if organized_data[log_type][file_name][0]['date'] < organized_data[log_type][date_indexes[log_type][i]][0]['date']:
                    date_indexes[log_type].insert(i, file_name)
                    break
        else:
            date_indexes[log_type].append(file_name) 
            
        for index, line in enumerate(organized_data[log_type][file_name]):
            if line['userId'] not in users_indexes:
                users_indexes[line['userId']]  = {}
            if file_name not in users_indexes[line['userId']]:
                users_indexes[line['userId']][file_name] = []
            
            users_indexes[line['userId']][file_name].append(index)
    
 
#print(users_indexes)
# for log_type in date_indexes:
#     for log in date_indexes[log_type]:
#         print(organized_data[log_type][log][0]['date'])

total_time = time.time()
#errors = 0
 
# for log_file in organized_data['APP_SERVER']: 
#     for line in organized_data['APP_SERVER'][log_file]:
#         if(line['level'] == 'INFO'):
#             errors += 1
            
# print(errors)
print(f'Size of Organized:{sys.getsizeof(organized_data)}')
print(f'Size of DIndex:{sys.getsizeof(date_indexes)}')
print(f'Size of UIndex:{sys.getsizeof(users_indexes)}')
#print(f'Size of :{}')
print(file_name_indexes)