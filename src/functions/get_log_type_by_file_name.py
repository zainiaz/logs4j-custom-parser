from ..constants.file_name_log_type_correlations import FILE_NAME_AND_LOG_TYPE_CORRELATIONS
from ..constants.allowed_file_names import ALLOWED_NAMES

def get_log_type_by_file_name(file_name):
    matched_substring = [substring for substring in ALLOWED_NAMES if substring in file_name]
    if len(matched_substring) > 0:
        return FILE_NAME_AND_LOG_TYPE_CORRELATIONS[matched_substring[0]]
    else:
        return []