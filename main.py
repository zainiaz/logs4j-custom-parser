# import module
import fileinput
import time
import os
import sys 
import pandas as pd
import json
from dateutil.parser import parse
from numpy import random
 

from src.functions.parse_line import parse_line
from src.functions.is_valid_file_name import is_valid_file_name
from src.interfaces.OrganizedData.OrganizedData import OrganizedData
from src.components.logger.logger import Logger
from src.components.plotter.plotter import Plotter
from src.functions.get_log_type_by_file_name import get_log_type_by_file_name
from src.functions.create_hourly_timeline import create_hourly_timeline
from src.functions.dictionaries_to_json import dictionaries_to_json
from src.constants.indexes import INDEX_LOG_LINE
from src.constants.indexes import INDEX_DATE
from src.constants.indexes import INDEX_USER_ID
from src.constants.l10n.l10n import english as eng




import plotly.graph_objs as go
import numpy as np 
import imgkit
from io import BytesIO


import argparse
 

help = {
    "path": "Path to the logs",
    "index": """Type of logs to index data for. Example:
        [a - App Server logs]
        [r - Root Logs]
        [e - Retriever Logs]
        [d - Dispatcher Logs]""",
    "disc": "Specifies that the data that will be loaded will come from disc. Possible value: true",
    "graph": "If this flag is set, the script will plot the logs",
    "save": "Saves the backups of the data processed in the specified location",
    "logs": "This is the directory where you want to save the logs of this application into. These are NOT the eGain logs folder (or ideally shouldn't been). Default=root directory"
    }

log_types = {
    'a': {
            "name": "Application Server",
            "arg": "APP_SERVER"
    },
    'r': {
        "name": "Root",
        "arg": "ROOT"
    },
    # 'e': {
    #     "name": "Retriever",
    #     "arg": "RX"
    # },
    # 'd': {
    #     "name": "Dispatcher",
    #     "arg": "DX"
    # }
}

parser = argparse.ArgumentParser(description='Description of your program') 
parser.add_argument('-path','--path', help=help['path'])
parser.add_argument('-index','--index', help=help['index']) 
parser.add_argument('-disc','--disc', help=help['disc']) 
parser.add_argument('-save', '--save', help=help['save'])
parser.add_argument('-graph', '--graph', help=help['graph'])
parser.add_argument('-logs', '--logs', help=help['logs'])
args = parser.parse_args()  


all_data = OrganizedData('')
def main():
    # Since we offed the option to change the path for this 
    log_messages_queued = []
    path_to_save_logs = '.'
    if args.logs != None:
        path_to_save_logs = args.logs
    
    logger = Logger('debug', path_to_save_logs) 
     
     
    if sys.stdout.isatty():
        logger.add("error", eng.MISSING_OUTPUT_FILE)
        sys.exit()
    #Check if we are generating a new set of indexed data or loading data from disk
    if args.path != None: # I know this path != None is redundant, I just think it makes it slightly easier to read
        if args.disc != None:
            logger.add("info", eng.MULTIPLE_INPUT_ARGS)
        logger.add('info', eng.SETTING_PATH.format(path=args.path)) 
        
        all_data.set_path_to_logs(args.path)
        
        logger.add('info', eng.PATH_SET.format(path=all_data.get_path_to_logs()))
        
        #choose which logs to index based on the -index argument
        for log_arg in args.index:
            if log_arg in log_types:
                logger.add('info', eng.PROCESSING_DATA.format(log_type=log_types[log_arg]['name']))
                try:
                    all_data.index_data_by_log_type(log_types[log_arg]['arg'])
                    logger.add("info", eng.DATA_PROCESSING_SUCCESS.format(log_type=log_types[log_arg]['name']))
                except:
                    logger.add("error", eng.DATA_PROCESSING_ERROR.format(log_type=log_types[log_arg]['name']))
            else:
                logger.add("error", eng.UNEXPECTED_ARG.format(arg=log_arg))
 
    elif args.disc != None:
        # There was no path specified in the arguments, loading pre-processed data from disc

        logger.add("error", eng.MISSING_PATH_ARG)
        if args.index != None:
            logger.add("info", eng.LOADING_FROM_DISC)
        
        try:
            all_data.load_all_data_from_file(args.disc)
            logger.add("info", eng.LOADING_FROM_DISC_SUCCESS)
        except:
            logger.add("error", eng.LOADING_FROM_DISC_ERROR)
    else:
        logger.add("error", eng.MISSING_INPUT_SOURCE)

    if args.save != None:
        logger.add("info", eng.SAVE_BACKUPS.format(path=args.save))
        try:
            all_data.save_all_data_to_files(args.save)
            logger.add("info", eng.SAVE_BACKUPS_SUCCESS)
        except:
            logger.add("error", eng.SAVE_BACKUPS_ERROR)

    if args.graph != None: 
        plotter = Plotter()
        for log_arg in args.graph:
            if log_arg in log_types:
                logger.add("info", eng.PLOTTING_DATA.format(log_type=log_types[log_arg]['name']))
                
                panda_dataframe = all_data.get_pandas_dataframe(log_types[log_arg]['arg'])
                plot_name = log_types[log_arg]['arg']
                if plotter.plot(panda_dataframe, plot_name):
                    logger.add("info", eng.PLOTTING_DATA_SUCCESS.format(log_type=log_types[log_arg]['arg']))
                else:
                    logger.add("error", eng.PLOTTING_DATA_ERROR.format(log_type=log_types[log_arg]['name']))
            else:
                logger.add("error", eng.UNRECOGNIZED_LOG_TYPE_ARG.format(arg=log_arg))
        
    print(dictionaries_to_json(all_data.get_raw_indexed_data(), all_data.get_all_summaries()))
    
     
