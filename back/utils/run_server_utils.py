from flask import jsonify, Response

def jsonifyException(err: Exception) -> Response:
    """Jsonfiy an exception

    Args:
        err (Exception): exception to jsonify

    Returns:
        Response: jonified exception
    """
    return jsonify({"errorMessage": str(err) })