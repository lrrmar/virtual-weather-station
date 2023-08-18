# referencing.py
#   reading of csv and data files

from dataclasses import dataclass, field
import pandas as pd
import numpy as np
from wrf import ll_to_xy
from netCDF4 import Dataset
from datetime import datetime, date, time, timedelta

@dataclass
class Station:
    id: int
    name: str
    latitude: float
    longitude: float
    elevation: int
    xy: list[float]



class StationReference:
    def __init__(self,path,csv_file,wrfin,data = []):
        '''reads this csv file into a pandas
        dataFrame, then will create individual
        instances of Stations above'''
        self.csv_file = csv_file
        self.data = data
        self.path = path
        self.wrfin = wrfin
        #print(self.csv_file)
        #print(dataset_path)
        df = self.read_stations_dataset(self.path,self.csv_file)
        self.make_the_stations(df)
        self.data.sort(key=lambda x: x.id)
        # new by LRRM
        self.all_ids = [station.id for station in self.data]


    def __getitem__(self,index):
        return self.data[index]

    @staticmethod
    def read_stations_dataset(path, filename):
        stations_data = pd.read_csv(path/filename)
        return stations_data

    def make_the_stations(self,df):
        for i in range(df.shape[0]):
            z = ll_to_xy(self.wrfin,df.loc[i, 'latitude'],df.loc[i,'longitude'], as_int=False, meta=False)
            # Check for stations outside of domain
            if (z[0] < self.wrfin.dimensions['west_east'].size
                and z[1] < self.wrfin.dimensions['south_north'].size):
                x = Station(df.loc[i,'StationID'], df.loc[i,'name'],df.loc[i, 'latitude'],df.loc[i,'longitude'],df.loc[i,'elevation'],[z.item(0),z.item(1)])
                self.data.append(x)
        return

#@dataclass
#class Report:
#    station_id: int
#    forecast_issue_time: str = field(default=None, init=False)
#    forecast_valid_time: str = field(default=None, init=False)
#    lead_time: int  = field(default=None, init=False)
#    rh: float or None = field(default=False)
#    ff: float or None = field(default=False)
#
#@dataclas)s
#class ReportReference:
#    forecast_issue_time: str = field(default=None, init=False)
#    forecast_valid_time: str = field(default=None, init=False)
#    lead_time: int  = field(default=None, init=False)
#    rh: bool = field(default=False)
#    ff: bool = field(default=False)
#




@dataclass
class Reports:
    '''instead of an __init__ function
    defines variable name, type, and if needed
    sets a default value for it using the field method'''
    launch_time: datetime
    forecast_time: datetime
    lead_time: int
    tmax: bool = field(default = False)
    tmin: bool = field(default = False)
    ne: bool = field(default = False)
    rrr6: bool = field(default = False)
    rh: bool = field(default = False)
    dd: bool = field(default = False)
    ff: bool = field(default = False)
    vv: bool = field(default = False)
    ww: bool = field(default = False)
    ffg: bool = field(default = False)




class ReportReference:
    def __init__(self,path,csv_file,date,data = []):
        '''reads this csv file into a pandas
        dataFrame, then will create individual
        instances of Stations above'''
        self.csv_file = csv_file
        self.data = data
        self.path = path
        self.date = date
        #calls the method and assings the dataframe to df
        df = self.read_reports_dataset(self.path,self.csv_file)
        #calls the method defined below
        self.make_reports(df)
        '''below sorts the individual instances of
        Reports stored in self.data by firstly their
        issue time then secondly by their valid time if needed'''
        self.data.sort(key=lambda x: (x.launch_time,x.forecast_time))




    @staticmethod
    def read_reports_dataset(path, filename):
        '''doesn't pass self as an argument just
        reads a csv file into a pandas dataframe'''
        reports_data = pd.read_csv(path/filename)
        return reports_data

    def make_reports(self,df):
        #fills all blanks with value False
        df.fillna(False,inplace = True)
        #assigns columns 1,2,3 (zero indexed) to df1
        df1 = df.iloc[:,1:4]
        #replaces the date format string with empty string
        df1.replace('YYYY-mm-dd','',regex = True, inplace = True)
        #inplace means it changes the original rather than duplicates and alters
        #same as df1 but now changes all entries to boolean
        df2 = df.iloc[:,4:].astype('bool')
        #creates date object from self.date argument
        init_date = datetime.strptime(self.date,'%Y-%m-%d')
        #create two empty lists to be used
        f_issue = []
        f_valid = []
        #repeats loop for each row in the dataframe
        for i in range(df1.shape[0]):
            #picks the hour from first column of df1
            add_time = df1.iloc[i,0].split(":")[0]
            #adds this time to init_date for a datetime object
            init_datetime = init_date + timedelta(hours = int(add_time))
            #add this to list 1
            f_issue.append(init_datetime)
            #creates list from 2nd column split by space
            leadtime = df1.iloc[i,1].split(' ')
            #create timedelta variable in hours
            forecast_hour = timedelta(hours = datetime.strptime(leadtime[-1], '%H:%M').hour)
            #check if there is a day to add or not
            if leadtime[0]:
                add_days = timedelta(days = int(leadtime[0]))
            else:
                add_days = timedelta(days = 0)
            #adds init_date ... together to create the new datetime object
            forecast_lead = init_date + add_days + forecast_hour
            f_valid.append(forecast_lead)
            #create an instance of Reports using the defined variables and reading from dataframes
            x = Reports(f_issue[i],f_valid[i],int(df1.iloc[i,2]),df2.iloc[i,0],df2.iloc[i,1],df2.iloc[i,2],df2.iloc[i,3],df2.iloc[i,4],df2.iloc[i,5],df2.iloc[i,6],df2.iloc[i,7],df2.iloc[i,8],df2.iloc[i,9])
            #adds object to the self.data list
            self.data.append(x)
        return

#instead of writing Report_storage.data[i] can just write Report_storage[i]
    def __getitem__(self,index):
        return self.data[index]