if __name__ == '__main__':
    main()


# x = np.random.rand(50)
# y = np.random.rand(50)

# # Define the plot as a dictionary
# fig = go.Figure(data=go.Scatter(x=x, y=y, mode='markers'),
#                 layout=go.Layout(images=[go.layout.Image(
#                                             source='https://www.example.com/image.jpg',
#                                             xref="x",
#                                             yref="y",
#                                             x=0,
#                                             y=1,
#                                             sizex=2,
#                                             sizey=2,
#                                             sizing="stretch",
#                                             opacity=0.5,
#                                             layer="below")]))
# # Add a title to the plot
# fig.update_layout(title='Scatter plot with image background')

# # Show the plot
# fig.write_html('first_figure.html', auto_open=True)
 

 


# # print('Reading Data. Please wait...')
# for file_name in os.listdir(path):  
    
#     if is_valid_file_name(file_name) : 
#         if file_name not in file_name_indexes:
#             file_name_indexes.append(file_name) 
        
#         count = 0  
#         log_type = get_log_type_by_file_name(file_name)
#         organized_data[log_type][file_name] = [] 
        
#         for lines in fileinput.input([f'{path}//{file_name}']):
#             count = count + 1 
#             line_temp  = parse_line(lines)
            
#             if line_temp['is_valid']:
#                 line_temp['parsed_line'][INDEX_LOG_LINE] = count 
#                 organized_data[log_type][file_name].append(line_temp['parsed_line'])   
                
#         # end = time.time()
        
#         # total_time += (end-start)
#         # total_count += count 
        
#         #print(f"--- Execution time [{file_name}]: {end-start}") 
     
   
# #print(f"Total Execution time: {total_time}") 


# temp = []
# all = all_data.get_raw_indexed_data()

# for type in all:
#     for file in all[type]:
#         for line in all[type][file]:
#             temp.append(line)


# df = pd.json_normalize(temp)

# print(df)

# df['parsed_date'] = [x[0:(len(x)-9)] for x in df['date']]

# df['date2'] = [parse(date).date() for date in df['parsed_date']]
# df['day'] = pd.to_datetime(df['date2']).dt.to_period('D')

# by_day = pd.to_datetime(df['date2']).dt.to_period('D').value_counts().sort_index()
# by_day.index = pd.PeriodIndex(by_day.index)
# df_day = by_day.rename_axis('month').reset_index(name='counts') 

# fig = go.Figure(data=go.Scatter(x=df_day['day'].astype(dtype=str), 
#                         y=df_day['counts'],
#                         marker_color='indianred', text="counts"))
# fig.update_layout({"title": 'Tweets about Malioboro from Jan 2020 to Jan 2021',
#                    "xaxis": {"title":"Months"},
#                    "yaxis": {"title":"Total tweets"},
#                    "showlegend": False})
# fig.write_image("by-month.png",format="png", width=1000, height=600, scale=3)
# fig.show()

 #print(all_data.get_raw_indexed_data())
# all_data.set_file_name_indexed_data(file_name_indexes)
#print(all_data.get_file_name_indexed_data())


# print('Indexing Creation Date of the organized data. Please wait')

# for log_type in all_data.get_all_data(): 
#     for file_name in all_data.get_all_data()[log_type]: 
#         if len(date_indexes[log_type]) > 0:
#             for i in range(0, len(date_indexes[log_type])):
#                 if all_data.get_all_data()[log_type][file_name][0][INDEX_DATE] < all_data.get_all_data()[log_type][date_indexes[log_type][i]][0][INDEX_DATE]:
#                     date_indexes[log_type].insert(i, file_name)
#                     break
#         else:
#             date_indexes[log_type][file_name]
            
#         for index, line in enumerate(all_data.get_all_data()[log_type][file_name]):  
#             if line[INDEX_USER_ID] not in users_indexes:
#                 users_indexes[line[INDEX_USER_ID]]  = {}
#             if file_name not in users_indexes[line[INDEX_USER_ID]]:
#                 users_indexes[line[INDEX_USER_ID]][file_name] = []
            
