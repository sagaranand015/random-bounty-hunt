from http import HTTPStatus
from flask import jsonify


def get_health_status():
    """
    Demo Endpoints for returning the health status of the DApp backend
    """
    try:
        # @TODO: Maybe have a check on the server health!
        return (
            jsonify({"status": HTTPStatus.OK, "message": "All Good!"}),
            HTTPStatus.OK,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "status": HTTPStatus.BAD_GATEWAY,
                    "message": "All NOT Good!" + str(e),
                }
            ),
            HTTPStatus.BAD_GATEWAY,
        )
