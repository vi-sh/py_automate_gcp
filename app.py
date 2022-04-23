import json
import requests
import sys
import subprocess
import get_credentials
import display_data
import get_apps_config
import utilities

# -------------------------------------- Creation/configuration ---------------------------------------------------------------------------------

def create_new_gcp_project():
    """
    Creats new Google cloud project
    Important : This functionality was implemented by mimicing the gcloud cli
                Because as a Trail GCP user I am not able to create Organizational resource
                And I cannot create Credentials in the Scope of Organization
                There by I can only access each project individually (By there own service account credentials)
    """
    headers = {"content-type":"application/json; charset=UTF-8"}
    uri = "https://accounts.google.com/o/oauth2/auth"
    project_id = input("Enter unique Project ID:\n")
    project_name = input("Enter Project Name:\n")
    create_new_project = 'gcloud projects create '+ project_id +' --name=' + project_name
    try:
        # Getting Authenticated using gcloud
        response = requests.get(uri, headers=headers)

        if response.status_code == 200:
            subprocess_response = subprocess.Popen(create_new_project, shell=True, stdout=subprocess.PIPE)
            subprocess_return = subprocess_response.stdout.read().decode('utf8')
            print(subprocess_return)

    except requests.exceptions.RequestException as e:
        print("ERROR\n")
        print(e)
        sys.exit()


def add_firebase_to_gcp_project():
    """
    Adds firebase resource to exisitng GCP projects
    Important : In order to add firebase resource to any GCP project
                Please make sure you create a new service account under its respwctive project and
                then you can make use of that credentials to add firebase resource.
    """
    headers = get_credentials.get_gcp_new_service_acc_credentials()
    print("Please enter a valid project id for which firebase resources should be added")
    project_id = input()
    uri = "https://firebase.googleapis.com/v1beta1/projects/"+ project_id +":addFirebase"
    try:
        response = requests.post(uri,headers=headers)
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("ERROR\n")
        print(e)
        sys.exit()
    finally:
        if response.status_code == 409:
            print("Request already exist")
        elif response.status_code == 403:
            print(f"\nERROR : The credentials does not belong to any service account of {project_id} project")
        elif response.status_code == 200:
            utilities.pretty_print_json(data)
        else:
            print("Connection Error")
            sys.exit()


def configure_android_app():
    """
    Creates a new android app within a firebase project (if it exist) with default parameters
    """
    headers = get_credentials.get_gcp_new_service_acc_credentials()
    print("Please enter a valid project id in which this Android app should be created")
    project_id = input()
    uri = "https://firebase.googleapis.com/v1beta1/projects/"+ project_id + "/androidApps"
    try:
        android_app_post_data = {}

        # Making a GET request to check if the project id entered is VALID
        response = requests.get(uri,headers=headers)
        if response.status_code == 200:
            print("Firebase project id entered is valid\nEnter details to configure Android app\n")
            print("Please enter android app displayName")
            android_app_name = input().strip()
            print("\nPlease enter android app packageName\nExample:com.<company>.<appname>")
            android_app_package_name = input().strip()
            android_app_post_data = {'displayName': android_app_name,'packageName':android_app_package_name}
            # android_app_post_data['packageName'] = android_app_package_name
            android_app_post_data = json.dumps(android_app_post_data)
        else:
            print("ERROR : Please enter a valid Project id !!!\n")
            sys.exit()

        # Making POST request to configure new app with collected information
        response = requests.post(uri,headers=headers,data=android_app_post_data)
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("ERROR\n")
        print(e)
        sys.exit()
    finally:
        if response.status_code == 200:
            print(f"\n------SUCCESS: {android_app_name} is created under {project_id} project------\n")
            utilities.pretty_print_json(data)
        else:
            print("Connection Error\nTry again !!!")
            sys.exit()


def configure_ios_app():
    """
    Creates a new ios app within a firebase project (if it exist) with default parameters
    """
    headers = get_credentials.get_firebase_service_acc_credentials()
    print("Please enter a valid project id in which this ios app should be created")
    project_id = input()
    uri = "https://firebase.googleapis.com/v1beta1/projects/"+ project_id + "/iosApps"
    try:
        ios_app_post_data = {}

        # Making a GET request to check if the project id entered is VALID
        response = requests.get(uri,headers=headers)
        if response.status_code == 200:
            print("\nFirebase project id entered is valid\nEnter details to configure ios app\n")
            print("\nPlease enter ios app displayName")
            ios_app_name = input().strip()
            print("\nPlease enter ios app bundleId\nExample:com.<company>.<appname>")
            ios_app_bundleid_name = input().strip()
            ios_app_post_data = {'displayName': ios_app_name,'bundleId':ios_app_bundleid_name}
            ios_app_post_data = json.dumps(ios_app_post_data)
        else:
            print("ERROR : Please enter a valid Project id !!!\n")
            sys.exit()

        # Making POST request to configure new app with collected information
        response = requests.post(uri,headers=headers,data=ios_app_post_data)
        data = response.json()
        
    except requests.exceptions.RequestException as e:
        print("ERROR\n")
        print(e)
        sys.exit()
    finally:
        if response.status_code == 409:
            print("Request already exist")
        elif response.status_code == 200:
            print(f"\n------SUCCESS: {ios_app_name} is created under {project_id} project------\n")
            utilities.pretty_print_json(data)
        else:
            print("Connection Error\nTry again !!!")
            sys.exit()


def main():
    """
    Main funtion that acts as interface with the user to accept inputs
    """
    print("\n|-----------------------------------------------------|")
    print("| Welcome                                             |")
    print("|-----------------------------------------------------|")
    print("| 1. List all GCP projects                            |")
    print("| 2. Create new GCP project                           |")
    print("| 3. Add firebase resource to new GCP project         |")
    print("| 4. Create/Configure new Android app                 |")
    print("| 5. Get android app Configuration                    |")
    print("| 6. Create/Configure new IOS app                     |")
    print("| 7. Get ios app Configuration                        |")
    print("| 8. Exit                                             |")
    print("|-----------------------------------------------------|\n")

    option = input()

    if option == '1':
        display_data.get_all_gcp_projects()
        main()
    elif option == '2':
        create_new_gcp_project()
        main()
    elif option == '3':
        add_firebase_to_gcp_project()
        main()
    elif option == '4':
        configure_android_app()
        main()
    elif option == '5':
        get_apps_config.get_android_app_config()
        main()
    elif option == '6':
        configure_ios_app()
        main()
    elif option == '7':
        get_apps_config.get_ios_app_config()
        main()
    elif option == '8':
        print("===================== Thank you ======================\n")
        sys.exit()
    else:
        print("Invalid entry !\nPlease try again")


if __name__ == "__main__":
    main()
