from referencing import Reports

class EmptyReport:

    fields = {}

    @classmethod
    def configure(cls, report):
        for key in report.__dict__:
            value = report.__dict__[key]
            if type(value) != int and value == True:
                cls.fields[key] = 'awaiting value'
            elif type(value) != int and  value == False:
                cls.fields[key] = None
            else:
                cls.fields[key] = value


    def __init__(self, station_id: int):
        if EmptyReport.fields ==  {}:
            print('Config incomplete')
            return
        self.__dict__ = EmptyReport.fields
        self.station_id = station_id

    def __repr__(self):
        return str(self.__dict__)


class ReportStore:

    # ReportStore will be configured by a given Report that will define
    # the format of all written reports, i.e. a class var
    # ReportStore.reportFormat = EmptyReport(Report). Then it will be
    # initialised with a list of station ids, for each of which it will
    # generate an empty report

    _report_format = EmptyReport

    @classmethod
    def set_report_format(cls, report: Reports):
        EmptyReport.configure(report)


    def __init__(self, station_ids: list):
        self.data = [EmptyReport(station_id) for station_id in station_ids]

    def __getitem__(self,index):
        return self.data[index]
