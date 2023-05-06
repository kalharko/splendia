from flask import jsonify, Response

def jsonifyException(err: Exception) -> Response:
    """Jsonfiy an exception

    Args:
        err (Exception): exception to jsonify

    Returns:
        Response: jsonified exception
    """
    return jsonify({"errorMessage": str(err) })

def jsonifyErrorMessage(errorMessage: str) -> Response:
    """Jsonfiy an error message 

    Args:
        errorMessage (str): error message to jsonify

    Returns:
        Response: jsonified error message
    """
    return jsonify({"errorMessage": errorMessage })
