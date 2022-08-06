
from Flight_Fare.logger import logging
from Flight_Fare.constant import *
from Flight_Fare.components.data_ingestion import DataIngestion
from Flight_Fare.logger import logging
from Flight_Fare.exception import flight_fare_exception
from Flight_Fare.entity.config_entity import DataValidationConfig
from Flight_Fare.entity.config_entity import DataIngestionConfig
from Flight_Fare.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
import os,sys
import pandas  as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json

from Flight_Fare.util.util import read_yaml_file

class DataValidation:
    

    def __init__(self, data_validation_config:DataValidationConfig,
        data_ingestion_artifact:DataIngestionArtifact,
        data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'>>'*30}Data Valdaition log started.{'<<'*30} \n\n")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise flight_fare_exception(e,sys) from e


    def get_train_and_test_df(self):
        try:
            train_df = pd.read_excel(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_excel(self.data_ingestion_artifact.test_file_path)
            return train_df,test_df
        except Exception as e:
            raise flight_fare_exception(e,sys) from e


    def is_train_test_file_exists(self)->bool:
        try:
            logging.info("Checking if training and test file is available")
            is_train_file_exist = False
            is_test_file_exist = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)

            is_available =  is_train_file_exist and is_test_file_exist

            logging.info(f"Is train and test file exists?-> {is_available}")
            
            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path
                message=f"Training file: {training_file} or Testing file: {testing_file}" \
                    "is not present"
                raise Exception(message)

            return is_available
        except Exception as e:
            raise flight_fare_exception(e,sys) from e

    
    def validate_dataset_schema(self)->bool:
        try:
        
            validation_status = False

            train_df = pd.read_excel(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_excel(self.data_ingestion_artifact.test_file_path)

            #reading column names from schema.yaml file
            dict = read_yaml_file(file_path=os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME))['columns']

            schema_file_columns = []
            for key in dict.keys():
                schema_file_columns.append(key)

            logging.info(f"reading columns names from the schema.yaml file : {schema_file_columns}")

            #checking values of categorical columns in schema.yaml file
            airline_yaml_col_value = sorted(read_yaml_file(file_path=os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME))['domain_value']['Airline'])
            source_yaml_col_value = sorted(read_yaml_file(file_path=os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME))['domain_value']['Source'])
            destination_yaml_col_value = sorted(read_yaml_file(file_path=os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME))['domain_value']['Destination'])
            additional_info_yaml_col_value = sorted(read_yaml_file(file_path=os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME))['domain_value']['Additional_Info'])

            #checking values of categorical columns in train and test files
            airline_val_train_df = sorted(train_df['Airline'].unique())
            airline_val_test_df = sorted(test_df['Airline'].unique())

            source_val_train_df = sorted(train_df['Source'].unique())
            source_val_test_df = sorted(test_df['Source'].unique())

            destination_val_train_df = sorted(train_df['Destination'].unique())
            destination_val_test_df = sorted(test_df['Destination'].unique())

            additional_info_val_train_df = sorted(train_df['Additional_Info'].unique())
            additional_info_val_test_df = sorted(test_df['Additional_Info'].unique())

            #checking if the values in categorical columns match with schema.yaml file
            if airline_val_train_df == airline_val_test_df == airline_yaml_col_value:
                if source_val_test_df == source_val_train_df == source_yaml_col_value:
                    if destination_val_test_df == destination_val_train_df == destination_yaml_col_value:
                        if additional_info_val_test_df == additional_info_val_train_df == additional_info_yaml_col_value:
                            validation_status = True
                            logging.info(f" All categorical columns have same value as schema.yaml file")
            return validation_status

        except Exception as e:
            raise flight_fare_exception(e,sys) from e

    def get_and_save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])

            train_df,test_df = self.get_train_and_test_df()

            profile.calculate(train_df,test_df)

            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_dir
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path,"w") as report_file:
                json.dump(report, report_file, indent=6)
            return report
        except Exception as e:
            raise flight_fare_exception(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df,test_df = self.get_train_and_test_df()
            dashboard.calculate(train_df,test_df)

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)
        except Exception as e:
            raise flight_fare_exception(e,sys) from e

    def is_data_drift_found(self)->bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise flight_fare_exception(e,sys) from e

    def initiate_data_validation(self)->DataValidationArtifact :
        try:
            self.is_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_dir,
                report_file_path=self.data_validation_config.report_file_name,
                report_page_file_path=self.data_validation_config.report_page_file_name,
                is_validated=True,
                message="Data Validation performed successully."
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise flight_fare_exception(e,sys) from e


    def __del__(self):
        logging.info(f"{'>>'*30}Data Valdaition log completed.{'<<'*30} \n\n")
        


