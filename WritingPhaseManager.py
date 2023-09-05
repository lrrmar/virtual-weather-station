from os import path
from storage import ForecastStore

class WritingPhaseManager:

    forecast_store = None

    @classmethod
    def set_forecast_store(cls, forecast_store: ForecastStore):
        cls.forecast_store = forecast_store

    def __init__(self):

        if WritingPhaseManager.forecast_store == None:
            print("No access to forecast storage")
            raise ValueError

    def print_station_report(self, station_id):
        [print(report) for report 
            in WritingPhaseManager.forecast_store[station_id].to_string_array]

    def write_to_file(self, file_path):

        # Need to change get item or it is not iterable through

        print(len(WritingPhaseManager.forecast_store))
        print(WritingPhaseManager.forecast_store.forecasts[0])

        for i in range(len(WritingPhaseManager.forecast_store)):
            WritingPhaseManager.forecast_store.forecasts[i].to_string_array
