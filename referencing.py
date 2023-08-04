# referencing.py
#   reading of csv files and generating their references.

from dataclasses import dataclass, field
import pandas as pd
from wrf import ll_to_xy
from netCDF4 import Dataset

@dataclass
class Station:
    id: int
    name: str
    latitude: float
    longitude: float
    elevation: int
    xy: list[float]



class Station_storage:
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
            z = ll_to_xy(self.wrfin,df.loc[i, 'latitude'],df.loc[i,'longitude'], as_int=False)
            x = Station(df.loc[i,'StationID'], df.loc[i,'name'],df.loc[i, 'latitude'],df.loc[i,'longitude'],df.loc[i,'elevation'],[z.item(0),z.item(1)])
            self.data.append(x)
        return

@dataclass
class Report:
    station_id: int
    forecast_issue_time: str = field(default=None, init=False)
    forecast_valid_time: str = field(default=None, init=False)
    lead_time: int  = field(default=None, init=False)
    rh: float or None = field(default=False)
    ff: float or None = field(default=False)

@dataclass
class ReportReference:
    forecast_issue_time: str = field(default=None, init=False)
    forecast_valid_time: str = field(default=None, init=False)
    lead_time: int  = field(default=None, init=False)
    rh: bool = field(default=False)
    ff: bool = field(default=False)



class ReportStore:

    def __init__(self, ids: list):
        self._data = [Report(id) for id in ids]
