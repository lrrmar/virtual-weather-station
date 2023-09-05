from referencing import Reports
from referencing import StationReference
from datetime import datetime

class EmptyReport:

    atts = {
            }

    # This is very programatic....
    att_strings = {
        'int': (lambda val: str(val)),
        'int64': (lambda val: str(val)),
        'float': (lambda val: str(val)),
        'float32': (lambda val: str(val)),
        'float64': (lambda val: str(val)),
        'datetime': 
            (lambda val: datetime.strftime(val, '%Y-%m-%d %H:%M:%S')),
        'NoneType': (lambda val: '')
    }


    @classmethod
    def configure(cls, report: Reports):
        for key in report.__dict__:
            value = report.__dict__[key]
            if type(value) != int and value == True:
                cls.atts[key] = 'awaiting value'
            elif type(value) != int and  value == False:
                cls.atts[key] = None
            else:
                cls.atts[key] = value


    def __init__(self, station_id: int):
        if EmptyReport.atts ==  {}:
            print('Config incomplete')
            return
        self.station_id = station_id
        for key in EmptyReport.atts:
            setattr(self, key, EmptyReport.atts[key])

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.station_id)

    def __ge__(self, other):
        if self.launch_time >= other.launch_time:
            return True
        elif self.launch_time == other.launch_time\
            and self.forecast_time >= other.forecast_time:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.launch_time < other.launch_time:
            return True
        elif self.launch_time == other.launch_time\
            and self.forecast_time < other.forecast_time:
            return True
        else:
            return False

    @property
    def complete(self):
        return not any(value == 'awaiting value' for value\
            in self.__dict__)

    @property
    def to_string(self):
        string = ''
        for val in self.__dict__:
            string += EmptyReport.att_strings[
                type(self.__dict__[val]).__name__](self.__dict__[val]) + ','

        return string

class ReportStore:

    # ReportStore will be configured by a given Report that will define
    # the format of all written reports, i.e. a class var
    # ReportStore.reportFormat = EmptyReport(Report). Then it will be
    # initialised with a list of station ids, for each of which it will
    # generate an empty report

    @classmethod
    def set_report_format(cls, report: Reports):
        EmptyReport.configure(report)

    def __init__(self, station_ids: list):
        self.reports = []
        for id in station_ids:
            self.reports.append(EmptyReport(id))

    def __getitem__(self, index):
        item = [report for report in self.reports if report.station_id == index][0]
        return item

    def __repr__(self):
        [print(report.station_id) for report in self.reports] 
        print('\n repr done')

    def __str__(self):

        string = 'Reports for stations '
        for report in self.reports:
            string += str(report) + ' ' 
        return string

    def store_reading(self, station_id, reading_name, reading_data):
        #ABSTRACT THIS METHOD TO EMptyReport to do more checks
        setattr(self[station_id], reading_name, reading_data)

    @property
    def complete(self):
        for report in self.reports:
            if not report.complete:
                return False
            else:
                return True

    def dump_reports(self):
        if self.complete:
            return self.reports
        else:
            # Wrong
            return str(self.station_id) + 'Incomplete'
        

class EmptyForecast:

    def __init__(self, station_id: int):
        self.reports = []
        self.station_id = station_id

    def __getitem__(self, index):
        return(sorted(self.reports)[index])

    def __ge__(self, other):
       if self.station_id >= other.station_id:
           return True
       else:
           return False

    def __lt__(self, other):
       if self.station_id < other.station_id:
           return True
       else:
           return False

    def __str__(self):
        return str(self.reports)

    def store_report(self, report: EmptyReport):
        if report.station_id == self.station_id:
            self.reports.append(report)
        else:
            print('Incorrect station id')

    @property
    def to_string_array(self):
        arr = [report.to_string for report in sorted(self.reports)]
        return arr

class ForecastStore:

    def __init__(self, station_reference: StationReference):
        self.forecasts = [EmptyForecast(station_id) for station_id\
            in station_reference.all_ids]

    def __getitem__(self, index):
        item = [forecast for forecast in self.forecasts
            if forecast.station_id == index][0]
        return item

    def __str__(self):
        for forecast in self.forecasts:
            return str(forecast) 

    def __len__(self):
        return len(self.forecasts)

    def store_report(self, report: EmptyReport):
        self[report.station_id].store_report(report)

    def ingest_report_store(self, report_store: ReportStore):
        for report in report_store.dump_reports():
            self.store_report(report)
    
    def forecast_for_station(self, station_id):
        return self[station_id].to_string_array




