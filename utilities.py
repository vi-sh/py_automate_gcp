import base64
import json

# -------------------------------------- Utilities ---------------------------------------------------------------------------------

def pretty_print_json(json_data):
    """
    Accepts Json object and displays json data in a much readable way
    """
    print(json.dumps(json_data, indent = 3))

def decode_config_data(config_data):
    """
    Returns decoded config data
    """
    content_data = config_data['configFileContents']
    decoded_content_data = base64.b64decode(content_data).decode('utf-8')
    return decoded_content_data