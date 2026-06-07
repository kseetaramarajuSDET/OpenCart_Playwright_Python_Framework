import yaml
import logging
import os
from utilities.custom_logger import LogGen


class YamlReader:
    # Initialize logger for the utility
    logger = LogGen.loggen()

    @staticmethod
    def read_loginData_from_Yaml_File(filePath):
        YamlReader.logger.info(f"📂 Attempting to read YAML data from: {filePath}")

        # Check if file exists before opening
        if not os.path.exists(filePath):
            YamlReader.logger.error(f"❌ File not found at path: {filePath}")
            raise FileNotFoundError(f"YAML file missing: {filePath}")

        try:
            with open(filePath, 'r') as file:
                yaml_data_list = yaml.safe_load(file)

            # Log the number of records found
            record_count = len(yaml_data_list)
            YamlReader.logger.info(f"✅ Successfully loaded {record_count} test data records from YAML.")

            # Convert dictionary into a list of tuples for Pytest @parametrize
            # Note: Renamed variable to avoid shadowing the list name
            formatted_data = [
                (data['user'], data['pwd'], data['expected'])
                for data in yaml_data_list
            ]

            return formatted_data

        except yaml.YAMLError as e:
            YamlReader.logger.error(f"❌ Failed to parse YAML file: {str(e)}")
            raise e
        except KeyError as e:
            YamlReader.logger.error(f"❌ YAML structure is missing expected keys: {str(e)}")
            raise e
        except Exception as e:
            YamlReader.logger.error(f"❌ An unexpected error occurred while reading YAML: {str(e)}")
            raise e
