import pandas as pd
import numpy as np
import datetime
import os
import pytz
import pickle

# Index Levels
def create_df(pickle_data):
    """
    Create a new data frame.
    Args:
        pickle_data : data that have all encodings.
    """

    # If timezone create probleum then create day month year 
    # and pass it to create datetime object
    current_date = datetime.date.today() 
    # getting next month
    # using replace to get to last day + offset
    # to reach next month
    nxt_mnth = current_date.replace(day=28) + datetime.timedelta(days=4)
    # subtracting the days from next month date to
    # get last date of current Month
    res = nxt_mnth - datetime.timedelta(days=nxt_mnth.day)
    
    no_of_days = res.day
    # create two index one is for outer and one is inner index
    outside = list(np.repeat(np.arange(1,no_of_days + 1),2)) # last is not included
    inside = ['Entry', 'Exit'] * no_of_days
    # Pandas MultiIndex
    hier_index = pd.MultiIndex.from_tuples(list(zip(outside,inside)))

    # names =  os.listdir(path)
    # names = ['Gaurav', 'Pradeep', 'Laveen']
    names = list(set(pickle_data['names']))
    names.sort()
    # new data frame, value of index is hier_index and columns is names 
    df_new = pd.DataFrame(None,index= hier_index, columns= names)
    # set index title
    df_new.index.names = ['Date','Status']
    # for changing dtype of the data from float to string
    df_new.loc[1].iloc[1] = 'None'

    return df_new

if __name__ == '__main__':    


    abs_path = "/home/pi/dlib_face/"
    try:
        data = pickle.loads(open(abs_path + "encodings.pickle", "rb").read())
		# unable to load pickle file or attendance file
    except Exception as e:
        print(e)
   
    today_info = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
    # extract name of the month in form of string
    month = today_info.strftime("%B") 
    
    # check that if same file exist or not in a dataframe
    file_csv = abs_path + f'Attendance_{month}.csv'
    isExisting = os.path.exists(file_csv)
    
    # If attendance sheet for that month does not exist than create a new sheet    
    if not isExisting: 
        df = create_df(data)
        df.to_csv(file_csv, index_label = ['Date','Status'])