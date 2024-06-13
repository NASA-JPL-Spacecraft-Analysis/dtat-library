import dtat.plot as dtat
from dtat.dataconnectors.csvconnector import CSVConnector


#load the data
predicted = CSVConnector("docs/sampledata.csv")
fig,c,m,t = dtat.make_stacked_graph(predicted.get_data(), 
            y_vars = [["Sample1"], ["Sample2"]], 
            y_axis_units = ["samples", "random samples"],
            x_var = "scet", 
            figure_title="new plot", 
            #figure_width=6000,
            figure_height = 1000,
            events={"Sample1": [("2020-001T01:40:50.910", "event1"), ("2020-002T01:40:50.910", "event3")], "Sample2": [("2020-001T11:40:50.910", "event2")]},
            event_line=True,
            )
fig.show()