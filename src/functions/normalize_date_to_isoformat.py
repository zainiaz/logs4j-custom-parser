from datetime import date, timedelta, datetime

def normalize_date_to_isoformat(date):
    DATETIME_FORMAT = '%Y-%m-%d %H:%M'
    
    #get rid of the unwanted ' GMT+0000' at the end eGain dates
    clean_date = date[0: len(date) - 16] 
    
    date_obj = datetime.strptime(clean_date , DATETIME_FORMAT)
    
    return date_obj.isoformat()