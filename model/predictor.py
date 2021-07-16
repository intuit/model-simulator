#!/usr/bin/env python
from flask import Flask, Response, request
import json
import sys
import time

KEY_SLEEP_SECONDS = "sleep_seconds"
KEY_STATUS = "status"
KEY_FILE_PATH = "file_path"
KEY_FILE_CONTENTS = "file_contents"
KEY_MESSAGE = "message"
KEY_ECHO = "echo"
KEY_EXCEPTION = "exception"
KEY_VERSION = "version"
KEY_EMPTY = "empty"

app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return Response(response="\n", status=200, mimetype="application/json")

@app.route("/invocations", methods=["POST"])
def invocations():
    print(f"request.data: {request.data}")

    # Parse request JSON if possible, else set empty dict as placeholder
    try:
        request_dict = json.loads(request.data)
        # Handle case where request was valid JSON but not expected dict format
        if isinstance(request_dict, dict):
            echo = request_dict
        else:
            raise ValueError("Request not in expected dict format")
    except:
        # Request is either not parsable JSON, or if it is, not expected dict.
        # So set empty dict as placeholder, and echo original value.
        request_dict = {}
        echo = request.data
    print(f"request_dict: {request_dict}")

    # Create response with default values
    sleep_seconds = 0
    status = 200
    file_path = ""
    file_contents = ""
    message = []
    version = "v1.3b"
    response_dict = {
        KEY_SLEEP_SECONDS : sleep_seconds,
        KEY_STATUS : status,
        KEY_FILE_PATH : file_path,
        KEY_FILE_CONTENTS : file_contents,
        KEY_MESSAGE : message,
        KEY_ECHO : echo,
        KEY_VERSION : version
    }

    # Handle sleep
    if KEY_SLEEP_SECONDS in request_dict:
        sleep_seconds = request_dict[KEY_SLEEP_SECONDS]
        response_dict[KEY_SLEEP_SECONDS] = sleep_seconds
        print(f"About to sleep {sleep_seconds} seconds")
        time.sleep(sleep_seconds)

    # Handle status
    if KEY_STATUS in request_dict:
        status = request_dict[KEY_STATUS]
        response_dict[KEY_STATUS] = status

    # Handle file
    if KEY_FILE_PATH in request_dict:
        file_path = request_dict[KEY_FILE_PATH]
        response_dict[KEY_FILE_PATH] = file_path
        f = open(f"/opt/ml/model/{file_path}", "r")
        if f.mode == "r":
            file_contents = f.read()
            response_dict[KEY_FILE_CONTENTS] = file_contents

    # Handle message
    if KEY_MESSAGE in request_dict:
        message = request_dict[KEY_MESSAGE]
        response_dict[KEY_MESSAGE] = message

    # Handle exception and test printing to stderr
    if KEY_EXCEPTION in request_dict:
        exception = request_dict[KEY_EXCEPTION]
        print(f"About to raise exception {exception}", file=sys.stderr)
        raise Exception(exception)

    # Handle empty check and return response
    if KEY_EMPTY in request_dict and request_dict[KEY_EMPTY] == True:
        response_string = ""
    else:
        response_string = json.dumps(response_dict, sort_keys=True)
    print(f"Return status {status} and response {response_string}")
    return Response(response=response_string, status=status, mimetype="application/json")
