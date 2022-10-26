import os
import json

from .constants import DATASETS_DB_FILE


def get_server_secret_key():
    sec_key = os.getenv("SERVER_SECRET_KEY")
    if sec_key is None:
        print("DEFINE SECRET KEY FOR THE SERVER API")
        raise Exception("No Secret Key Defined for the API. ")
    return sec_key


def validate_dataset_id(dataset_id: str):
    """
    Return True if a valid dataset id is sent, otherwise false
    """
    with open(DATASETS_DB_FILE) as fp:
        datasets_db = json.loads(fp.read())

    print("========= datasets db is: ", datasets_db)

    if dataset_id in datasets_db:
        return True
    return False
