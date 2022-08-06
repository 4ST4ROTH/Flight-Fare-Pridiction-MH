from cgi import test
from msilib import schema
from tkinter import E
from matplotlib import axis
from sklearn import preprocessing
from sklearn import pipeline
from Flight_Fare.exception import flight_fare_exception
from Flight_Fare.entity.config_entity import DataTransformationConfig
from Flight_Fare.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact , DataIngestionArtifact
from Flight_Fare.logger import logging
import sys, os
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator , TransformerMixin
from sklearn.preprocessing import StandardScaler , OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from Flight_Fare.constant import *
from Flight_Fare.util.util import load_data, read_yaml_file, remove_letter,save_numpy_array_data,save_object


class FeatureGenerator(BaseEstimator,TransformerMixin):

    def __init__(self, total_stops_ix = 1,
                date_of_journey_ix = 2,
                duration_ix=3,
                arrival_time_ix = 4,
                dep_time_ix = 5,
                route_ix = 6,
                airline_ix = 7,
                source_ix = 8,
                destination_ix = 9,
                aditional_info_ix = 10, columns=None):
        """FeatureGenerator initialization"""

        try:
            self.columns = columns
            if self.columns is not None:
                total_stops_ix = self.columns.index(COLUMN_TOTAL_STOPS)
                date_of_journey_ix = self.columns.index(COLUMN_DATE_OF_JOURNEY)
                duration_ix = self.columns.index(COLUMN_DURATION)
                arrival_time_ix = self.columns.index(COLUMN_ARRIVAL_TIME)
                dep_time_ix = self.columns.index(COLUMN_DEP_TIME)
                route_ix = self.columns.index(COLUMN_ROUTE)
                airline_ix = self.columns.index(COLUMN_AIRLINE)
                source_ix = self.columns.index(COLUMN_SOURCE)
                destination_ix = self.columns.index(COLUMN_DESTINATION)
                aditional_info_ix = self.columns.index(COLUMN_ADDITIONAL_INFO)
                

            self.total_stops_ix = total_stops_ix
            self.date_of_journey_ix = date_of_journey_ix
            self.duration_ix = duration_ix
            self.arrival_time_ix = arrival_time_ix
            self.dep_time_ix = dep_time_ix
            self.route_ix = route_ix
            self.airline_ix = airline_ix
            self.source_ix = source_ix
            self.destination_ix = destination_ix
            self.aditional_info_ix = aditional_info_ix



        except Exception as e:
            raise flight_fare_exception(e,sys) from E


    def fit(self, X, y=None):
        return self

    def transform(self,X,y=None):
        try:

            #Transforming the featrures required
            Date = X[COLUMN_DATE_OF_JOURNEY].str.split("/").str[0]
            Month = X[COLUMN_DATE_OF_JOURNEY].str.spli("/").str[1]
            Year = X[COLUMN_DATE_OF_JOURNEY].str.split("/").str[2]
            Departure_Hour = X[COLUMN_DEP_TIME].str.split(":").str[0]
            Departure_Minute = X[COLUMN_DEP_TIME].str.split(":").str[1]

            COLUMN_ARRIVAL_TIME = X[COLUMN_ARRIVAL_TIME].str.split(" ").str[0]
            Arrival_Hour = X[COLUMN_ARRIVAL_TIME].str.split(":").str[0]
            Arrival_Minute = X[COLUMN_ARRIVAL_TIME].str.split(":").str[1]
            
            # feature engineering on Total_stops columns done in mltiplke steps
            Total_stops = X[COLUMN_TOTAL_STOPS].replace(to_replace='non-stop',value=0,inplace=True)
            Total_stops = X[Total_stops].replace(to_replace='2 stops',value=2,inplace=True)
            Total_stops = X[Total_stops].replace(to_replace='1 stop',value=1,inplace=True)
            Total_stops = X[Total_stops].replace(to_replace='3 stops',value=3,inplace=True)
            Total_stops = X[Total_stops].replace(to_replace='4 stops',value=4,inplace=True)

            
            COLUMN_DURATION = X[COLUMN_DURATION].str.split(' ').str[0]
            Duration_Hour = remove_letter(COLUMN_DURATION)

            COLUMN_DURATION = X[COLUMN_DURATION].str.split(' ').str[1]
            Duration_Minute = remove_letter(COLUMN_DURATION)

            #changing the dtype for each generated feature to int:
            features_to_change_dtypes = np.c_[Date,
                                        Month,
                                        Year,
                                        Departure_Hour,
                                        Departure_Minute,
                                        Arrival_Hour,
                                        Arrival_Minute,
                                        Duration_Hour,
                                        Duration_Minute,
                                        Total_stops]
        
            features_to_change_dtypes['Date'].astype(int)
            features_to_change_dtypes['Month'].astype(int)
            features_to_change_dtypes['Year'].astype(int)
            features_to_change_dtypes['Departure_Hour'].astype(int)
            features_to_change_dtypes['Departure_Minute'].astype(int)
            features_to_change_dtypes['Arrival_Hour'].astype(int)
            features_to_change_dtypes['Arrival_Minute'].astype(int)
            features_to_change_dtypes['Duration_Hour'].astype(int)
            features_to_change_dtypes['Duration_Minute'].astype(int)
            features_to_change_dtypes['Total_stops'].astype(int)

            #below are the columns that are useless and need to drop
            X.drop(['Route',COLUMN_DATE_OF_JOURNEY,COLUMN_ARRIVAL_TIME,COLUMN_DEP_TIME,COLUMN_DURATION,COLUMN_TOTAL_STOPS],axis=1,inplace=True)


            generated_features = np.c_[X,features_to_change_dtypes]

            return generated_features

        except Exception as e:
            raise flight_fare_exception(e,sys) from e





