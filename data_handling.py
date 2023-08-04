# data_handling.py
#   Reading model data.

from dataclasses import dataclass, field
import pandas as pd
from wrf import ll_to_xy
from netCDF4 import Dataset
from datetime import date, time, datetime, timedelta
from os import path

class DataBank:

    # Forecast attribute
    _base_data_dir = None
    _wrf_domain = None

    # Report attribute
    _forecast_issue_time = None
    _forecast_valid_at = None

    def __init__(self):


        if _base_data_dir == None:
            print("No  base source for data.")
            raise ValueError

        if _wrf_domain == None:
            print("No  wrf domain prescribed.")
            raise ValueError

        if _forecast_issue_time == None:
            print("No value set for forecast issue time.")
            raise ValueError

        if _forecast_valid_at == None:
            print("No value set for forecast valid at.")
            raise ValueError

    @classmethod
    def set_forecast_issue_time(cls, forecast_issue_time):
        cls._forecast_issue_time = forecast_issue_time

    @classmethod
    def set_forecast_valid_at(cls, forecast_valid_at):
        cls._forecast_valid_at = forecast_valid_at


    def load_data_source(self, name: str, file_type: str, dt: timedelta):

        data_dir = path.join(DataBank._base_data_dir,
            datetime_to_date_dir(DataBank._forecast_issue_time))
        valid_time = DataBank._forecast_valid_at + dt

        if file_type == 'wrfout':
            file_name = datetime_to_wrf_file(valid_time, DataBank._wrf_domain)
            path_to_file = path.join(data_dir, file_name)

        if file_type == 'wrf auxiliary':

        setattr(self, Dataset(path_to_file), name)



def datetime_to_wrf_file(dt: datetime, domain: int):

    if domain <= 0:
        raise ValueError
    domain_str = str(domain)
    if 1 <= domain <= 9:
        domain_str = "0" + domain_str
    filename = "wrfout_d"+ domain_str + "_" + dt.strftime('%Y-%m-%d_%H:%M')

    return filename

def datetime_to_aux_file(dt: datetime):
    pass

def datetime_to_date_dir(dt: datetime):

    dirname = dt.strftime('%Y%m%d%H')

    return dirname

