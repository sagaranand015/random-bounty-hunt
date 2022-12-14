import json
import typing

from http import HTTPStatus
from flask import jsonify, request

from .auth import validate_user_token
from utils.utils import validate_dataset_id
from contracts.randomness import get_randomness_from_app


def get_sample_from_dataset():
    """
    Demo Endpoints for returning the randomly sampled data from the DApp backend,
    using the randomness generated by the algorand beacon
    """
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return (
                jsonify(
                    dict(status=False, message="No Auth Header specified. Please specify Authorization header"),
                ),
                HTTPStatus.UNAUTHORIZED,
            )

        if bearer_header := auth_header.split(" "):
            if bearer_header[0] != "Bearer":
                return (
                    jsonify(
                        dict(status=False, message="Authorization header should start with Bearer. Please use correct auth"),
                    ),
                    HTTPStatus.UNAUTHORIZED,
                )

        auth_token = bearer_header[1]
        (validated, decoded_token) = validate_user_token(auth_token)
        if not validated:
            return (
                jsonify(
                    dict(status=False, message="Invalidated Token. Please try again"),
                ),
                HTTPStatus.UNAUTHORIZED,
            )

        print("========== decoded token is: ", decoded_token)
        data = request.get_json()
        if not data.get("dataset_id"):
            return (
                jsonify(
                    dict(status=False, message="Please supply a dataset Id to use this API"),
                ),
                HTTPStatus.BAD_REQUEST,
            )
        if not validate_dataset_id(data.get("dataset_id")):
            return (
                jsonify(
                    dict(status=False, message="Invalid Dataset ID. Please use the correct one"),
                ),
                HTTPStatus.BAD_REQUEST,
            )

        u_data = auth_token + json.dumps(decoded_token) + str(data)
        randomness_resp = get_randomness_from_app(u_data)
        print("======== randomness resp 2 is: ", str(randomness_resp))
        resp_arr = []
        for r in range(0, len(randomness_resp)):
            print("========= r is: ", randomness_resp[r])
            resp_arr.append(randomness_resp[r])

        return (
            jsonify(dict(status=True, message="All Good!", data=data, randomness=str(randomness_resp), resp_arr=resp_arr)),
            HTTPStatus.OK,
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return (
            jsonify(
                dict(status=False, message=str(e))
            ),
            HTTPStatus.BAD_GATEWAY,
        )


def _do_sampling(dataset_id: str, randomness_arr: typing.List):
    """
    Do the actual sampling from the given dataset ID and the randomness array obtained from the algorand beacon
    via the pre-deployed app
    """
    return None

