from collections import namedtuple


DataIngestionConfig = namedtuple("DataIngestionConfig",['download_url','dataset_dir','ingested_dir','ingested_train_dir','ingested_test_dir'])

DataValidationConfig = namedtuple('DataValidationConfig',['schema_dir','schema_file_name','report_file_name','report_page_file_name','report_dir'])

DataTransformationConfig = namedtuple('DataTransformationConfig',['transformed_dir',
                                                                  'transformed_train_dir',
                                                                  'transformed_test_dir',
                                                                  'preprocessing_dir',
                                                                  'preprocessed_object_file_name'])

ModelTrainerConfig = namedtuple('ModelTrainerConfig' , ['trained_model_dir',
                                                                    'trained_model_file_name',
                                                                    'base_accuracy',
                                                                    'trained_model_config_dir',
                                                                    'trained_model_config_file_name'])

ModelEvaluationConfig = namedtuple('ModelEvaluationConfig', ['model_evaluation_dir','model_evaluation_file_name'])

ModelPusherConfig = namedtuple('ModelPusherConfig' , ['model_export_dir'])

TrainingPipelineConfig = namedtuple('TrainingPipelineConfig', ['artifact_dir'])