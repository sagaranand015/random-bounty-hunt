import json

from http import HTTPStatus
from flask import jsonify

from utils.constants import DATASETS_DB_FILE


def get_all_datasets():
    """
    Demo Endpoints for returning all available datasets available with the Dapp backend
    """
    try:
        with open(DATASETS_DB_FILE) as fp:
            datasets_db = json.loads(fp.read())
        return (
            jsonify(dict(status=True, datasets=datasets_db)),
            HTTPStatus.OK,
        )
    except Exception as e:
        return (
            jsonify(dict(status=False, message=str(e))),
            HTTPStatus.BAD_GATEWAY,
        )