#             users_indexes[line[INDEX_USER_ID]][file_name].append(index)
    
# all_data.set_user_indexed_data(users_indexes)
# all_data.set_date_indexed_data(date_indexes)

# print(all_data.get_date_indexed_data())

# #print(all_data.get_user_indexed_data())
# #print(users_indexes)
# # for log_type in date_indexes:
# #     for log in date_indexes[log_type]:
# #         print(organized_data[log_type][log][0]['date'])

# total_time = time.time()
# #errors = 0
 
# # for log_file in organized_data['APP_SERVER']: 
# #     for line in organized_data['APP_SERVER'][log_file]:
# #         if(line['level'] == 'INFO'):
# #             errors += 1
            
# # print(errors)
# print(f'Size of Organized:{sys.getsizeof(organized_data)}')
# print(f'Size of DIndex:{sys.getsizeof(date_indexes)}')
# print(f'Size of UIndex:{sys.getsizeof(users_indexes)}')
# #print(f'Size of :{}') 
 


#dates = all_data.get_logs_start_date('APP_SERVER')
#date_list = create_hourly_timeline(dates[0], dates[1])


"""
 

def show_in_window(fig):
    import sys, os
    import plotly.offline
    from PyQt5.QtCore import QUrl
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from PyQt5.QtWidgets import QApplication
    
    plotly.offline.plot(fig, filename='name.html', auto_open=False)
    
    app = QApplication(sys.argv)
    web = QWebEngineView()
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "name.html"))
    web.load(QUrl.fromLocalFile(file_path))
    web.show()
    sys.exit(app.exec_())


 
#dates = all_data.get_pandas_dataframe('APP_SERVER')
#print(dates)

#df = px.data.gapminder().query("country=='Canada'")

rows = [
    '2023-01-18T16:48:00', 
    '2023-01-18T16:49:00', 
    '2023-01-18T16:50:00', 
    '2023-01-18T16:51:00', 
    '2023-01-18T16:52:00', 
    '2023-01-18T16:53:00', 
    '2023-01-18T16:54:00', 
    '2023-01-18T16:55:00', 
    '2023-01-18T16:56:00', 
    '2023-01-18T16:57:00', 
    '2023-01-18T16:58:00', 
    '2023-01-18T16:59:00', 
]

columns = {'fatal': [], 
           'error': [], 
           'warn': [], 
           'info': [], 
           'debug': [], 
           'trace': []
           }


for col in columns:
    columns[col]  = random.randint(100, size=len(rows))


#def onclick_func(trace, points, selectos)


#print(columns)
#df = pd.DataFrame(data=columns,index=rows) 

all_data.index_data_by_log_type('APP_SERVER') 


# ---------------------------------
df = all_data.get_pandas_dataframe('APP_SERVER')
#print(df)
fig = px.line(df)
fig.update_layout({"title": 'Logs',
                   "xaxis": {"title":"Dates"},
                   "yaxis": {"title":"Frequencies"},
                   "showlegend": True})
 
fig.write_html("app_server.html")


all_data.index_data_by_log_type('ROOT') 
df = all_data.get_pandas_dataframe('ROOT')
fig = px.line(df)
fig.update_layout({"title": 'Logs',
                   "xaxis": {"title":"Dates"},
                   "yaxis": {"title":"Frequencies"},
                   "showlegend": True})
 
fig.write_html("root.html")


all_data.index_data_by_log_type('RX') 
df = all_data.get_pandas_dataframe('RX')
fig = px.line(df)
fig.update_layout({"title": 'Logs',
                   "xaxis": {"title":"Dates"},
                   "yaxis": {"title":"Frequencies"},
                   "showlegend": True})
 
fig.write_html("rx.html")

# df = all_data.get_pandas_dataframe('PROCESS_LAUNCHER')
# fig = px.line(df)
# fig.update_layout({"title": 'Logs',
#                    "xaxis": {"title":"Dates"},
#                    "yaxis": {"title":"Frequencies"},
#                    "showlegend": True})
 
# fig.write_html("process_launcher.html")

#-------------------
# fig.add_scatter(x=date_list, y=np.random.rand(100), mode='markers',
#                 marker={'size': 30, 'color': np.random.rand(100), 'opacity': 0.6, 
#                         'colorscale': 'Viridis'})

#fig = go.Figure()
# fig.add_scatter(test1, x="Dates", y="Log Level")
#print(all_data.get_pandas_dataframe('APP_SERVER')) 
#show_in_window(fig)
# all_data.save_all_data_to_file()

# all_data = None

# all_data = OrganizedData(path)

# all_data.load_all_data_from_file()

# print(all_data.get_all_summaries())

"""