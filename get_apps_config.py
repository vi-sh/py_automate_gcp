import os
import requests
import sys
import get_credentials
import display_data
import utilities

# -------------------------------------- Get Android and IOS app configuration ---------------------------------------------------------------------------------

def get_android_app_config():
    """
    Gets the android app configuration by taking app name and saves the config to Json
    """
    headers = get_credentials.get_firebase_service_acc_credentials()
    print("Please enter a valid project id where android app exists")
    project_id = input()
    android_app_dataframe = display_data.display_all_android_apps(project_id)
    android_app_id_list = android_app_dataframe['appId'].to_list()
    android_app_name_list = android_app_dataframe['displayName'].to_list()
    print("\nPlease choose the app for which the configuration file needs to be downloaded")
    option = input()
    
    # Here choice-1 since we are displaying index from 1, so inorder to match with list index  
    option = int(option) - 1

    # this app_id holds the ios app id can be used to fetch configurations
    app_id = android_app_id_list[option]
    app_name = android_app_name_list[option]

    uri = "https://firebase.googleapis.com/v1beta1/projects/"+ project_id + "/androidApps/"+ app_id +"/config"
    try:
        response = requests.get(uri, headers=headers)
        config_data = response.json()
        valid_config_info = utilities.decode_config_data(config_data)
        print("Do you want to save this configuration ?")
        choice = input("Y/N:\n")
        if choice == "Y" or choice == "y":
            config_filename = app_name + ".plist"
            config_file_path = os.path.join("output",config_filename)
            if not os.path.exists(config_file_path):
                with open(config_file_path, "w") as outfile:
                    outfile.write(valid_config_info)
            else:
                print(f"ERROR :{config_file_path} file already exist !!\nPlease delete and Try again")
        else:
            pass
    except requests.exceptions.RequestException as e:
        print("ERROR\n")
        print(e)
        sys.exit()
    finally:
        if response.status_code == 409:
            print("Request already exist")
        elif response.status_code == 200:
            print(f"SUCCESS : Configuration file is downloaded\nPath:{config_file_path}")
        else:
            print("Connection Error\nTry again !!!")
            sys.exit()


def get_ios_app_config():
    """
    Gets the ios app configuration by taking app name and saves the config to Json
    """
    headers = get_credentials.get_firebase_service_acc_credentials()
    print("Please enter a valid project id where ios app exists")
    project_id = input()
    ios_app_dataframe = display_data.display_all_ios_apps(project_id)
    ios_app_id_list = ios_app_dataframe['appId'].to_list()
    ios_app_name_list = ios_app_dataframe['displayName'].to_list()
    print("\nPlease choose the app for which the configuration file needs to be downloaded")
    option = input()
    
    # Here choice-1 since we are displaying index from 1, so inorder to match with list index  
    option = int(option) - 1

    # this app_id holds the ios app id can be used to fetch configurations
    app_id = ios_app_id_list[option]
    app_name = ios_app_name_list[option]

    uri = "https://firebase.googleapis.com/v1beta1/projects/"+ project_id + "/iosApps/"+ app_id +"/config"
    try:
        response = requests.get(uri, headers=headers)
        config_data = response.json()
        valid_config_info = utilities.decode_config_data(config_data)
        print("Do you want to save this configuration ?")
        choice = input("Y/N:\n")
        if choice == "Y" or choice == "y":
            config_filename = app_name + ".plist"
            config_file_path = os.path.join("output",config_filename)
            if not os.path.exists(config_file_path):
                with open(config_file_path, "w") as outfile:
                    outfile.write(valid_config_info)
            else:
                print(f"ERROR :{config_file_path} file already exist !!\nPlease delete and Try again")
        else:
            pass
    except requests.exceptions.RequestException as e:
        print("ERROR\n")
        print(e)
        sys.exit()
    finally:
        if response.status_code == 409:
            print("Request already exist")
        elif response.status_code == 200:
            print(f"SUCCESS : Configuration file is downloaded\nPath:{config_file_path}")
        else:
            print("Connection Error\nTry again !!!")
            sys.exit()
