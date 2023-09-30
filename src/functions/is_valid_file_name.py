from ..constants.allowed_extensions import ALLOWED_EXTENSIONS
from ..constants.allowed_file_names import ALLOWED_NAMES

# Return a tuple:
# [a, b] where:
# a = is a valid name
# b = the matched string
def is_valid_file_name(file_name):
    matched_substring = [substring for substring in ALLOWED_NAMES if substring in file_name]
    is_valid = False 
    if file_name.lower().endswith(ALLOWED_EXTENSIONS) and any(matched_substring) and 'connpool' not in file_name:
        is_valid =  True 
 
    return is_valid