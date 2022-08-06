from cmath import e
from Flight_Fare.exception import flight_fare_exception
import Flight_Fare.logger import logging
import sys , os
from Flight_Fare.exception import flight_fare_exception
from Flight_Fare.entity.artifact_entity import DataIngestionArtifact
import numpy as np
import pandas as pd
from six.moves import urllib
from sklearn.model_selection import StratifiedShuffleSplit
from Flight_Fare.entity.config_entity import DataIngestionConfig


class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} Data ingestion log started. {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise flight_fare_exception(e,sys)

    
    def download_data(self,) -> str:
        try:
            #extracting remote url to download dataset
            download_url = self.data_ingestion_config.download_url

            #folder location to download file
            dataset_dir = self.data_ingestion_config.dataset_dir

            os.makedirs(dataset_dir,exist_ok=True)

            fare_file_name = os.path.basename(download_url)

            logging.info(f"Downloading file from [{download_url}] into [{dataset_dir}]")
            urllib.request.urlretrieve(download_url,dataset_dir)
            logging.info(f" file name : [{fare_file_name}] is downlaoded in [{dataset_dir}] folder")
            return dataset_dir

        except Exception as e:
            raise flight_fare_exception(e,sys) from e
    def data_split_train_test(self) -> DataIngestionArtifact:
        try:
            dataset_dir = self.data_ingestion_config.dataset_dir
            file_name = os.listdir(dataset_dir)[0]
            file_path = os.path.join(dataset_dir,file_name)

            logging.info(f"Reading excel file  from [{file_path}]")
            
            flight_data = pd.read_excel(file_path)

            logging.info(f"splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=42)
            
            for train_index,test_index in split.split(flight_data,flight_data['Price']):
                strat_train_set = flight_data.loc[train_index].drop(['Price'],axis=1)
                strat_test_set = flight_data.loc[test_index].drop(['Price'],axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,file_name)

            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training dataset to file : [{train_file_path}]")
                strat_train_set.to_excel(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir , exist_ok=True)
                logging.info(f"Exporting testing dataset to file : [{test_file_path}]")
                strat_test_set.to_excel(test_file_path,index=False)

            
            data_ingestion_artifact = DataIngestionArtifact(train_file_path = train_file_path,
                                                             test_file_path= test_file_path,
                                                             is_ingested=True,
                                                             message= f"Data ingestion completed successfully")
            logging.info(f"data ingestion artifact : [{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise flight_fare_exception(e,sys) from e


    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            dataset_dir = self.download_data()
            return self.data_split_train_test()

        except Exception as e:
            raise flight_fare_exception(e,sys) from e

    def __del__(self):
        logging.info(f"{'>>'*20} Data Ingestion log completed, {'<<'*20}")
        
    