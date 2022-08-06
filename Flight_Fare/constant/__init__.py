import os
import sys
from datetime import datetime

def get_current_time_stamp():
    return f"{datetime.now().strftime('%y-%m-%d-%H-%M-%S')}"


ROOT_DIR = os.getcwd()
CONFIG_DIR = 'config'
CONFIG_FILE_NAME = 'config.yaml'
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)

CURRENT_TIME_STAMP = get_current_time_stamp()


#training pipeline related variables
TRAINING_PIPELINE_CONFIG_KEY = 'training_pipeline_config'
TRAINING_PIPELINE_ARTIFACT_KEY = 'artifact_dir'
TRAINING_PIPELINE_NAME_KEY = 'pipeline_name'

#data ingestion pipeline related variables
DATA_INGESTION_DOWNLOAD_URL_KEY = 'download_url'
DATA_INGESTION_CONFIG_KEY = 'data_ingestion_config'
DATA_INGESTION_DATASET_DIR_KEY = 'dataset_dir'
DATA_INGESTION_ARTIFACT_DIR = 'data_ingestion'
DATA_INGESTION_DIR_NAME_KEY = 'ingested_dir'
DATA_INGESTION_TRAIN_DIR_KEY = 'ingested_train_dir'
DATA_INGESTION_TEST_DIR_KEY = 'ingested_test_dir'

#data validation pipeline related variables
DATA_VALIDATION_CONFIG_KEY = 'data_validation_config'
DATA_VALIDATION_SCHEMA_DIR_KEY = 'schema_dir'
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY = 'schema_file_name'
DATA_VALIDATION_REPORT_FILE_NAME_KEY = 'report_file_name'
DATA_VALIDATION_REPORT_DIR = 'report_dir'
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY = 'report_page_file_name'
DATA_VALIDATION_ARTIFACT_DIR_KEY = 'data_validation'

#data transformation pipeline related variables
DATA_TRANSFOMATION_CONFIG_KEY = 'data_transformation_config'
DATA_TRANSFORMATION_TRANSFORMD_DIR_KEY = 'transformed_dir'
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY = 'transformed_train_dir'
DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY = 'transformed_test_dir'
DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY = 'preprocessing_dir'
DATA_TRANSFORMATION_PREPROCESSED_OBJECT_FILE_NAME_KEY = 'preprocessed_object_file_name'
DATA_TRANSFORMATION_ARTIFACT_DI_KEY = 'data_transformation'

COLUMN_TOTAL_STOPS = "Total_Stops"
COLUMN_DATE_OF_JOURNEY = "Date_of_Journey"
COLUMN_DURATION = "Duration"
COLUMN_ARRIVAL_TIME = "Arrival_Time"
COLUMN_DEP_TIME = "Dep_Time"
COLUMN_ROUTE = "Route"
COLUMN_AIRLINE = "Airline"
COLUMN_SOURCE = "Source"
COLUMN_DESTINATION = "Destination"
COLUMN_ADDITIONAL_INFO = "Additional_Info"

DATASET_SCHEMA_COLUMNS_KEY=  "columns"

NUMERICAL_COLUMN_KEY="numerical_columns"
CATEGORICAL_COLUMN_KEY = "categorical_columns"
DROP_COLUMN_KEY = "drop_column"



TARGET_COLUMN_KEY="target_column"

# Model Training related variables

MODEL_TRAINER_ARTIFACT_DIR = "model_trainer"
MODEL_TRAINER_CONFIG_KEY = "model_trainer_config"
MODEL_TRAINER_TRAINED_MODEL_DIR_KEY = "trained_model_dir"
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY = "model_file_name"
MODEL_TRAINER_BASE_ACCURACY_KEY = "base_accuracy"
MODEL_TRAINER_MODEL_CONFIG_DIR_KEY = "model_config_dir"
MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY = "model_config_file_name"


MODEL_EVALUATION_CONFIG_KEY = "model_evaluation_config"
MODEL_EVALUATION_FILE_NAME_KEY = "model_evaluation_file_name"
MODEL_EVALUATION_ARTIFACT_DIR = "model_evaluation"
# Model Pusher config key
MODEL_PUSHER_CONFIG_KEY = "model_pusher_config"
MODEL_PUSHER_MODEL_EXPORT_DIR_KEY = "model_export_dir"

BEST_MODEL_KEY = "best_model"
HISTORY_KEY = "history"
MODEL_PATH_KEY = "model_path"

EXPERIMENT_DIR_NAME="experiment"
EXPERIMENT_FILE_NAME="experiment.csv"