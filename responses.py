from flask import jsonify


def ok_with_data(data, cookie):
    response = jsonify({"status": "ok", "data": data})
    if cookie:
        response.set_cookie(*cookie)
    return response, 200


def ok_created(data):
    return jsonify({"status": "created", "data": data}), 201


def ok_deleted():
    return jsonify({"status": "ok", "details": "deleted"}), 200


def error_not_found():
    return jsonify({"status": "error", "details": "Not found"}), 404


def error_bad_request():
    return jsonify({"status": "error", "details": "Malformed payload"}), 400


def error_auth_req():
    return jsonify(
        {"status": "error", "details": "Invalid email, password or token"}
    ), 401


def error_unauthorized():
    return jsonify({"status": "error", "details": "Unauthorized"}), 403
