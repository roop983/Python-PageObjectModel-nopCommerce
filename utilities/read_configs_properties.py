import configparser
import os

# This file will read configuratation keys from config_properties.ini file. This keys will then be passed in yhe Test or Pages files.
config = configparser.RawConfigParser()
base_dir = os.path.dirname(os.path.abspath(__file__)) # By default pytest may be running from a different working directory. To point to this configuratation directory path, use this code to extract the absolute path directory.
config_path = os.path.join(base_dir, "..", "configuratation", "config_properties.ini")
# configuratation.read(".\\configuratation\\config_properties.ini") # This is a relative path. pytest by default is using a different directory. Hence this doesnt work.
config.read(config_path)
project_root_path = os.path.abspath(os.path.join(base_dir, ".."))
# project_root_path = os.path.abspath(os.path.join(os.getcwd(),".."))
# print("Current Working Dir:", os.getcwd())
# print("Base Director Absolute Path:", base_dir) # Same as Current working directory
# print("File Path is: ", config.get('properties_info', 'FILE_PATH_ADMIN_LOGIN'))
# relative_path = config.get('properties_info', 'FILE_PATH_ADMIN_LOGIN')
# excel_file_path = os.path.join(project_root_path, relative_path)
# print("Excel Path", excel_file_path)

class ReadConfig:
    @staticmethod
    def get_base_url():
        base_url = config.get('properties_info', 'BASE_URL')
        return base_url

    @staticmethod
    def get_username():
        username = config.get('properties_info', 'USER_NAME')
        return username

    @staticmethod
    def get_password():
        password = config.get('properties_info', 'PASSWORD')
        return password

    @staticmethod
    def get_admin_login_file():
        relative_path = config.get('properties_info', 'FILE_PATH_ADMIN_LOGIN')
        excel_file = os.path.join(project_root_path, relative_path)
        return excel_file

    @staticmethod
    def get_customers_data_file():
        relative_path = config.get('properties_info', 'CIUSTOMERS_DATA')
        customers_data_file = os.path.join(project_root_path, relative_path)
        return customers_data_file



# Add other keys also. Add the @staticmethod followed by other property name