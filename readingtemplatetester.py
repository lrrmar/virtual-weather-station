from ReadingTemplates import *
from ReadingPhaseManager import ReadingPhaseManager
from data_handling import *
from referencing import *
from pathlib import Path
from netCDF4 import Dataset

if __name__ == '__main__':


    #### 'Forecast' ####

    # Forecast class config

    DataBank.set_base_data_dir('/home/force-woest/woest1300/uk/data/')
    DataBank.set_wrf_domain(2)


    # Forecast reference generation

    wrfin = Dataset(path.join(DataBank._base_data_dir, 
        '2023080312', 'wrfout_d02_2023-08-03_12:00:00'))

    station_csv_path = Path('./')
    filename = 'stations_csv.csv'
    station_storage = Station_storage(station_csv_path, filename, wrfin)


        # Dummy report setup...
    report_reference = ReportReference(True, True)
    report_reference.forecast_issue_time =\
        datetime.strptime('2023-08-03 12:00:00', '%Y-%m-%d %H:%M:%S')
    report_reference.forecast_valid_at =\
        datetime.strptime('2023-08-03 20:00:00', '%Y-%m-%d %H:%M:%S')



    ####  'Report' ####

    # Report class config

    ReadingPhaseManager.set_station_store(station_storage)

    # ReadingPhase

    man = ReadingPhaseManager(report_reference)
    man.open_report_store()
    man.get_reading_templates()
    man.prep_loads()
    man.get_loads()
    man.prep_readings()
    man.get_readings()

    exit()






    all_station_ids = [station.id for station in station_storage]
    report_store = ReportStore(all_station_ids)

    ReadingTemplate.set_report_store(report_store)

    reading_templates = [rhReading]

    print(list(product(station_storage, reading_templates)))



