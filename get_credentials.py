from oauth2client.service_account import ServiceAccountCredentials

# -------------------------------------- Passes Credentials ---------------------------------------------------------------------------------

__scopes = [
    'https://www.googleapis.com/auth/firebase',
    'https://www.googleapis.com/auth/userinfo.email',
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/cloudplatformprojects",
    "https://www.googleapis.com/auth/cloud-platform.read-only",
    "https://www.googleapis.com/auth/cloudplatformprojects.readonly",
    "https://www.googleapis.com/auth/firebase",
    "https://www.googleapis.com/auth/firebase.readonly"
]


def get_firebase_service_acc_credentials():
    """
    Returns firebase service account aunthentication
    """
    __credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'keys\\firebase_serviceAccountKey.json', __scopes)

    headers = {"content-type":"application/json; charset=UTF-8"}
    headers['Authorization'] = 'Bearer ' + __credentials.get_access_token().access_token
    # Headers can be extended depending on the requirement within the methods
    return headers


def get_gcp_service_acc_credentials():
    """
    Returns GCP service account aunthentication
    """
    __credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'keys\\important\\service_Account_key_myproject-342009-87d82f5ac31f.json', __scopes)

    headers = {"content-type":"application/json; charset=UTF-8"}
    headers['Authorization'] = 'Bearer ' + __credentials.get_access_token().access_token
    # Headers can be extended depending on the requirement within the methods
    return headers


def get_gcp_new_service_acc_credentials():
    """
    Returns GCP service account aunthentication
    """
    __credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'keys\\important\\new_2nd_gcp_service_Acc_creds.json', __scopes)

    headers = {"content-type":"application/json; charset=UTF-8"}
    headers['Authorization'] = 'Bearer ' + __credentials.get_access_token().access_token
    # Headers can be extended depending on the requirement within the methods
    return headers