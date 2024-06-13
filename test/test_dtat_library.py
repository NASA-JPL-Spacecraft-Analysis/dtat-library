import dtat.stacked as dtat

class CSVConnector:
    """Connector object to read data from a file"""

    def __init__(self, file):
        import pandas as pd

        self.__file = file

        self.__data = pd.DataFrame()

        self.refresh_data()

        self.__states = self.__scrape_states()

    def get_file(self):
        """Returns the name of the file this connector reads from"""
        return self.__file

    def get_data(self):
        """Read the data stored by the object"""
        return self.__data

    def refresh_data(self):
        """Refresh the data stored by the object with the latest from the original file"""
        import pandas as pd

        def handle_mixed_time_formats(timestamp):
            """Tries to convert a string with subseconds first,
            if that fails, tries without subseconds,
            and otherwise returns an error if both fail"""
            import datetime
            try:
                return datetime.datetime.strptime(timestamp, "%Y-%jT%H:%M:%S.%f")
            except ValueError:
                return datetime.datetime.strptime(timestamp, "%Y-%jT%H:%M:%S")

        def make_datetime_column(time_data):
            """Returns a transformed column of strings to datetime objects"""
            try:
                return pd.to_datetime(time_data, utc=True, format="%Y-%jT%H:%M:%S.%f")
            except ValueError:
                try:
                    return pd.to_datetime(time_data, utc=True, format="%Y-%jT%H:%M:%S")
                except ValueError:
                    return time_data.apply(handle_mixed_time_formats)

        self.__data = pd.read_csv(self.__file, skipinitialspace=True)

        self.__data["scet"] = make_datetime_column(
            self.__data["scet"]
        )
        
    def __scrape_states(self):
        if "name" not in self.__data.columns:
            return []
        return self.__data.name.unique()
    
    def get_states(self):
        """Returns the names of the states contained in this connector"""
        return self.__states


#load the data
predicted = CSVConnector("docs/sampledata.csv")
fig,c,m,t = dtat.make_stacked_graph(predicted.get_data(), 
            y_vars = [["Sample1"], ["Sample2"]], 
            x_var = "scet", 
            figure_title="new plot", 
            #figure_width=6000,
            figure_height = 1000,
            events={"Sample1": [("2020-001T01:40:50.910", "event1"), ("2020-002T01:40:50.910", "event3")], "predicted": [("2020-001T11:40:50.910", "event2")]}
            )
fig.show()