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

    def __init__(self, forecast_issue_time, forecast_valid_time, *args):

        self._forecast_issue_time = forecast_issue_time
        self._forecast_valid_at = forecast_valid_time
        print("iniated DataBank", self._forecast_issue_time)
        print('DataBank args are', args)


        if DataBank._base_data_dir == None:
            print('No  base source for data.')
            raise ValueError

        if DataBank._wrf_domain == None:
            print('No  wrf domain prescribed.')
            raise ValueError

        for arg in args:
            print('This arg is ', arg)
            (attr_name, file_type, dt) = arg
            self.load_data_source(attr_name, file_type, dt)


    @classmethod
    def set_base_data_dir(cls, base_data_dir):
        cls._base_data_dir = base_data_dir

    @classmethod
    def set_wrf_domain(cls, wrf_domain):
        cls._wrf_domain = wrf_domain

    @classmethod
    def set_forecast_issue_time(cls, forecast_issue_time):
        cls._forecast_issue_time = forecast_issue_time

    @classmethod
    def set_forecast_valid_at(cls, forecast_valid_at):
        cls._forecast_valid_at = forecast_valid_at


    def load_data_source(self, attr_name: str, file_type: str, dt: timedelta):

        data_dir = path.join(DataBank._base_data_dir,
            datetime_to_date_dir(self._forecast_issue_time))
        valid_time = self._forecast_valid_at + dt

        if file_type == 'wrfout':
            file_name = datetime_to_wrf_file(valid_time, DataBank._wrf_domain)
            path_to_file = path.join(data_dir, file_name)

        if file_type == 'wrf auxiliary':
<<<<<<< HEAD
            pass

        setattr(self, attr_name, Dataset(path_to_file))
=======
            setattr(self, Dataset(path_to_file), name)
>>>>>>> 1c1082b (A timeley commit...)



def datetime_to_wrf_file(dt: datetime, domain: int):

    if domain <= 0:
        raise ValueError
    domain_str = str(domain)
    if 1 <= domain <= 9:
        domain_str = '0' + domain_str
    filename = 'wrfout_d'+ domain_str + '_' + dt.strftime('%Y-%m-%d_%H:%M:%S')

    return filename

def datetime_to_aux_file(dt: datetime):
    pass

def datetime_to_date_dir(dt: datetime):

    dirname = dt.strftime('%Y%m%d%H')

    return dirname

