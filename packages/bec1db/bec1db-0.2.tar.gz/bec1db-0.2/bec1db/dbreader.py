import os
import re
import time
import shutil
import pandas as pd
import hackyorm as horm
import pathmaker as pm
import snippetreader as snip

## Define a local location to store the database
def localloc():
    # Get user home directory
    basepath = os.path.expanduser('~')
    # Find out the os
    from sys import platform as _platform
    # Platform dependent storage
    if _platform == 'darwin':
        # Mac OS X
        localpath = os.path.join(basepath, 'Documents', 'My Programs', 'Database')
    elif _platform == 'win32' or _platform == 'cygwin':
        # Windows
        localpath = os.path.join(basepath, 'Documents', 'My Programs', 'Database')
    else:
        # Unknown platform
        return None
    # If the folder doesn't exist, create it
    if not (os.path.exists(localpath)): os.makedirs(localpath)
    return localpath


# Clean the parameters
def clean_params(params):
    paramsout = ['exp_'+re.sub('-| |=|\+|\.','', param) for param in params]
    paramsout = [str.strip(param).lower() for param in paramsout]
    return paramsout

# The database api class
class Tullia:
    def __init__(self):
        self.refresh()

    def refresh(self):
        ## Get the original database directory
        databasepath = pm.pathmake(main_folder='Processed Data', sub_folder='Database')
        self.databasepath = os.path.join(databasepath,'Zeus.db')
        ## Download the database
        shutil.copy(self.databasepath, localloc())
        self.localdbpath = os.path.join(localloc(),'Zeus.db')

    def image_query(self,imagesin,paramsin):
        # Clean the image names and parameter names
        images = [image[0:19] for image in imagesin]
        params = clean_params(paramsin)
        zeus = horm.Zeus(self.localdbpath)

        # Convert the time strings to datetimes
        try:
            image_times = [snip.timestr_to_datetime(image) for image in images]
        except ValueError:
            print('Some of the image names are not valid')
            raise
            return None


        # Make a new dataframe
        df = pd.DataFrame(columns=['imagename']+paramsin)

        # Get the parameters
        for image_time in image_times:
            sql = '''SELECT snippet_time,{columns} FROM data
                        WHERE unixtime between {unixtime_range}'''
            cols = ', '.join(params)
            unixtime_0 = snip.unix_time(image_time)
            unixtimes = str(unixtime_0 -10) + ' AND ' + str(unixtime_0 +10)
            sql_query = sql.format(columns=cols, unixtime_range=unixtimes)
            results = zeus.data_query(sql_query)
            df = df.append(pd.DataFrame(results,columns=['imagename']+paramsin))

        return df
