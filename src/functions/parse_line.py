from ..constants.indexes import *
from ..constants.delimiters import *

# Return a tuple [a, b] where:
# a = sucess of parsing
# b = parsed line
def parse_line(line):  
    parsed_line = {}
    parsed_line['is_valid'] = False
    parsed_line['parsed_line'] = {} 
    
    split_line = line.split(DELIMETER_RAW_LOG_LINE) 
    
    if len(split_line) >= DELIMETER_RAW_LOG_LINE_SPLIT_LENGTH:   
        parsed_line['is_valid'] = True
        
        parsed_line['parsed_line'][INDEX_DATE] = split_line[INDEX_DATE_UNORGANIZED]
        
        parsed_line['parsed_line'][INDEX_LEVEL] = split_line[INDEX_LEVEL_UNORGANIZED]
        
        temp_thread = split_line[INDEX_THREAD_UNORGANIZED] 
        temp_thread = temp_thread.replace('[', '')
        temp_thread = temp_thread.replace(']', '') 
        parsed_line['parsed_line'][INDEX_THREAD] = temp_thread
        
        temp_process_id = split_line[INDEX_PROCESS_ID_UNORGANIZED]
        temp_process_id = temp_process_id.replace('ProcessId:', '') 
        parsed_line['parsed_line'][INDEX_PROCESS_ID] = temp_process_id
        
        temp_parent_id = split_line[INDEX_PARENT_PROCESS_ID_UNORGANIZED]
        temp_parent_id = temp_parent_id.replace('PID:', '') 
        parsed_line['parsed_line'][INDEX_PARENT_PROCESS_ID] = temp_parent_id
        
        temp_user_id = split_line[INDEX_USER_ID_UNORGANIZED]
        temp_user_id = temp_user_id.replace('UID:', '') 
        parsed_line['parsed_line'][INDEX_USER_ID] = temp_user_id
        
        temp_user_session = split_line[INDEX_USER_SESSION_UNORGANIZED]
        temp_user_session = temp_user_session.replace('UserSessionId:', '')  
        parsed_line['parsed_line'][INDEX_USER_SESSION] = temp_user_session.strip()
        
        temp_user_ip = split_line[INDEX_USER_IP_UNORGANIZED]
        temp_user_ip = temp_user_ip.replace('ClientIP:', '')  
        parsed_line['parsed_line'][INDEX_USER_IP] = temp_user_ip.strip()
       
        parsed_line['parsed_line'][INDEX_CLASS] = split_line[INDEX_CLASS_UNORGANIZED]
        
        parsed_line['parsed_line'][INDEX_METHOD] = split_line[INDEX_METHOD_UNORGANIZED]
        
        parsed_line['parsed_line'][INDEX_MESSAGE] = split_line[INDEX_MESSAGE_UNORGANIZED]
        
        parsed_line['parsed_line'][INDEX_LOG_LINE] = 0 

    return parsed_line