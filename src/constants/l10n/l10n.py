from src.interfaces.utils.dot_notation_dictionary import dot_notation_dict

english_dict = { 
    "MISSING_OUTPUT_FILE": "Command not executed. Missing the directory to save result. Please use command: this_programs_name.exe [commands/args] > [YOUR TARGET FILE]",
    "MULTIPLE_INPUT_ARGS": "There's a -path and a -disc arguments specified. Considering -path over -disc since it has a higher precedence level",
    "SETTING_PATH": "Setting up path for logs to: [{path}]",
    "PATH_SET": "Path to logs successfully set to: [{path}]",
    "PROCESSING_DATA": "Creating indexes and summaries for [{log_type}] logs",
    "DATA_PROCESSING_SUCCESS": "Data for [{log_type}] sucessfully processed",
    "DATA_PROCESSING_ERROR": "An error occurred when creating index and summaries for [{log_types}] logs",
    "UNEXPECTED_ARG": "(ignored index) Unexpected argument in index list: [{arg}]",
    "MISSING_PATH_ARG": "Path to logs not specified. Loading log data from disc",
    "LOADING_FROM_DISC": "(ignored all indexes) Loading pre-processed data. When this happens, no new index or summaries are generated",
    "LOADING_FROM_DISC_SUCESS": "Logs sucessfully loaded from disc",
    "LOADING_FROM_DISC_ERROR": "There was an issue loading logs from disc",
    "MISSING_INPUT_SOURCE": "No -path or -disc arguments could be found. At least one needs to be specified",
    "PLOTTING_DATA": "Generating/Plotting graphics for [{log_type}] logs",
    "PLOTTING_DATA_SUCCESS": "Successfully plotted [{log_type}] data",
    "PLOTTING_DATA_ERROR": "There was a problem plotting the data of [{log_type}] logs",
    "UNRECOGNIZED_LOG_TYPE_ARG": "(ignored) Unrecognized log type to plot in arguments: [{arg}]",
    "SAVE_BACKUPS": "Attempting to save index and summary backups to [{path}]",
    "SAVE_BACKUPS_ERROR": "There was an error while saving the backups",
    "SAVE_BACKUPS_SUCCESS": "Backups sucessfully saved",
    "LOGS_PATH_ARG": "Path for this application's logs found: [{path}]",
    "LOGS_PATH_SET": "Path to save this application's logs set to: [{path}]"
}
 
english = dot_notation_dict(english_dict)