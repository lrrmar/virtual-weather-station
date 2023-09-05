from netCDF4 import Dataset
from referencing import StationReference, ReportReference
from data_handling import DataBank, datetime_to_wrf_file
from ReadingPhaseManager import ReadingPhaseManager
from WritingPhaseManager import WritingPhaseManager
from storage import ForecastStore

class SetUpManager:

    def __init__(self, wrf_domain: int, base_data_dir: str):
        self.wrf_domain = wrf_domain
        self.base_data_dir = base_data_dir

    def configure_databank(self):
        DataBank.set_wrf_domain(self.wrf_domain)
        DataBank.set_base_data_dir(self.base_data_dir)

    def get_report_reference(
            self, csv_dir: str, csv_file: str, issue_date: str):
        self.report_reference = ReportReference(csv_dir, csv_file, issue_date)

    def get_station_reference(
            self, csv_dir: str, csv_file: str, issue_date: str):
        # Temporary data bank
        data_bank = DataBank(
            forecast_issue_time = self.report_reference[0].launch_time, 
            forecast_valid_time = self.report_reference[0].forecast_time)
        
        # Load wrfout
        wrf_file = Dataset(
            data_bank.wrf_data_dir + '/' + datetime_to_wrf_file(
                self.report_reference[0].forecast_time, self.wrf_domain))

        # Station reference
        self.station_reference = StationReference(
                csv_dir, csv_file, wrf_file)

    def get_forecast_store(self):
        self.forecast_store = ForecastStore(self.station_reference)

    def configure_reading_phase_manager(self):
        ReadingPhaseManager.set_station_reference(self.station_reference)
        ReadingPhaseManager.set_forecast_store(self.forecast_store)

    def configure_writing_phase_manager(self):
        WritingPhaseManager.set_forecast_store(self.forecast_store)
