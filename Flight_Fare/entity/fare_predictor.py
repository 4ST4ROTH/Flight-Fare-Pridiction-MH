import os
import sys
from Flight_Fare.exception import flight_fare_exception
from Flight_Fare.util.util import load_object
import pandas as pd


class flightData:

    def __init__(self,
                 Airline : str,
                 Source : str,
                 Destination : str,
                 Total_Stops : str,
                 Additional_Info : str,
                 Date_of_Journey : str,
                 Duration : str,
                 Arrival_Time : str,
                 Dep_Time : str,
                 Route : str
                 ):

        try:
            self.Airline = Airline
            self.Source = Source
            self.Destination = Destination
            self.Total_Stops = Total_Stops
            self.Additional_Info = Additional_Info
            self.Date_of_Journey = Date_of_Journey
            self.Duration = Duration
            self.Arrival_Time = Arrival_Time
            self.Dep_Time = Dep_Time
            self.Route = Route
            
        except Exception as e:
            raise flight_fare_exception(e, sys) from e


    def get_fares_input_data_frame(self):
        try:
            fare_input_dict = self.get_fare_data_as_dict()
            return pd.DataFrame(fare_input_dict)

        except Exception as e:
            raise flight_fare_exception(e, sys) from e


    def get_fare_data_as_dict(self):
        try:
            input_data = {
                "Airline": [self.Airline],
                "Source": [self.Source],
                "Destination": [self.Destination],
                "Total_Stops": [self.Total_Stops],
                "Additional_Info": [self.Additional_Info],
                "Date_of_Journey": [self.Date_of_Journey],
                "Duration": [self.Duration],
                "Arrival_Time": [self.Arrival_Time]
                "Dep_Time" : [self.Dep_Time]
                "Route" : [self.Route]
                }

            return input_data

        except Exception as e:
            raise flight_fare_exception(e, sys)


class FarePredictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir

        except Exception as e:
            raise flight_fare_exception(e, sys) from e


    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path

        except Exception as e:
            raise flight_fare_exception(e, sys) from e


    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            expenses = model.predict(X)
            return expenses

        except Exception as e:
            raise flight_fare_exception(e, sys) from e