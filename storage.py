from referencing import Reports

class EmptyReport:

    atts = {}

    @classmethod
    def configure(cls, report):
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
        for key in EmptyReport.atts:
            setattr(self, key, EmptyReport.atts[key])
        self.station_id = station_id

    def __repr__(self):
        return str(self.__dict__)


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
        self.data = []
        for id in station_ids:
            self.data.append(EmptyReport(id))
    def __getitem__(self, index):
        item = [report for report in self.data if report.station_id == index][0]
        return item

    def store_reading(self, station_id, reading_name, reading_data):
        setattr(self[station_id], reading_name, reading_data)
        
