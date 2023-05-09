from flask import jsonify, Response


def jsonifyException(err: Exception) -> Response:
    """Jsonify an exception

    Args:
        err (Exception): exception to jsonify

    Returns:
        Response: jsonified exception
    """
    return jsonify({"errorMessage": str(err)})


def jsonifyErrorMessage(errorMessage: str) -> Response:
    """Jsonify an error message 

    Args:
        errorMessage (str): error message to jsonify

    Returns:
        Response: jsonified error message
    """
    return jsonify({"errorMessage": errorMessage})
