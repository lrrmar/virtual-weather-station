from referencing import *
from storage import *
from pathlib import Path

if __name__ == '__main__':

    dataset_path = Path('./')
    filename = 'stations_csv.csv'
    wrfin = Dataset('wrfout_d03_2023-06-01_18:00:00')

    station_reference = StationReference(dataset_path, filename, wrfin)
    report_reference = ReportReference('./', 'test_reports.csv', '2023-08-16')

    EmptyReport.configure(report_reference[0])

    report_store = ReportStore(
        [station.id for station in station_reference] )

    print(report_store[:])
