import base64
import os
import json
import requests
import re
import pandas as pd
import sys
import subprocess
from tabulate import tabulate
import get_credentials

# ---------------------Display data about GCP projects, Android apps and IOS apps-----------------------------------------------------------------

def get_all_gcp_projects():
    """
    Lists all GCP projects
    Important : This functionality was implemented by mimicing the gcloud cli
                Because as a Trail GCP user I am not able to create Organizational account
                And I cannot create Credentials in the Scope of Organization
                There by I can only access each project individually (By there own service account credentials)
    """
    headers = {"content-type":"application/json; charset=UTF-8"}
    uri = "https://accounts.google.com/o/oauth2/auth"
    list_all_gcp_project_id= 'gcloud projects list --format="list(projectId)"'
    gcp_project_id_list = []
    try:
        # Getting Authenticated using gcloud
        response = requests.get(uri, headers=headers)

        if response.status_code == 200:
            sr = subprocess.Popen(list_all_gcp_project_id, shell=True, stdout=subprocess.PIPE)
            subprocess_return = sr.stdout.read().decode('utf8')
            regex_pattern = r"[a-zA-Z][a-zA-Z-\d]+"
            gcp_project_id_list = re.findall(regex_pattern, subprocess_return, re.MULTILINE)
            project_id_dataframe_list = pd.DataFrame(gcp_project_id_list,columns=['Project IDs'])

            # Converting to DataFrame and increasing the index so as to pretty print with proper serial number
            project_id_dataframe_list.index += 1
            print(tabulate(project_id_dataframe_list[['Project IDs']],headers=['SLNo','Project IDs'], tablefmt='fancy_grid'))
            return gcp_project_id_list

    except requests.exceptions.RequestException as e:
        print("ERROR\n")
        print(e)
        sys.exit()


def display_all_android_apps(project_id):
    """
    Display all android apps within the firebase project by taking its project id as input
    """
    headers = get_credentials.get_firebase_service_acc_credentials()
    print(f"\nDisplaying all Android apps within {project_id}\n")
    uri = "https://firebase.googleapis.com/v1beta1/projects/"+ project_id +"/androidApps"
    try:
        response = requests.get(uri, headers=headers)
        data = response.json()
        android_apps_data = data['apps']
        android_temp_dict = {}
        for i in range(len(android_apps_data)):
            android_temp_dict[i] = android_apps_data[i]
        # Creating dataframe from dictionary and Transposing it to display heanders properly
        # Creating dataframe also help in better displaying tabular data
        android_app_dataframe = pd.DataFrame.from_dict(android_temp_dict).T
        
        # For displaying index starting from 1
        android_app_dataframe.index += 1
        print(tabulate(android_app_dataframe[["displayName","packageName","appId"]], headers=["slno","displayName","packageName","appId"], tablefmt='fancy_grid'))
    except requests.exceptions.RequestException as e:
        print("ERROR\n")
        print(e)
        sys.exit()
    finally:
        if response.status_code != 200:
            print("Connection Error")
            sys.exit()
        return android_app_dataframe


def display_all_ios_apps(project_id):
    """
    Display all ios apps within the firebase project by its firebase project id as input
    """
    headers = get_credentials.get_firebase_service_acc_credentials()
    print(f"\nDisplaying all ios apps within {project_id}\n")
    uri = "https://firebase.googleapis.com/v1beta1/projects/"+ project_id +"/iosApps"

    try:
        response = requests.get(uri, headers=headers)
        data = response.json()
        # print(data)
        ios_apps_data = data['apps']
        ios_temp_dict = {}
        for i in range(len(ios_apps_data)):
            ios_temp_dict[i] = ios_apps_data[i]
        # Creating dataframe from dictionary and Transposing it to display heanders properly
        # Creating dataframe also help in better displaying tabular data
        ios_app_dataframe = pd.DataFrame.from_dict(ios_temp_dict).T

        # For displaying index starting from 1
        ios_app_dataframe.index += 1
        print(tabulate(ios_app_dataframe[["displayName","bundleId","appId"]], headers=["slno","displayName","bundleId","appId"], tablefmt='fancy_grid'))
    except requests.exceptions.RequestException as e:
        print("ERROR\n")
        print(e)
        sys.exit()
    finally:
        if response.status_code != 200:
            print("Connection Error")
            sys.exit()
        return ios_app_dataframe