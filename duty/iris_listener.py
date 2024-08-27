import json

from flask import request

from duty.objects import Event, ExceptToJson, dp
from logger import get_writer
from microvk import VkApiResponseException

from .app import DEBUG, app

logger = get_writer('IRIS Callback')


OK_RESP = json.dumps({"response": "ok"})


@app.route('/callback', methods=["POST", "GET"])
def callback():
    event = Event(request)

    if event.method == 'ping':
        return OK_RESP, 200

    if event.secret != event.db.secret and not DEBUG:
        return 'Неверная секретка', 500

    d = dp.event_run(event)
    event.db.sync()
    if d is None:
        d = "ok"
    if d == "ok":
        return OK_RESP
    elif isinstance(d, dict):
        return json.dumps(d, ensure_ascii=False)
    else:
        return r"\\\\\ашипка хэз бин произошла/////" + '\n' + d


@app.errorhandler(ExceptToJson)
def json_error(e):
    return e.response


@app.errorhandler(VkApiResponseException)
def vk_error(e: VkApiResponseException):
    return json.dumps({
        "response": "vk_error",
        "error_code": e.error_code,
        "error_message": e.error_msg
    }, ensure_ascii=False)