class DataTransformation:

    def __init__(self,data_transformation_config: DataTransformationConfig,
                      data_ingestion_artifact: DataIngestionArtifact,
                      data_validation_artifact: DataValidationArtifact):

                    
        try:
            logging.info(f"{'>>'*30} Data Transformation log started. {'<<'*30}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact

        except Exception as e:
            raise flight_fare_exception(e,sys) from e


    def get_data_tranformer_obj(self) -> ColumnTransformer:
        try:
            schema_file_path = self.data_validation_artifact.schema_file_path
            dataset_schema = read_yaml_file(file_path=schema_file_path)

            numerical_columns = dataset_schema[NUMERICAL_COLUMN_KEY]
            categorical_columns = dataset_schema[CATEGORICAL_COLUMN_KEY]

             



            numerical_pipeline = pipeline(steps=[ 
                     ('imputer' , SimpleImputer(strategy="most_frequent")),
                     ("feature_generator" , FeatureGenerator(columns=numerical_columns)),
                     ("Scaler" , StandardScaler())
            ]
            )


            categorical_pipeline = pipeline(steps=[
                ('imputer' , SimpleImputer(strategy="most_frequent")),
                ('one_hot_encoder' , OneHotEncoder()),
                ("saler" , StandardScaler(with_mean=False))
            ]
            )         

            logging.info(f"Numerical columns : {numerical_columns}")
            logging.info(f"Categorical columns : {categorical_columns}")

            preprocessing = ColumnTransformer([
                ('numerical_pipeline', numerical_pipeline , numerical_columns),
                ("categorical_pipeline" , categorical_pipeline , categorical_columns)
            ]
            )

            return preprocessing

        except Exception as e:
            raise flight_fare_exception(e,sys) from e


    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info(f"obtaining preprocessing object")
            preprocessing_obj = self.get_data_tranformer_obj()

            logging.info(f"Obtaining training and test file path")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            schema_file_path = self.data_validation_artifact.schema_file_path

            logging.info(f"Loading training and test data as pandas dataframe")
            train_df = load_data(file_path=train_file_path , schema_file_path=schema_file_path)
            test_df = load_data(file_path=test_file_path,schema_file_path=schema_file_path)
            schema = read_yaml_file(file_path=schema_file_path)
            target_column_name = schema[TARGET_COLUMN_KEY]
            numerical_column_name = schema[NUMERICAL_COLUMN_KEY]
            drop_column_name = schema[DROP_COLUMN_KEY]
            categorical_column_name = schema[CATEGORICAL_COLUMN_KEY]

            logging.info(f"Splitting input and target feature from training and testing dataset")
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis = 1)
            target_feature_train_df = train_df.drop(columns=[numerical_column_name,drop_column_name,categorical_column_name], axis = 1)

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis = 1)
            target_feature_test_df = test_df.drop(columns=[numerical_column_name,drop_column_name,categorical_column_name], axis = 1)

            logging.info(f"Applying preprocessing object on training dataset and testing dataset")
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.fit_transform(input_feature_test_df)

            train__arr = np.c_[input_feature_train_arr , np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr , np.array(target_feature_test_df)]

            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(train_file_path).replace(".xlsx",".npz")
            test_file_name = os.path.basename(test_file_path).replace(".xlsx",".npz")

            transformed_train_file_path = os.path.join(transformed_train_dir,train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir,test_file_name)

            logging.info(f"Saving training and testin array")

            save_numpy_array_data(file_path=transformed_train_file_path,array=train__arr)
            save_numpy_array_data(file_path=transformed_test_file_path,array=test_arr)

            preprocessing_obj_file_path = self.data_transformation_config.preprocessing_dir

            logging.info(f"saving preprocessinf object")
            save_object(file_path=preprocessing_obj_file_path,obj=preprocessing_obj)

            data_transformation_artifact = DataTransformationArtifact(is_transformed=True,
                                               message="Data transformation successful",
                                               transformed_train_file_path=transformed_train_file_path,
                                               transformed_test_file_path=transformed_test_file_path,
                                               preprocessed_object_file_path=preprocessing_obj_file_path)

            logging.info(f"Data transformation artifact : {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise flight_fare_exception(e,sys) from e


    def __del__(self):
        logging.info(f"{'>>'*30} Data Transformation Log completed {'<<'*30}")







