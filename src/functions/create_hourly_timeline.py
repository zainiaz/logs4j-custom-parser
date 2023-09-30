from datetime import date, timedelta, datetime

# Function to return a string of dates to use as a X-axis in a graph
def create_hourly_timeline(start_date, end_date):
    DATETIME_FORMAT = '%Y-%m-%d %H:%M'
    
    # create datetime objects witht DATETIME_FORMAT (datetime documentation) 
    start_date_obj = datetime.strptime(start_date[0: len(start_date) - 16] , DATETIME_FORMAT)
    end_date_obj = datetime.strptime(end_date[0: len(end_date) - 16] , DATETIME_FORMAT)
    
    # A delta with days=1 to increase to out initial date to get all dates
    # Check official documentation for more information about this
    delta = timedelta(minutes=1)
    
    dates = []
    
    # Iterate over start date until > so we collect all dates and get their
    # ISO representation in a array of Strings
    while start_date_obj <= end_date_obj:
        
        dates.append(start_date_obj.isoformat())
        
        start_date_obj += delta

    #print(dates)
    return dates